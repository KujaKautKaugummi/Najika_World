import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import 'dart:io';

import '../services/messenger_service.dart';
import '../models/conversation_model.dart';
import '../models/message_model.dart';
import './widgets/message_bubble.dart';
import '../../../services/media/media_picker_service.dart';
import '../../../services/media/media_encryption_service.dart';

/// Chat Screen
///
/// Shows conversation with contact
class ChatScreen extends StatefulWidget {
  final Conversation conversation;

  const ChatScreen({
    super.key,
    required this.conversation,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  bool _isTyping = false;
  Timer? _typingTimer;
  String? _contactTyping;

  // Disappearing message mode
  bool _disappearingMode = false;
  int _disappearSeconds = 10; // Default 10 seconds

  @override
  void initState() {
    super.initState();

    // Listen for typing indicator
    Provider.of<MessengerService>(context, listen: false)
        .addTypingListener(_onTypingIndicator);

    // Listen for new messages
    Provider.of<MessengerService>(context, listen: false)
        .addMessageListener(_onNewMessage);
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    _typingTimer?.cancel();
    super.dispose();
  }

  void _onTypingIndicator(String contactId, bool isTyping) {
    if (contactId == widget.conversation.contactId) {
      setState(() {
        _contactTyping = isTyping ? widget.conversation.contactName : null;
      });
    }
  }

  void _onNewMessage(Message message) {
    // Scroll to bottom when new message arrives
    if (message.recipientId == widget.conversation.contactId ||
        message.senderId == widget.conversation.contactId) {
      _scrollToBottom();
    }
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      Future.delayed(const Duration(milliseconds: 100), () {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }

  void _sendMessage() async {
    final content = _messageController.text.trim();
    if (content.isEmpty) return;

    final messenger = Provider.of<MessengerService>(context, listen: false);

    try {
      await messenger.sendMessage(
        recipientId: widget.conversation.contactId,
        content: content,
        type: _disappearingMode ? MessageType.disappearing : MessageType.text,
        disappearAfterSeconds: _disappearingMode ? _disappearSeconds : null,
      );

      _messageController.clear();
      _scrollToBottom();
    } catch (e) {
      _showError('Failed to send message: $e');
    }
  }

  void _onTextChanged(String text) {
    if (text.isNotEmpty && !_isTyping) {
      // Start typing
      _isTyping = true;
      Provider.of<MessengerService>(context, listen: false)
          .sendTypingIndicator(widget.conversation.contactId, isTyping: true);

      // Stop typing after 3 seconds of inactivity
      _typingTimer?.cancel();
      _typingTimer = Timer(const Duration(seconds: 3), () {
        _isTyping = false;
        Provider.of<MessengerService>(context, listen: false)
            .sendTypingIndicator(widget.conversation.contactId, isTyping: false);
      });
    } else if (text.isEmpty && _isTyping) {
      // Stopped typing
      _isTyping = false;
      _typingTimer?.cancel();
      Provider.of<MessengerService>(context, listen: false)
          .sendTypingIndicator(widget.conversation.contactId, isTyping: false);
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.conversation.contactName),
            if (_contactTyping != null)
              Text(
                'typing...',
                style: TextStyle(
                  fontSize: 12,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.call),
            onPressed: () {
              // TODO: Start voice call
            },
          ),
          IconButton(
            icon: const Icon(Icons.videocam),
            onPressed: () {
              // TODO: Start avatar call
            },
          ),
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () {
              _showChatOptions();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Disappearing mode banner
          if (_disappearingMode)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(8),
              color: Theme.of(context).colorScheme.primary.withOpacity(0.2),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.timer, size: 16),
                  const SizedBox(width: 8),
                  Text(
                    'Disappearing messages: ${_disappearSeconds}s',
                    style: const TextStyle(fontSize: 12),
                  ),
                  const SizedBox(width: 8),
                  TextButton(
                    onPressed: () {
                      setState(() {
                        _disappearingMode = false;
                      });
                    },
                    child: const Text('Turn off'),
                  ),
                ],
              ),
            ),

          // Messages list
          Expanded(
            child: Consumer<MessengerService>(
              builder: (context, messenger, child) {
                final messages = messenger.getMessages(widget.conversation.id);

                if (messages.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.lock,
                          size: 80,
                          color: Colors.grey[600],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'End-to-end encrypted',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey[600],
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Send your first message',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[500],
                          ),
                        ),
                      ],
                    ),
                  );
                }

