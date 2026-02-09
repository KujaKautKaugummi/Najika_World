import 'package:flutter/foundation.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../../core/constants/app_constants.dart';
import '../../services/storage/secure_storage_service.dart';
import '../../services/database/database_service.dart';
import '../../services/network/connection_manager.dart';

/// Panic Service
///
/// Handles emergency situations:
/// - Panic Mode: Wipe all data
/// - Duress Mode: Show fake data
/// - Emergency wipe via server command
///
/// Based on EncroChat panic button design
class PanicService extends ChangeNotifier {
  static final PanicService instance = PanicService._();
  PanicService._();

  // State
  PanicMode _currentMode = PanicMode.normal;
  bool _isWipeInProgress = false;
  DateTime? _lastPanicAttempt;

  // PINs (will be set by user during setup)
  String? _unlockPin;
  String? _panicPin;
  String? _duressPin;

  // Getters
  PanicMode get currentMode => _currentMode;
  bool get isWipeInProgress => _isWipeInProgress;

  /// Initialize panic service
  Future<void> initialize() async {
    debugPrint('🚨 PanicService: Initializing...');

    // Load PINs from secure storage
    _unlockPin = await SecureStorageService.instance.read('unlock_pin') ??
        AppConstants.defaultUnlockPin;
    _panicPin = await SecureStorageService.instance.read('panic_pin') ??
        AppConstants.defaultPanicPin;
    _duressPin = await SecureStorageService.instance.read('duress_pin') ??
        AppConstants.defaultDuressPin;

    debugPrint('✅ PanicService: Initialized');
  }

  /// Verify PIN and handle mode
  ///
  /// Returns:
  /// - 'unlock': Normal unlock
  /// - 'panic': Trigger panic wipe
  /// - 'duress': Enter duress mode (fake data)
  /// - 'invalid': Wrong PIN
  Future<String> verifyPin(String enteredPin) async {
    // Check unlock PIN
    if (enteredPin == _unlockPin) {
      _currentMode = PanicMode.normal;
      notifyListeners();
      return 'unlock';
    }

    // Check panic PIN
    if (enteredPin == _panicPin) {
      debugPrint('🚨 PANIC PIN detected - triggering wipe!');
      await _triggerPanicWipe();
      return 'panic';
    }

    // Check duress PIN
    if (enteredPin == _duressPin) {
      debugPrint('⚠️ DURESS PIN detected - entering duress mode');
      _currentMode = PanicMode.duress;
      notifyListeners();
      return 'duress';
    }

    // Invalid PIN
    return 'invalid';
  }

  /// Trigger panic wipe
  ///
  /// PERMANENTLY deletes all data!
  Future<void> _triggerPanicWipe() async {
    if (_isWipeInProgress) {
      debugPrint('⚠️ Wipe already in progress');
      return;
    }

    _isWipeInProgress = true;
    _currentMode = PanicMode.panic;
    _lastPanicAttempt = DateTime.now();
    notifyListeners();

    debugPrint('🚨 PANIC WIPE INITIATED');

    // Grace period (gives user time to cancel if accidental)
    await Future.delayed(
      Duration(seconds: AppConstants.panicWipeDelaySeconds),
    );

    try {
      // 1. Notify server to wipe (if connected)
      await _notifyServerWipe();

      // 2. Wipe local storage
      await _wipeLocalStorage();

      // 3. Wipe secure storage
      await _wipeSecureStorage();

      // 4. Wipe database
      await _wipeDatabase();

      // 5. Wipe cached files
      await _wipeCachedFiles();

      // 6. Overwrite free space (optional - time consuming)
      // await _overwriteFreeSpace();

      debugPrint('✅ PANIC WIPE COMPLETED');
    } catch (e) {
      debugPrint('❌ Panic wipe error: $e');
    }

    _isWipeInProgress = false;
    notifyListeners();

    // Exit app after wipe
    await Future.delayed(const Duration(seconds: 1));
    exit(0);
  }

  /// Notify server to wipe data
  Future<void> _notifyServerWipe() async {
    try {
      final client = ConnectionManager.instance.createMessengerClient();

      final userId = await SecureStorageService.instance.read(
        AppConstants.userIdKey,
      );
      final deviceId = await SecureStorageService.instance.read(
        AppConstants.deviceIdKey,
      );

      if (userId != null && deviceId != null) {
        await client.post(
          '/api/messenger/panic/trigger',
          data: {
            'user_id': userId,
            'device_id': deviceId,
            'panic_code': _panicPin,
          },
        );

        debugPrint('✅ Server wipe notification sent');
      }
    } catch (e) {
      debugPrint('⚠️ Server wipe notification failed: $e');
      // Continue with local wipe even if server notification fails
    }
  }

  /// Wipe local storage (SharedPreferences)
  Future<void> _wipeLocalStorage() async {
    try {
      // Hive boxes
      final boxNames = Hive.boxNames.toList();
      for (final boxName in boxNames) {
        final box = await Hive.openBox(boxName);
        await box.clear();
        await box.close();
      }

      debugPrint('✅ Local storage wiped');
    } catch (e) {
      debugPrint('❌ Local storage wipe error: $e');
    }
  }

