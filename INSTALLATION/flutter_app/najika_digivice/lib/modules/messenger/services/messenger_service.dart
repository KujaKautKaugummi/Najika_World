import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:uuid/uuid.dart';

import '../../../services/crypto/double_ratchet.dart';
import '../../../services/crypto/post_quantum_crypto.dart';
import '../../../services/network/connection_manager.dart';
import '../../../services/storage/secure_storage_service.dart';
import '../../../services/database/database_service.dart';
import '../../../core/constants/app_constants.dart';
import '../models/message_model.dart';
import '../models/conversation_model.dart';

/// Messenger Service
///
/// Handles all messaging functionality:
/// - E2E encryption (Double/Triple Ratchet)
/// - Message sending/receiving
/// - WebSocket real-time communication
/// - Message persistence
/// - Disappearing messages
class MessengerService extends ChangeNotifier {
  static final MessengerService instance = MessengerService._();
  MessengerService._();

  // State
  bool _isInitialized = false;
  bool _isConnected = false;
  String? _userId;
  String? _deviceId;

  // WebSocket
  IO.Socket? _socket;

  // Sessions (Double/Triple Ratchet)
  final SessionManager _sessionManager = SessionManager();

  // Conversations
  final Map<String, Conversation> _conversations = {};
  final Map<String, List<Message>> _messages = {};

  // Message callbacks
  final List<Function(Message)> _messageListeners = [];
  final List<Function(String, bool)> _typingListeners = [];

  // Getters
  bool get isInitialized => _isInitialized;
  bool get isConnected => _isConnected;
  List<Conversation> get conversations => _conversations.values.toList();

  /// Initialize messenger
  Future<void> initialize() async {
    debugPrint('💬 MessengerService: Initializing...');

    // Get user info
    _userId = await SecureStorageService.instance.read(
      AppConstants.userIdKey,
    );
    _deviceId = await SecureStorageService.instance.read(
      AppConstants.deviceIdKey,
    );

    if (_userId == null || _deviceId == null) {
      throw Exception('User not authenticated');
    }

    // Connect WebSocket
    await _connectWebSocket();

    // Load conversations
    await _loadConversations();

    _isInitialized = true;
    debugPrint('✅ MessengerService: Initialized');
  }

  /// Connect to WebSocket
  Future<void> _connectWebSocket() async {
    final messengerUrl = ConnectionManager.instance.activeMessengerUrl ??
        AppConstants.messengerServerUrl;

    debugPrint('🔌 Connecting to: $messengerUrl');

    _socket = IO.io(messengerUrl,
      IO.OptionBuilder()
        .setTransports(['websocket'])
        .disableAutoConnect()
        .build(),
    );

    // Connection handlers
    _socket!.onConnect((_) {
      debugPrint('✅ WebSocket connected');
      _isConnected = true;
      notifyListeners();

      // Authenticate
      _socket!.emit('authenticate', {
        'user_id': _userId,
        'device_id': _deviceId,
      });
    });

    _socket!.onDisconnect((_) {
      debugPrint('❌ WebSocket disconnected');
      _isConnected = false;
      notifyListeners();
    });

    // Message handlers
    _socket!.on('new_message', (data) {
      _handleIncomingMessage(data);
    });

    _socket!.on('typing_indicator', (data) {
      _handleTypingIndicator(data);
    });

    _socket!.on('auth_success', (data) {
      debugPrint('✅ Authenticated: ${data['queued_messages']} queued');
    });

    _socket!.on('panic_wipe', (data) {
      debugPrint('🚨 Panic wipe triggered by server!');
      // Trigger local panic wipe
    });

    // Connect
    _socket!.connect();
  }

  /// Send message
  Future<void> sendMessage({
    required String recipientId,
    required String content,
    MessageType type = MessageType.text,
    int? disappearAfterSeconds,
  }) async {
    if (!_isConnected) {
      throw Exception('Not connected to server');
    }

    // Get or create session
    final session = _sessionManager.getSession(recipientId, usePostQuantum: true);

    // Check if session is initialized
    if (!await _isSessionInitialized(recipientId)) {
      await _initializeSession(recipientId);
    }

    // Create message object
    final message = Message(
      id: const Uuid().v4(),
      senderId: _userId!,
      recipientId: recipientId,
      content: content,
      type: type,
      timestamp: DateTime.now(),
      isRead: false,
      isSent: false,
      disappearAfterSeconds: disappearAfterSeconds,
    );

    // Encrypt message
    final ratchetMessage = await session.encryptMessage(content);

    // Create encrypted payload
    final payload = {
      'type': type.toString(),
      'content': message.toJson(),
      'ratchet': ratchetMessage.toJson(),
    };

    final encryptedPayload = base64Encode(
      utf8.encode(jsonEncode(payload)),
    );

    // Send via WebSocket
    _socket!.emit('send_message', {
      'recipient_id': recipientId,
      'encrypted_payload': encryptedPayload,
      'sealed_sender': true,
    });

    // Store locally
    message.isSent = true;
    await _storeMessage(message);

    // Update conversation
    await _updateConversation(recipientId, message);

    notifyListeners();
  }

