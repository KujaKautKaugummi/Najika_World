import 'dart:typed_data';
import 'dart:convert';
import 'package:cryptography/cryptography.dart';
import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart';

import './post_quantum_crypto.dart';

/// Double Ratchet Implementation
///
/// Signal Protocol's Double Ratchet provides:
/// - Perfect Forward Secrecy
/// - Post-Compromise Security
/// - Self-healing after key compromise
///
/// Based on Signal's specification:
/// https://signal.org/docs/specifications/doubleratchet/
class DoubleRatchet {
  // Ratchet state
  SimpleKeyPair? _dhSendingKey;
  SimpleKeyPair? _dhReceivingKey;
  SimplePublicKey? _dhRemotePublicKey;

  Uint8List? _rootKey;
  Uint8List? _sendingChainKey;
  Uint8List? _receivingChainKey;

  int _sendingMessageNumber = 0;
  int _receivingMessageNumber = 0;
  int _previousSendingChainLength = 0;

  // Skipped message keys (for out-of-order messages)
  final Map<String, Uint8List> _skippedMessageKeys = {};

  // Constants
  static const int maxSkip = 1000; // Max messages to skip

  // Crypto
  final x25519 = X25519();
  final hkdf = Hkdf(hmac: Hmac(Sha256()), outputLength: 32);

  /// Initialize as Alice (sender initiating conversation)
  Future<void> initializeAsAlice({
    required Uint8List sharedSecret,
    required SimplePublicKey bobPublicKey,
  }) async {
    _rootKey = sharedSecret;
    _dhRemotePublicKey = bobPublicKey;

    // Generate our first DH key pair
    _dhSendingKey = await x25519.newKeyPair();

    // Perform initial DH ratchet
    await _dhRatchet();
  }

  /// Initialize as Bob (receiver)
  Future<void> initializeAsBob({
    required Uint8List sharedSecret,
    required SimpleKeyPair bobKeyPair,
  }) async {
    _rootKey = sharedSecret;
    _dhReceivingKey = bobKeyPair;
  }

  /// Encrypt message
  Future<RatchetMessage> encryptMessage(String plaintext) async {
    if (_sendingChainKey == null) {
      throw Exception('Sending chain not initialized');
    }

    // Derive message key from chain key
    final messageKey = await _deriveMessageKey(_sendingChainKey!);

    // Encrypt plaintext
    final ciphertext = await _encryptWithMessageKey(
      plaintext,
      messageKey,
    );

    // Get current DH public key
    final dhPublicKey = await _dhSendingKey!.extractPublicKey();

    // Advance chain
    _sendingChainKey = await _advanceChainKey(_sendingChainKey!);
    final messageNumber = _sendingMessageNumber;
    _sendingMessageNumber++;

    return RatchetMessage(
      ciphertext: ciphertext,
      dhPublicKey: dhPublicKey,
      messageNumber: messageNumber,
      previousChainLength: _previousSendingChainLength,
    );
  }

  /// Decrypt message
  Future<String> decryptMessage(RatchetMessage message) async {
    // Check if we have a skipped message key
    final skippedKey = _trySkippedMessageKeys(message);
    if (skippedKey != null) {
      return await _decryptWithMessageKey(message.ciphertext, skippedKey);
    }

    // Check if we need to perform DH ratchet
    if (message.dhPublicKey.bytes != _dhRemotePublicKey?.bytes) {
      await _skipMessageKeys(message.previousChainLength);
      await _dhRatchetReceive(message.dhPublicKey);
    }

    // Skip any messages we haven't received yet
    await _skipMessageKeys(message.messageNumber);

    // Derive message key
    final messageKey = await _deriveMessageKey(_receivingChainKey!);

    // Decrypt
    final plaintext = await _decryptWithMessageKey(
      message.ciphertext,
      messageKey,
    );

    // Advance chain
    _receivingChainKey = await _advanceChainKey(_receivingChainKey!);
    _receivingMessageNumber++;

    return plaintext;
  }

  /// Perform DH ratchet (sending)
  Future<void> _dhRatchet() async {
    // Store previous chain length
    _previousSendingChainLength = _sendingMessageNumber;

    // Reset message counter
    _sendingMessageNumber = 0;

    // Compute DH
    final dhOutput = await x25519.sharedSecretKey(
      keyPair: _dhSendingKey!,
      remotePublicKey: _dhRemotePublicKey!,
    );

    // KDF to get new root key and sending chain key
    final kdfOutput = await _kdfRootKey(_rootKey!, await dhOutput.extractBytes());
    _rootKey = kdfOutput.rootKey;
    _sendingChainKey = kdfOutput.chainKey;
  }

