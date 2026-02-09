import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/foundation.dart';

/// Secure Storage Service
///
/// Wrapper around FlutterSecureStorage with:
/// - EncryptedSharedPreferences on Android
/// - Keychain on iOS
/// - Encrypted at rest
class SecureStorageService {
  static final SecureStorageService instance = SecureStorageService._();
  SecureStorageService._();

  late FlutterSecureStorage _storage;
  bool _isInitialized = false;

  /// Initialize secure storage
  Future<void> initialize() async {
    debugPrint('🔐 SecureStorageService: Initializing...');

    // Configure with platform-specific options
    _storage = const FlutterSecureStorage(
      aOptions: AndroidOptions(
        encryptedSharedPreferences: true, // NEW in V5.0.0!
        keyCipherAlgorithm: KeyCipherAlgorithm.RSA_ECB_OAEPwithSHA_256andMGF1Padding,
        storageCipherAlgorithm: StorageCipherAlgorithm.AES_GCM_NoPadding,
      ),
      iOptions: IOSOptions(
        accessibility: KeychainAccessibility.first_unlock_this_device,
      ),
    );

    _isInitialized = true;
    debugPrint('✅ SecureStorageService: Initialized');
  }

  /// Write key-value pair
  Future<void> write(String key, String value) async {
    _ensureInitialized();
    await _storage.write(key: key, value: value);
    debugPrint('✅ Stored: $key');
  }

  /// Read value by key
  Future<String?> read(String key) async {
    _ensureInitialized();
    return await _storage.read(key: key);
  }

  /// Delete value by key
  Future<void> delete(String key) async {
    _ensureInitialized();
    await _storage.delete(key: key);
    debugPrint('✅ Deleted: $key');
  }

  /// Delete all values
  Future<void> deleteAll() async {
    _ensureInitialized();
    await _storage.deleteAll();
    debugPrint('✅ All storage cleared');
  }

  /// Check if key exists
  Future<bool> containsKey(String key) async {
    _ensureInitialized();
    return await _storage.containsKey(key: key);
  }

  /// Get all keys
  Future<Map<String, String>> readAll() async {
    _ensureInitialized();
    return await _storage.readAll();
  }

  void _ensureInitialized() {
    if (!_isInitialized) {
      throw Exception('SecureStorageService not initialized');
    }
  }
}
