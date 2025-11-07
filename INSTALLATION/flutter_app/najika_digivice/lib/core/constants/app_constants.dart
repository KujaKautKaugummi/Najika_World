/// Application-wide constants
class AppConstants {
  // App Info
  static const String appName = 'Najika Digivice';
  static const String appVersion = '1.0.0';
  static const String appBuild = '1';

  // Server URLs (will be detected automatically)
  static const String localServerUrl = 'http://192.168.1.100:5000';
  static const String cloudflareServerUrl = 'https://najika.yourdomain.com';
  static const String messengerServerUrl = 'http://192.168.1.100:5001';

  // Security
  static const int maxLoginAttempts = 5;
  static const int lockoutDurationMinutes = 30;
  static const int sessionTimeoutMinutes = 30;
  static const int panicWipeDelaySeconds = 5;

  // Storage keys
  static const String userIdKey = 'user_id';
  static const String deviceIdKey = 'device_id';
  static const String authTokenKey = 'auth_token';
  static const String identityKeyKey = 'identity_key';
  static const String signedPreKeyKey = 'signed_prekey';

  // Crypto
  static const int aesKeySize = 256;
  static const int saltSize = 32;
  static const int ivSize = 16;
  static const int kyberPublicKeySize = 800;  // CRYSTALS-Kyber-512
  static const int kyberSecretKeySize = 1632;
  static const int kyberCiphertextSize = 768;

  // Message limits
  static const int maxMessageSize = 100000;  // 100 KB
  static const int maxAttachmentSize = 10485760;  // 10 MB
  static const int maxQueuedMessages = 1000;

  // UI
  static const Duration animationDuration = Duration(milliseconds: 300);
  static const Duration shortAnimationDuration = Duration(milliseconds: 150);

  // Panic PINs (defaults - user will set their own)
  static const String defaultUnlockPin = '1234';
  static const String defaultPanicPin = '4321';
  static const String defaultDuressPin = '0000';
}

/// Security levels
enum SecurityLevel {
  high,      // Full security enabled
  medium,    // Some features disabled
  low,       // Minimal security
  compromised // Device compromised
}

/// Connection types
enum ConnectionType {
  local,      // Same network
  cloudflare, // Via Cloudflare Tunnel
  tailscale,  // Via Tailscale VPN
  unknown     // Cannot determine
}

/// Message types
enum MessageType {
  text,
  image,
  video,
  audio,
  file,
  disappearing,  // Snapchat-style
  voiceCall,
  avatarCall
}

/// Panic modes
enum PanicMode {
  normal,    // Normal operation
  duress,    // Duress mode (fake data)
  panic      // Panic mode (wipe triggered)
}