  /// Perform DH ratchet (receiving)
  Future<void> _dhRatchetReceive(SimplePublicKey newPublicKey) async {
    // Store previous chain length
    _previousSendingChainLength = _sendingMessageNumber;
    _sendingMessageNumber = 0;
    _receivingMessageNumber = 0;

    // Update remote public key
    _dhRemotePublicKey = newPublicKey;

    // Compute DH with receiving key
    final dhOutput = await x25519.sharedSecretKey(
      keyPair: _dhReceivingKey!,
      remotePublicKey: newPublicKey,
    );

    // KDF for receiving chain
    final kdfOutput1 = await _kdfRootKey(_rootKey!, await dhOutput.extractBytes());
    _rootKey = kdfOutput1.rootKey;
    _receivingChainKey = kdfOutput1.chainKey;

    // Generate new sending key
    _dhSendingKey = await x25519.newKeyPair();

    // Compute DH with new sending key
    final dhOutput2 = await x25519.sharedSecretKey(
      keyPair: _dhSendingKey!,
      remotePublicKey: newPublicKey,
    );

    // KDF for sending chain
    final kdfOutput2 = await _kdfRootKey(_rootKey!, await dhOutput2.extractBytes());
    _rootKey = kdfOutput2.rootKey;
    _sendingChainKey = kdfOutput2.chainKey;
  }

  /// KDF for root key
  Future<KdfOutput> _kdfRootKey(Uint8List rootKey, List<int> dhOutput) async {
    // HKDF with root key as salt
    final derivedKey = await hkdf.deriveKey(
      secretKey: SecretKey(dhOutput),
      nonce: rootKey,
      info: utf8.encode('DoubleRatchet'),
    );

    final bytes = await derivedKey.extractBytes();

    return KdfOutput(
      rootKey: Uint8List.fromList(bytes.sublist(0, 32)),
      chainKey: Uint8List.fromList(bytes.sublist(32, 64)),
    );
  }

  /// Derive message key from chain key
  Future<Uint8List> _deriveMessageKey(Uint8List chainKey) async {
    // HMAC-SHA256 with constant
    final hmac = Hmac(Sha256());
    final mac = await hmac.calculateMac(
      [0x01], // Constant for message key
      secretKey: SecretKey(chainKey),
    );

    return Uint8List.fromList(mac.bytes);
  }

  /// Advance chain key
  Future<Uint8List> _advanceChainKey(Uint8List chainKey) async {
    // HMAC-SHA256 with constant
    final hmac = Hmac(Sha256());
    final mac = await hmac.calculateMac(
      [0x02], // Constant for chain key
      secretKey: SecretKey(chainKey),
    );

    return Uint8List.fromList(mac.bytes);
  }

  /// Encrypt with message key (AES-256-GCM)
  Future<Uint8List> _encryptWithMessageKey(
    String plaintext,
    Uint8List messageKey,
  ) async {
    final algorithm = AesGcm.with256bits();

    final secretBox = await algorithm.encrypt(
      utf8.encode(plaintext),
      secretKey: SecretKey(messageKey),
    );

    // Combine nonce + ciphertext + mac
    final result = <int>[];
    result.addAll(secretBox.nonce);
    result.addAll(secretBox.cipherText);
    result.addAll(secretBox.mac.bytes);

    return Uint8List.fromList(result);
  }

  /// Decrypt with message key
  Future<String> _decryptWithMessageKey(
    Uint8List ciphertext,
    Uint8List messageKey,
  ) async {
    final algorithm = AesGcm.with256bits();

    // Split nonce + ciphertext + mac
    final nonce = ciphertext.sublist(0, 12);
    final encrypted = ciphertext.sublist(12, ciphertext.length - 16);
    final mac = Mac(ciphertext.sublist(ciphertext.length - 16));

    final secretBox = SecretBox(
      encrypted,
      nonce: nonce,
      mac: mac,
    );

    final decrypted = await algorithm.decrypt(
      secretBox,
      secretKey: SecretKey(messageKey),
    );

    return utf8.decode(decrypted);
  }

  /// Try to use skipped message key
  Uint8List? _trySkippedMessageKeys(RatchetMessage message) {
    final key = '${base64Encode(message.dhPublicKey.bytes)}_${message.messageNumber}';
    return _skippedMessageKeys.remove(key);
  }

  /// Skip message keys (store for later)
  Future<void> _skipMessageKeys(int until) async {
    if (_receivingMessageNumber + maxSkip < until) {
      throw Exception('Too many skipped messages');
    }

    if (_receivingChainKey != null) {
      while (_receivingMessageNumber < until) {
        final messageKey = await _deriveMessageKey(_receivingChainKey!);

        // Store skipped key
        final key = '${base64Encode(_dhRemotePublicKey!.bytes)}_$_receivingMessageNumber';
        _skippedMessageKeys[key] = messageKey;

        _receivingChainKey = await _advanceChainKey(_receivingChainKey!);
        _receivingMessageNumber++;
      }
    }
  }

