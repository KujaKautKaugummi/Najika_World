import 'package:flutter/foundation.dart';
import 'package:safe_device/safe_device.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:screenshot_callback/screenshot_callback.dart';
import 'package:local_auth/local_auth.dart';

/// Security Service
///
/// Handles all security checks:
/// - Root/Jailbreak detection
/// - Screenshot detection
/// - Biometric authentication
/// - Device integrity
class SecurityService {
  static final SecurityService instance = SecurityService._();
  SecurityService._();

  // State
  bool _isInitialized = false;
  bool _isRooted = false;
  bool _isDevelopmentMode = false;
  bool _isEmulator = false;
  SecurityLevel _securityLevel = SecurityLevel.high;

  // Screenshot detection
  final _screenshotCallback = ScreenshotCallback();
  final List<Function(String)> _screenshotListeners = [];

  // Biometric auth
  final LocalAuthentication _localAuth = LocalAuthentication();

  // Getters
  bool get isInitialized => _isInitialized;
  bool get isRooted => _isRooted;
  bool get isDevelopmentMode => _isDevelopmentMode;
  bool get isEmulator => _isEmulator;
  SecurityLevel get securityLevel => _securityLevel;

  /// Initialize security service
  Future<void> initialize() async {
    debugPrint('🔒 SecurityService: Initializing...');

    // Check device security
    await checkDeviceSecurity();

    // Start screenshot monitoring
    _initializeScreenshotDetection();

    _isInitialized = true;
    debugPrint('✅ SecurityService: Initialized');
  }

  /// Check device security
  ///
  /// Returns true if device is compromised
  Future<bool> checkDeviceSecurity() async {
    debugPrint('🔍 Checking device security...');

    try {
      // Check if device is rooted/jailbroken
      _isRooted = await SafeDevice.isJailBroken;

      // Check if running in development mode
      _isDevelopmentMode = await SafeDevice.isDevelopmentModeEnable;

      // Check if running on emulator
      _isEmulator = await SafeDevice.isRealDevice == false;

      // Determine security level
      if (_isRooted) {
        _securityLevel = SecurityLevel.compromised;
        debugPrint('❌ Device is ROOTED/JAILBROKEN');
      } else if (_isDevelopmentMode || _isEmulator) {
        _securityLevel = SecurityLevel.low;
        debugPrint('⚠️ Device is in DEVELOPMENT MODE or EMULATOR');
      } else {
        _securityLevel = SecurityLevel.high;
        debugPrint('✅ Device security: OK');
      }

      return _isRooted; // Return true if compromised
    } catch (e) {
      debugPrint('⚠️ Security check error: $e');
      _securityLevel = SecurityLevel.unknown;
      return false;
    }
  }

  /// Initialize screenshot detection
  void _initializeScreenshotDetection() {
    _screenshotCallback.addListener(() {
      debugPrint('📸 Screenshot detected!');

      // Notify all listeners
      for (final listener in _screenshotListeners) {
        listener('Screenshot detected at ${DateTime.now()}');
      }
    });
  }

  /// Add screenshot listener
  ///
  /// Callback receives timestamp of screenshot
  void addScreenshotListener(Function(String) callback) {
    _screenshotListeners.add(callback);
  }

  /// Remove screenshot listener
  void removeScreenshotListener(Function(String) callback) {
    _screenshotListeners.remove(callback);
  }

  /// Check if biometric authentication is available
  Future<bool> canAuthenticateWithBiometrics() async {
    try {
      return await _localAuth.canCheckBiometrics &&
          await _localAuth.isDeviceSupported();
    } catch (e) {
      debugPrint('❌ Biometric check error: $e');
      return false;
    }
  }

  /// Get available biometric types
  Future<List<BiometricType>> getAvailableBiometrics() async {
    try {
      return await _localAuth.getAvailableBiometrics();
    } catch (e) {
      debugPrint('❌ Get biometrics error: $e');
      return [];
    }
  }

  /// Authenticate with biometrics
  Future<bool> authenticateWithBiometrics({
    String localizedReason = 'Authenticate to access Najika',
  }) async {
    try {
      return await _localAuth.authenticate(
        localizedReason: localizedReason,
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
    } catch (e) {
      debugPrint('❌ Biometric authentication error: $e');
      return false;
    }
  }

  /// Get device info
  Future<Map<String, dynamic>> getDeviceInfo() async {
    final deviceInfo = DeviceInfoPlugin();

    if (defaultTargetPlatform == TargetPlatform.android) {
      final androidInfo = await deviceInfo.androidInfo;
      return {
        'platform': 'android',
        'model': androidInfo.model,
        'manufacturer': androidInfo.manufacturer,
        'version': androidInfo.version.release,
        'sdk': androidInfo.version.sdkInt,
        'device': androidInfo.device,
        'isPhysicalDevice': androidInfo.isPhysicalDevice,
      };
    } else if (defaultTargetPlatform == TargetPlatform.iOS) {
      final iosInfo = await deviceInfo.iosInfo;
      return {
        'platform': 'ios',
        'model': iosInfo.model,
        'systemName': iosInfo.systemName,
        'systemVersion': iosInfo.systemVersion,
        'name': iosInfo.name,
        'isPhysicalDevice': iosInfo.isPhysicalDevice,
      };
    }

    return {'platform': 'unknown'};
  }

  /// Check if device meets security requirements
  bool meetsSecurityRequirements() {
    // Device must not be rooted/jailbroken
    if (_isRooted) return false;

    // Allow emulator only in debug mode
    if (_isEmulator && kReleaseMode) return false;

    return true;
  }

  /// Get security warnings
  List<String> getSecurityWarnings() {
    final warnings = <String>[];

    if (_isRooted) {
      warnings.add('Device is rooted/jailbroken');
    }

    if (_isDevelopmentMode) {
      warnings.add('Development mode is enabled');
    }

    if (_isEmulator) {
      warnings.add('Running on emulator');
    }

    return warnings;
  }

  /// Dispose resources
  void dispose() {
    _screenshotCallback.dispose();
    _screenshotListeners.clear();
  }
}

/// Security level enum
enum SecurityLevel {
  high,        // Full security
  medium,      // Some warnings
  low,         // Multiple warnings
  compromised, // Device rooted
  unknown      // Cannot determine
}