  /// Handle incoming message
  Future<void> _handleIncomingMessage(dynamic data) async {
    try {
      final messageData = data['message'];
      final senderId = messageData['sender_id'] ?? 'unknown';
      final encryptedPayload = messageData['encrypted_payload'];

      // Decode payload
      final payloadJson = jsonDecode(
        utf8.decode(base64Decode(encryptedPayload)),
      );

      // Get ratchet message
      final ratchetMessage = RatchetMessage.fromJson(payloadJson['ratchet']);

      // Get session
      final session = _sessionManager.getSession(senderId, usePostQuantum: true);

      // Decrypt
      final decryptedContent = await session.decryptMessage(ratchetMessage);

      // Parse message
      final messageContent = Message.fromJson(payloadJson['content']);
      messageContent.content = decryptedContent;

      // Store locally
      await _storeMessage(messageContent);

      // Update conversation
      await _updateConversation(senderId, messageContent);

      // Notify listeners
      for (final listener in _messageListeners) {
        listener(messageContent);
      }

      // Handle disappearing message
      if (messageContent.disappearAfterSeconds != null) {
        _scheduleMessageDeletion(messageContent);
      }

      notifyListeners();

      debugPrint('✅ Message received and decrypted');
    } catch (e) {
      debugPrint('❌ Failed to handle message: $e');
    }
  }

  /// Initialize session with contact
  Future<void> _initializeSession(String contactId) async {
    // Fetch prekey bundle from server
    final client = ConnectionManager.instance.createMessengerClient();

    final response = await client.get(
      '/api/messenger/prekeys/$contactId',
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to fetch prekey bundle');
    }

    final bundleData = response.data['prekey_bundle'];

    // Parse bundle
    final bundle = PQXDHPreKeyBundle(
      identityKey: SimplePublicKey(
        base64Decode(bundleData['identity_key']),
        type: KeyPairType.x25519,
      ),
      signedPreKey: SimplePublicKey(
        base64Decode(bundleData['signed_prekey']),
        type: KeyPairType.x25519,
      ),
      signedPreKeySignature: base64Decode(bundleData['signed_prekey_signature']),
      oneTimePreKey: bundleData['one_time_prekey'] != null
          ? SimplePublicKey(
              base64Decode(bundleData['one_time_prekey']),
              type: KeyPairType.x25519,
            )
          : null,
      kyberPreKey: KyberPublicKey.fromBase64(bundleData['pq_last_resort_prekey']),
      kyberOneTimePreKey: bundleData['pq_one_time_prekey'] != null
          ? KyberPublicKey.fromBase64(bundleData['pq_one_time_prekey'])
          : null,
      deviceId: bundleData['device_id'],
      createdAt: DateTime.parse(bundleData['created_at']),
    );

    // Perform PQXDH key exchange
    final ourIdentityKey = await PostQuantumCrypto.instance.generateIdentityKeyPair();
    final ourEphemeralKey = await PostQuantumCrypto.instance.x25519.newKeyPair();

    final sharedSecret = await PostQuantumCrypto.instance.performPQXDHInitiator(
      ourIdentityKey: ourIdentityKey.classical,
      ourEphemeralKey: ourEphemeralKey,
      theirIdentityKey: bundle.identityKey,
      theirSignedPreKey: bundle.signedPreKey,
      theirOneTimePreKey: bundle.oneTimePreKey,
      theirKyberPreKey: bundle.kyberPreKey,
    );

    // Initialize session
    final session = _sessionManager.getSession(contactId, usePostQuantum: true);
    if (session is TripleRatchet) {
      await session.initializeWithPQ(
        sharedSecret: sharedSecret,
        bobPublicKey: bundle.identityKey,
        bobPQPublicKey: bundle.kyberPreKey,
      );
    } else {
      await session.initializeAsAlice(
        sharedSecret: sharedSecret,
        bobPublicKey: bundle.identityKey,
      );
    }

    debugPrint('✅ Session initialized with $contactId');
  }

  /// Check if session is initialized
  Future<bool> _isSessionInitialized(String contactId) async {
    // Check if session exists and has keys
    final session = _sessionManager.getSession(contactId);
    final state = session.exportState();
    return state['root_key'] != null;
  }

  /// Store message locally
  Future<void> _storeMessage(Message message) async {
    final conversationId = message.senderId == _userId
        ? message.recipientId
        : message.senderId;

    _messages.putIfAbsent(conversationId, () => []);
    _messages[conversationId]!.add(message);

    // Persist to database
    try {
      await DatabaseService.instance.saveMessage(message, conversationId);
      debugPrint('💾 Message saved to database');
    } catch (e) {
      debugPrint('❌ Failed to save message to database: $e');
    }
  }