  /// Export session state (for persistence)
  Map<String, dynamic> exportState() {
    return {
      'root_key': _rootKey != null ? base64Encode(_rootKey!) : null,
      'sending_chain_key': _sendingChainKey != null ? base64Encode(_sendingChainKey!) : null,
      'receiving_chain_key': _receivingChainKey != null ? base64Encode(_receivingChainKey!) : null,
      'sending_message_number': _sendingMessageNumber,
      'receiving_message_number': _receivingMessageNumber,
      'previous_sending_chain_length': _previousSendingChainLength,
      // Note: DH keys and skipped keys should be stored separately
    };
  }
}

/// Triple Ratchet (Post-Quantum Extension)
///
/// Extends Double Ratchet with Post-Quantum keys
/// As specified in Signal's PQXDH protocol
class TripleRatchet extends DoubleRatchet {
  // Post-Quantum state
  KyberKeyPair? _pqSendingKey;
  KyberPublicKey? _pqRemotePublicKey;
  Uint8List? _pqChainKey;

  /// Initialize with Post-Quantum keys
  Future<void> initializeWithPQ({
    required Uint8List sharedSecret,
    required SimplePublicKey bobPublicKey,
    required KyberPublicKey bobPQPublicKey,
  }) async {
    // Initialize classical Double Ratchet
    await initializeAsAlice(
      sharedSecret: sharedSecret,
      bobPublicKey: bobPublicKey,
    );

    // Initialize PQ ratchet
    _pqRemotePublicKey = bobPQPublicKey;
    _pqSendingKey = await PostQuantumCrypto.instance.generateKyberKeyPair();

    // Mix PQ shared secret into root key
    await _pqRatchet();
  }

  /// Perform Post-Quantum ratchet
  Future<void> _pqRatchet() async {
    // Encapsulate to get PQ shared secret
    final pqResult = await PostQuantumCrypto.instance._kyberEncapsulate(
      _pqRemotePublicKey!,
    );

    // Mix into root key using KDF
    final combined = <int>[];
    combined.addAll(_rootKey!);
    combined.addAll(pqResult.sharedSecret);

    final derivedKey = await hkdf.deriveKey(
      secretKey: SecretKey(combined),
      nonce: Uint8List(32),
      info: utf8.encode('TripleRatchet-PQ'),
    );

    _rootKey = Uint8List.fromList(await derivedKey.extractBytes());
  }

  @override
  Future<RatchetMessage> encryptMessage(String plaintext) async {
    // Perform classical Double Ratchet encryption
    final message = await super.encryptMessage(plaintext);

    // Add PQ public key to message
    if (_pqSendingKey != null) {
      message.pqPublicKey = _pqSendingKey!.publicKey;
    }

    return message;
  }
}

// ============================================================================
// DATA MODELS
// ============================================================================

/// Ratchet message envelope
class RatchetMessage {
  final Uint8List ciphertext;
  final SimplePublicKey dhPublicKey;
  final int messageNumber;
  final int previousChainLength;

  // Post-Quantum (optional)
  KyberPublicKey? pqPublicKey;

  RatchetMessage({
    required this.ciphertext,
    required this.dhPublicKey,
    required this.messageNumber,
    required this.previousChainLength,
    this.pqPublicKey,
  });

  Map<String, dynamic> toJson() {
    return {
      'ciphertext': base64Encode(ciphertext),
      'dh_public_key': base64Encode(dhPublicKey.bytes),
      'message_number': messageNumber,
      'previous_chain_length': previousChainLength,
      'pq_public_key': pqPublicKey?.toBase64(),
    };
  }

  factory RatchetMessage.fromJson(Map<String, dynamic> json) {
    return RatchetMessage(
      ciphertext: base64Decode(json['ciphertext']),
      dhPublicKey: SimplePublicKey(
        base64Decode(json['dh_public_key']),
        type: KeyPairType.x25519,
      ),
      messageNumber: json['message_number'],
      previousChainLength: json['previous_chain_length'],
      pqPublicKey: json['pq_public_key'] != null
          ? KyberPublicKey.fromBase64(json['pq_public_key'])
          : null,
    );
  }
}

/// KDF output
class KdfOutput {
  final Uint8List rootKey;
  final Uint8List chainKey;

  KdfOutput({
    required this.rootKey,
    required this.chainKey,
  });
}

/// Session manager for multiple conversations
class SessionManager {
  final Map<String, DoubleRatchet> _sessions = {};
  final Map<String, TripleRatchet> _pqSessions = {};

  /// Get or create session
  DoubleRatchet getSession(String contactId, {bool usePostQuantum = true}) {
    if (usePostQuantum) {
      return _pqSessions.putIfAbsent(contactId, () => TripleRatchet());
    }
    return _sessions.putIfAbsent(contactId, () => DoubleRatchet());
  }

  /// Remove session
  void removeSession(String contactId) {
    _sessions.remove(contactId);
    _pqSessions.remove(contactId);
  }

  /// Clear all sessions
  void clearAll() {
    _sessions.clear();
    _pqSessions.clear();
  }
}