                return ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.all(16),
                  itemCount: messages.length,
                  itemBuilder: (context, index) {
                    final message = messages[index];
                    return MessageBubble(
                      message: message,
                      isMe: message.senderId == messenger._userId,
                    );
                  },
                );
              },
            ),
          ),

          // Input area
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              boxShadow: [
                BoxShadow(
                  offset: const Offset(0, -2),
                  blurRadius: 4,
                  color: Colors.black.withOpacity(0.1),
                ),
              ],
            ),
            child: Row(
              children: [
                // Attachment button
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () {
                    _showAttachmentOptions();
                  },
                ),

                // Text input
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Message',
                      border: InputBorder.none,
                    ),
                    maxLines: null,
                    textCapitalization: TextCapitalization.sentences,
                    onChanged: _onTextChanged,
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),

                // Disappearing message toggle
                IconButton(
                  icon: Icon(
                    _disappearingMode ? Icons.timer : Icons.timer_outlined,
                    color: _disappearingMode
                        ? Theme.of(context).colorScheme.primary
                        : null,
                  ),
                  onPressed: () {
                    setState(() {
                      _disappearingMode = !_disappearingMode;
                    });
                    if (_disappearingMode) {
                      _showDisappearingOptions();
                    }
                  },
                ),

                // Send button
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _showChatOptions() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            leading: const Icon(Icons.timer),
            title: const Text('Disappearing messages'),
            trailing: Switch(
              value: _disappearingMode,
              onChanged: (value) {
                setState(() {
                  _disappearingMode = value;
                });
                Navigator.pop(context);
                if (value) {
                  _showDisappearingOptions();
                }
              },
            ),
          ),
          ListTile(
            leading: const Icon(Icons.notifications_off),
            title: Text(widget.conversation.isMuted ? 'Unmute' : 'Mute'),
            onTap: () {
              // TODO: Toggle mute
              Navigator.pop(context);
            },
          ),
          ListTile(
            leading: const Icon(Icons.block, color: Colors.red),
            title: const Text('Block contact', style: TextStyle(color: Colors.red)),
            onTap: () {
              // TODO: Block contact
              Navigator.pop(context);
            },
          ),
        ],
      ),
    );
  }

  void _showDisappearingOptions() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Disappearing messages'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RadioListTile<int>(
              title: const Text('5 seconds'),
              value: 5,
              groupValue: _disappearSeconds,
              onChanged: (value) {
                setState(() {
                  _disappearSeconds = value!;
                });
                Navigator.pop(context);
              },
            ),
            RadioListTile<int>(
              title: const Text('10 seconds'),
              value: 10,
              groupValue: _disappearSeconds,
              onChanged: (value) {
                setState(() {
                  _disappearSeconds = value!;
                });
                Navigator.pop(context);
              },
            ),
            RadioListTile<int>(
              title: const Text('30 seconds'),
              value: 30,
              groupValue: _disappearSeconds,
              onChanged: (value) {
                setState(() {
                  _disappearSeconds = value!;
                });
                Navigator.pop(context);
              },
            ),
            RadioListTile<int>(
              title: const Text('1 minute'),
              value: 60,
              groupValue: _disappearSeconds,
              onChanged: (value) {
                setState(() {
                  _disappearSeconds = value!;
                });
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
    );
  }

  void _showAttachmentOptions() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            leading: const Icon(Icons.photo_camera),
            title: const Text('Camera'),
            onTap: () {
              Navigator.pop(context);
              _handleCamera();
            },
          ),
          ListTile(
            leading: const Icon(Icons.videocam),
            title: const Text('Video'),
            onTap: () {
              Navigator.pop(context);
              _handleVideo();
            },
          ),
          ListTile(
            leading: const Icon(Icons.photo_library),
            title: const Text('Gallery'),
            onTap: () {
              Navigator.pop(context);
              _handleGallery();
            },
          ),
          ListTile(
            leading: const Icon(Icons.insert_drive_file),
            title: const Text('File'),
            onTap: () {
              Navigator.pop(context);
              _handleFile();
            },
          ),
        ],
      ),
    );
  }

  Future<void> _handleCamera() async {
    try {
      final file = await MediaPickerService.instance.pickImageFromCamera();
      if (file != null) {
        await _sendMediaFile(file, MessageType.image);
      }
    } catch (e) {
      _showError('Camera error: $e');
    }
  }

  Future<void> _handleVideo() async {
    try {
      final file = await MediaPickerService.instance.recordVideo();
      if (file != null) {
        await _sendMediaFile(file, MessageType.video);
      }
    } catch (e) {
      _showError('Video error: $e');
    }
  }

  Future<void> _handleGallery() async {
    try {
      final file = await MediaPickerService.instance.pickImageFromGallery();
      if (file != null) {
        await _sendMediaFile(file, MessageType.image);
      }
    } catch (e) {
      _showError('Gallery error: $e');
    }
  }

  Future<void> _handleFile() async {
    try {
      final file = await MediaPickerService.instance.pickFile();
      if (file != null) {
        await _sendMediaFile(file, MessageType.file);
      }
    } catch (e) {
      _showError('File error: $e');
    }
  }

  Future<void> _sendMediaFile(File file, MessageType type) async {
    final messenger = Provider.of<MessengerService>(context, listen: false);

    try {
      // Show uploading indicator
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Row(
            children: [
              SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
              SizedBox(width: 16),
              Text('Encrypting and uploading...'),
            ],
          ),
          duration: Duration(minutes: 5),
        ),
      );

      // Encrypt the file
      final encryptionService = MediaEncryptionService.instance;

      // Derive encryption key from conversation
      // In production, this would use the shared secret from the ratchet
      final encryptionKey = await encryptionService.deriveKeyFromPassword(
        'shared-secret-${widget.conversation.contactId}',
      );

      final encryptedFile = await encryptionService.encryptFile(file, encryptionKey);

      // Upload encrypted file
      final mediaUrl = await messenger.uploadMedia(encryptedFile);

      // Send message with media URL
      await messenger.sendMessage(
        recipientId: widget.conversation.contactId,
        content: file.path.split('/').last, // Original filename
        type: type,
        mediaUrl: mediaUrl,
        disappearAfterSeconds: _disappearingMode ? _disappearSeconds : null,
      );

      // Cleanup
      await encryptedFile.delete();
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Sent!'),
          duration: Duration(seconds: 2),
        ),
      );

      _scrollToBottom();
    } catch (e) {
      ScaffoldMessenger.of(context).hideCurrentSnackBar();
      _showError('Failed to send media: $e');
    }
  }
}
