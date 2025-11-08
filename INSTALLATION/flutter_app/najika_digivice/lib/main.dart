import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'core/constants/app_constants.dart';
import 'core/theme/app_theme.dart';
import 'services/security/security_service.dart';
import 'services/storage/secure_storage_service.dart';
import 'services/network/connection_manager.dart';
import 'services/database/database_service.dart';
import 'modules/security/security_check_screen.dart';
import 'modules/panic/panic_service.dart';
import 'modules/messenger/services/messenger_service.dart';
import 'modules/contacts/contact_service.dart';
import 'services/calls/voice_call_service.dart';

/// Najika Digivice - Main Entry Point
///
/// Security-first mobile app with:
/// - Post-Quantum Cryptography
/// - E2E Encrypted Messaging
/// - Panic Button
/// - Zero-Knowledge Architecture
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Lock orientation to portrait
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // Initialize Hive
  await Hive.initFlutter();

  // Initialize secure storage
  await SecureStorageService.instance.initialize();

  // Initialize security service
  await SecurityService.instance.initialize();

  // Initialize database (with master password from secure storage)
  // In production, this password is derived from user's PIN during first setup
  final dbPassword = await SecureStorageService.instance.read('db_master_password') ??
      'default-master-password-change-me';
  await DatabaseService.instance.initialize(dbPassword);

  // Check for root/jailbreak BEFORE starting app
  final isCompromised = await SecurityService.instance.checkDeviceSecurity();
  if (isCompromised) {
    runApp(const CompromisedDeviceApp());
    return;
  }

  // Run main app
  runApp(const NajikaDigiviceApp());
}

/// Main Application
class NajikaDigiviceApp extends StatelessWidget {
  const NajikaDigiviceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SecurityService.instance),
        ChangeNotifierProvider(create: (_) => ConnectionManager.instance),
        ChangeNotifierProvider(create: (_) => PanicService.instance),
        ChangeNotifierProvider(create: (_) => MessengerService.instance),
        ChangeNotifierProvider(create: (_) => ContactService.instance),
        ChangeNotifierProvider(create: (_) => VoiceCallService.instance),
      ],
      child: MaterialApp(
        title: AppConstants.appName,
        debugShowCheckedModeBanner: false,
        theme: AppTheme.darkTheme, // Gothic Lolita dark theme
        home: const SecurityCheckScreen(),
      ),
    );
  }
}

/// App shown when device is compromised (rooted/jailbroken)
class CompromisedDeviceApp extends StatelessWidget {
  const CompromisedDeviceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Security Warning',
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.security,
                  color: Colors.red,
                  size: 80,
                ),
                const SizedBox(height: 32),
                const Text(
                  '⚠️ Security Warning',
                  style: TextStyle(
                    color: Colors.red,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'This device appears to be rooted/jailbroken.\n\n'
                  'Najika cannot run on compromised devices '
                  'for security reasons.',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 32),
                ElevatedButton(
                  onPressed: () => SystemNavigator.pop(),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                  ),
                  child: const Text('Exit'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