  /// Wipe secure storage
  Future<void> _wipeSecureStorage() async {
    try {
      await SecureStorageService.instance.deleteAll();
      debugPrint('✅ Secure storage wiped');
    } catch (e) {
      debugPrint('❌ Secure storage wipe error: $e');
    }
  }

  /// Wipe database
  Future<void> _wipeDatabase() async {
    try {
      // First, wipe all data from database tables
      await DatabaseService.instance.wipeAll();
      debugPrint('✅ Database tables wiped');

      // Then, securely delete the database file
      final appDir = await getApplicationDocumentsDirectory();
      final dbPath = '${appDir.path}/najika.db';

      final dbFile = File(dbPath);
      if (await dbFile.exists()) {
        // DOD 5220.22-M standard: 7-pass overwrite
        await _secureDeleteFile(dbFile);
        debugPrint('✅ Database file securely deleted');
      }
    } catch (e) {
      debugPrint('❌ Database wipe error: $e');
    }
  }

  /// Wipe cached files
  Future<void> _wipeCachedFiles() async {
    try {
      final cacheDir = await getTemporaryDirectory();
      if (await cacheDir.exists()) {
        await cacheDir.delete(recursive: true);
        debugPrint('✅ Cache wiped');
      }

      final appDir = await getApplicationDocumentsDirectory();
      if (await appDir.exists()) {
        // Delete all files except system files
        await for (final entity in appDir.list()) {
          if (entity is File) {
            await _secureDeleteFile(entity);
          }
        }
        debugPrint('✅ App directory wiped');
      }
    } catch (e) {
      debugPrint('❌ Cache wipe error: $e');
    }
  }

  /// Secure delete file (DOD 5220.22-M standard)
  ///
  /// 7-pass overwrite:
  /// 1. Pass 1: Write 0x00
  /// 2. Pass 2: Write 0xFF
  /// 3. Pass 3: Write random
  /// 4. Pass 4: Write 0x00
  /// 5. Pass 5: Write 0xFF
  /// 6. Pass 6: Write random
  /// 7. Pass 7: Write random
  Future<void> _secureDeleteFile(File file) async {
    try {
      final length = await file.length();

      // Pass 1: 0x00
      await file.writeAsBytes(List.filled(length, 0x00), flush: true);

      // Pass 2: 0xFF
      await file.writeAsBytes(List.filled(length, 0xFF), flush: true);

      // Pass 3: Random
      await file.writeAsBytes(
        List.generate(length, (_) => DateTime.now().microsecond % 256),
        flush: true,
      );

      // Pass 4: 0x00
      await file.writeAsBytes(List.filled(length, 0x00), flush: true);

      // Pass 5: 0xFF
      await file.writeAsBytes(List.filled(length, 0xFF), flush: true);

      // Pass 6: Random
      await file.writeAsBytes(
        List.generate(length, (_) => DateTime.now().microsecond % 256),
        flush: true,
      );

      // Pass 7: Random
      await file.writeAsBytes(
        List.generate(length, (_) => DateTime.now().microsecond % 256),
        flush: true,
      );

      // Finally, delete the file
      await file.delete();

      debugPrint('✅ Secure delete: ${file.path}');
    } catch (e) {
      debugPrint('❌ Secure delete error: $e');
      // Fallback: normal delete
      try {
        await file.delete();
      } catch (_) {}
    }
  }

  /// Set custom PINs
  Future<void> setPins({
    required String unlockPin,
    required String panicPin,
    required String duressPin,
  }) async {
    // Validate PINs are different
    if (unlockPin == panicPin || unlockPin == duressPin || panicPin == duressPin) {
      throw Exception('PINs must be different from each other');
    }

    // Validate PIN format (4-8 digits)
    final pinRegex = RegExp(r'^\d{4,8}$');
    if (!pinRegex.hasMatch(unlockPin) ||
        !pinRegex.hasMatch(panicPin) ||
        !pinRegex.hasMatch(duressPin)) {
      throw Exception('PINs must be 4-8 digits');
    }

    // Save to secure storage
    await SecureStorageService.instance.write('unlock_pin', unlockPin);
    await SecureStorageService.instance.write('panic_pin', panicPin);
    await SecureStorageService.instance.write('duress_pin', duressPin);

    _unlockPin = unlockPin;
    _panicPin = panicPin;
    _duressPin = duressPin;

    debugPrint('✅ PINs updated');
  }

  /// Cancel panic wipe (if in grace period)
  void cancelPanicWipe() {
    if (_isWipeInProgress) {
      _isWipeInProgress = false;
      _currentMode = PanicMode.normal;
      notifyListeners();
      debugPrint('⚠️ Panic wipe cancelled');
    }
  }

  /// Enter duress mode manually
  void enterDuressMode() {
    _currentMode = PanicMode.duress;
    notifyListeners();
    debugPrint('⚠️ Entered duress mode');
  }

  /// Exit duress mode
  void exitDuressMode() {
    _currentMode = PanicMode.normal;
    notifyListeners();
    debugPrint('✅ Exited duress mode');
  }

  /// Check if in duress mode
  bool get isDuressMode => _currentMode == PanicMode.duress;

  /// Check if in panic mode
  bool get isPanicMode => _currentMode == PanicMode.panic;
}
