import 'package:flutter/foundation.dart';
import 'package:dio/dio.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

import '../../core/constants/app_constants.dart';

/// Connection Manager
///
/// Automatically detects best connection method:
/// 1. Local (same network) - Fastest
/// 2. Tailscale (mesh VPN) - Fast + Secure
/// 3. Cloudflare Tunnel - Remote access
///
/// Works WITH ExpressVPN active!
class ConnectionManager extends ChangeNotifier {
  static final ConnectionManager instance = ConnectionManager._();
  ConnectionManager._();

  // Connection state
  ConnectionType _connectionType = ConnectionType.unknown;
  String? _activeServerUrl;
  String? _activeMessengerUrl;
  bool _isConnected = false;
  DateTime? _lastCheck;

  // Getters
  ConnectionType get connectionType => _connectionType;
  String? get activeServerUrl => _activeServerUrl;
  String? get activeMessengerUrl => _activeMessengerUrl;
  bool get isConnected => _isConnected;

  // HTTP client with timeout
  final _dio = Dio(BaseOptions(
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 5),
  ));

  /// Initialize connection
  ///
  /// Tries all connection methods in order of preference
  Future<bool> initialize() async {
    debugPrint('🔄 ConnectionManager: Initializing...');

    // 1. Try local connection first (fastest)
    if (await _tryLocal()) {
      _connectionType = ConnectionType.local;
      _activeServerUrl = AppConstants.localServerUrl;
      _activeMessengerUrl = AppConstants.messengerServerUrl;
      _isConnected = true;
      _lastCheck = DateTime.now();
      debugPrint('✅ ConnectionManager: Local connection established');
      notifyListeners();
      return true;
    }

    // 2. Try Tailscale (if available)
    if (await _tryTailscale()) {
      _connectionType = ConnectionType.tailscale;
      _isConnected = true;
      _lastCheck = DateTime.now();
      debugPrint('✅ ConnectionManager: Tailscale connection established');
      notifyListeners();
      return true;
    }

    // 3. Fallback to Cloudflare Tunnel
    if (await _tryCloudflare()) {
      _connectionType = ConnectionType.cloudflare;
      _activeServerUrl = AppConstants.cloudflareServerUrl;
      _activeMessengerUrl = AppConstants.cloudflareServerUrl.replaceFirst(
        'najika.',
        'messenger.najika.',
      );
      _isConnected = true;
      _lastCheck = DateTime.now();
      debugPrint('✅ ConnectionManager: Cloudflare connection established');
      notifyListeners();
      return true;
    }

    // No connection available
    _isConnected = false;
    debugPrint('❌ ConnectionManager: No connection available');
    notifyListeners();
    return false;
  }

  /// Try local connection
  ///
  /// Checks if server is on same network
  Future<bool> _tryLocal() async {
    debugPrint('🔍 Trying local connection...');

    try {
      final response = await _dio.get(
        '${AppConstants.localServerUrl}/api/mobile/health',
      );

      if (response.statusCode == 200) {
        debugPrint('✅ Local server responding');
        return true;
      }
    } catch (e) {
      debugPrint('❌ Local connection failed: $e');
    }

    return false;
  }

  /// Try Tailscale connection
  ///
  /// Checks if server is accessible via Tailscale
  Future<bool> _tryTailscale() async {
    debugPrint('🔍 Trying Tailscale connection...');

    // Tailscale uses 100.x.x.x IP range
    // We need to query the Tailscale API or local config for server IP
    // For now, skip if not configured

    // TODO: Implement Tailscale IP detection
    // This would query:
    // - Local Tailscale daemon (if available on mobile)
    // - Or use pre-configured Tailscale IP

    return false; // Skip for now
  }

  /// Try Cloudflare Tunnel
  ///
  /// Checks if Cloudflare Tunnel is accessible
  Future<bool> _tryCloudflare() async {
    debugPrint('🔍 Trying Cloudflare connection...');

    try {
      final response = await _dio.get(
        '${AppConstants.cloudflareServerUrl}/api/mobile/health',
      );

      if (response.statusCode == 200) {
        debugPrint('✅ Cloudflare server responding');
        return true;
      }
    } catch (e) {
      debugPrint('❌ Cloudflare connection failed: $e');
    }

    return false;
  }

  /// Check if connection is still alive
  ///
  /// Should be called periodically
  Future<bool> checkConnection() async {
    if (_activeServerUrl == null) {
      return false;
    }

    try {
      final response = await _dio.get(
        '$_activeServerUrl/api/mobile/health',
      );

      if (response.statusCode == 200) {
        _isConnected = true;
        _lastCheck = DateTime.now();
        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('⚠️ Connection check failed: $e');
    }

    _isConnected = false;
    notifyListeners();
    return false;
  }

  /// Reconnect if connection lost
  ///
  /// Tries to re-establish connection
  Future<bool> reconnect() async {
    debugPrint('🔄 Attempting to reconnect...');
    return await initialize();
  }

  /// Get server info
  ///
  /// Fetches server capabilities and version
  Future<Map<String, dynamic>?> getServerInfo() async {
    if (_activeServerUrl == null) {
      return null;
    }

    try {
      final response = await _dio.get(
        '$_activeServerUrl/api/mobile/server/info',
      );

      if (response.statusCode == 200) {
        return response.data as Map<String, dynamic>;
      }
    } catch (e) {
      debugPrint('❌ Failed to get server info: $e');
    }

    return null;
  }

  /// Create configured Dio instance for API calls
  ///
  /// Returns Dio with correct base URL and timeouts
  Dio createApiClient() {
    return Dio(BaseOptions(
      baseUrl: _activeServerUrl ?? AppConstants.cloudflareServerUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Najika-Digivice/${AppConstants.appVersion}',
      },
    ));
  }

  /// Create configured Dio instance for messenger API
  Dio createMessengerClient() {
    return Dio(BaseOptions(
      baseUrl: _activeMessengerUrl ?? AppConstants.messengerServerUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Najika-Digivice/${AppConstants.appVersion}',
      },
    ));
  }

  /// Monitor network changes
  ///
  /// Automatically reconnect when network changes
  void startNetworkMonitoring() {
    Connectivity().onConnectivityChanged.listen((result) async {
      debugPrint('🔄 Network change detected: $result');

      // Wait a moment for network to stabilize
      await Future.delayed(const Duration(seconds: 2));

      // Try to reconnect
      await reconnect();
    });
  }

  /// Get connection status message
  String getConnectionStatusMessage() {
    if (!_isConnected) {
      return '❌ Not connected';
    }

    switch (_connectionType) {
      case ConnectionType.local:
        return '✅ Local (Fast)';
      case ConnectionType.tailscale:
        return '✅ Tailscale (Secure)';
      case ConnectionType.cloudflare:
        return '✅ Cloudflare (Remote)';
      case ConnectionType.unknown:
        return '⚠️ Unknown';
    }
  }

  /// Get connection quality estimate
  ///
  /// Returns 0-100 score
  int getConnectionQuality() {
    if (!_isConnected) return 0;

    switch (_connectionType) {
      case ConnectionType.local:
        return 100; // Fastest
      case ConnectionType.tailscale:
        return 80; // Fast + secure
      case ConnectionType.cloudflare:
        return 60; // Remote but stable
      case ConnectionType.unknown:
        return 0;
    }
  }
}

/// Network status widget mixin
///
/// Provides automatic reconnection and status updates
mixin NetworkStatusMixin {
  void initializeNetworkStatus() {
    ConnectionManager.instance.startNetworkMonitoring();
  }

  Future<bool> ensureConnected() async {
    if (!ConnectionManager.instance.isConnected) {
      return await ConnectionManager.instance.reconnect();
    }
    return true;
  }

  String getNetworkStatusText() {
    return ConnectionManager.instance.getConnectionStatusMessage();
  }
}