  /// Update conversation
  Future<void> _updateConversation(String contactId, Message lastMessage) async {
    if (!_conversations.containsKey(contactId)) {
      _conversations[contactId] = Conversation(
        id: contactId,
        contactId: contactId,
        contactName: 'User $contactId', // TODO: Get actual name from ContactService
        lastMessage: lastMessage,
        unreadCount: 0,
        lastActivity: DateTime.now(),
      );
    } else {
      _conversations[contactId]!.lastMessage = lastMessage;
      _conversations[contactId]!.lastActivity = DateTime.now();
      if (lastMessage.senderId != _userId) {
        _conversations[contactId]!.unreadCount++;
      }
    }

    // Persist to database
    try {
      await DatabaseService.instance.saveConversation(_conversations[contactId]!);
      debugPrint('💾 Conversation saved to database');
    } catch (e) {
      debugPrint('❌ Failed to save conversation to database: $e');
    }

    notifyListeners();
  }

  /// Load conversations from storage
  Future<void> _loadConversations() async {
    try {
      debugPrint('📥 Loading conversations from database...');
      final conversations = await DatabaseService.instance.getConversations();

      for (final conversation in conversations) {
        _conversations[conversation.contactId] = conversation;

        // Load messages for this conversation
        final messages = await DatabaseService.instance.getMessages(conversation.id);
        _messages[conversation.contactId] = messages;
      }

      debugPrint('✅ Loaded ${conversations.length} conversations');
      notifyListeners();
    } catch (e) {
      debugPrint('❌ Failed to load conversations: $e');
    }
  }

  /// Get messages for conversation
  List<Message> getMessages(String conversationId) {
    // If not in memory, try loading from database
    if (_messages[conversationId] == null) {
      _loadMessagesForConversation(conversationId);
    }
    return _messages[conversationId] ?? [];
  }

  /// Load messages for a specific conversation
  Future<void> _loadMessagesForConversation(String conversationId) async {
    try {
      final messages = await DatabaseService.instance.getMessages(conversationId);
      _messages[conversationId] = messages;
      notifyListeners();
    } catch (e) {
      debugPrint('❌ Failed to load messages for $conversationId: $e');
    }
  }

  /// Mark conversation as read
  void markAsRead(String conversationId) {
    if (_conversations.containsKey(conversationId)) {
      _conversations[conversationId]!.unreadCount = 0;
      notifyListeners();
    }
  }

  /// Send typing indicator
  void sendTypingIndicator(String recipientId, {bool isTyping = true}) {
    if (_isConnected) {
      _socket!.emit('typing', {
        'recipient_id': recipientId,
        'is_typing': isTyping,
      });
    }
  }

  /// Handle typing indicator
  void _handleTypingIndicator(dynamic data) {
    final senderId = data['sender_id'];
    final isTyping = data['is_typing'];

    for (final listener in _typingListeners) {
      listener(senderId, isTyping);
    }
  }

  /// Add message listener
  void addMessageListener(Function(Message) callback) {
    _messageListeners.add(callback);
  }

  /// Remove message listener
  void removeMessageListener(Function(Message) callback) {
    _messageListeners.remove(callback);
  }

  /// Add typing listener
  void addTypingListener(Function(String, bool) callback) {
    _typingListeners.add(callback);
  }

  /// Schedule message deletion (disappearing messages)
  void _scheduleMessageDeletion(Message message) {
    if (message.disappearAfterSeconds == null) return;

    Future.delayed(Duration(seconds: message.disappearAfterSeconds!), () {
      _deleteMessage(message);
    });
  }

  /// Delete message
  Future<void> _deleteMessage(Message message) async {
    final conversationId = message.senderId == _userId
        ? message.recipientId
        : message.senderId;

    _messages[conversationId]?.remove(message);

    // Delete from database
    try {
      await DatabaseService.instance.deleteMessage(message.id);
      debugPrint('🗑️ Message deleted (disappeared) from memory and database');
    } catch (e) {
      debugPrint('❌ Failed to delete message from database: $e');
    }

    notifyListeners();
  }

  /// Upload media file (encrypted)
  Future<String> uploadMedia(File file) async {
    // TODO: Implement actual upload to server
    // For now, this is a placeholder that would upload the encrypted file
    // to the server and return the URL

    // In production:
    // 1. Upload encrypted file to server
    // 2. Server returns URL without decrypting
    // 3. Return URL to be included in message

    debugPrint('📤 Uploading media: ${file.path}');

    // Placeholder - would use dio/http to upload
    await Future.delayed(const Duration(seconds: 2));

    return 'https://najika.example.com/media/${DateTime.now().millisecondsSinceEpoch}.enc';
  }

  /// Disconnect
  void disconnect() {
    _socket?.disconnect();
    _socket?.dispose();
    _isConnected = false;
    notifyListeners();
  }

  @override
  void dispose() {
    disconnect();
    _messageListeners.clear();
    _typingListeners.clear();
    super.dispose();
  }
}
