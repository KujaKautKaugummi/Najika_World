import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../services/security/security_service.dart';
import '../../services/network/connection_manager.dart';
import '../../modules/messenger/services/messenger_service.dart';
import '../home/home_screen.dart';

/// Security Check Screen
///
/// Runs security checks on app startup:
/// - Root/Jailbreak detection
/// - Device integrity
/// - Network connection
class SecurityCheckScreen extends StatefulWidget {
  const SecurityCheckScreen({super.key});

  @override
  State<SecurityCheckScreen> createState() => _SecurityCheckScreenState();
}

class _SecurityCheckScreenState extends State<SecurityCheckScreen> {
  bool _isChecking = true;
  String _statusMessage = 'Initializing security checks...';
  double _progress = 0.0;

  @override
  void initState() {
    super.initState();
    _runSecurityChecks();
  }

  Future<void> _runSecurityChecks() async {
    // Check 1: Device Security
    setState(() {
      _statusMessage = 'Checking device security...';
      _progress = 0.2;
    });
    await Future.delayed(const Duration(milliseconds: 500));

    final isCompromised = await SecurityService.instance.checkDeviceSecurity();
    if (isCompromised) {
      _showSecurityWarning();
      return;
    }

    // Check 2: Network Connection
    setState(() {
      _statusMessage = 'Establishing connection...';
      _progress = 0.5;
    });
    await Future.delayed(const Duration(milliseconds: 500));

    final connected = await ConnectionManager.instance.initialize();
    if (!connected) {
      _showConnectionError();
      return;
    }

    // Check 3: Server Info
    setState(() {
      _statusMessage = 'Verifying server...';
      _progress = 0.8;
    });
    await Future.delayed(const Duration(milliseconds: 500));

    final serverInfo = await ConnectionManager.instance.getServerInfo();
    if (serverInfo == null) {
      _showServerError();
      return;
    }

    // All checks passed
    setState(() {
      _statusMessage = 'Security checks complete ✓';
      _progress = 1.0;
      _isChecking = false;
    });

    // Initialize Messenger Service
    try {
      await Provider.of<MessengerService>(context, listen: false).initialize();
    } catch (e) {
      debugPrint('⚠️ Failed to initialize messenger: $e');
      // Continue anyway - can initialize later
    }

    // Navigate to main app
    await Future.delayed(const Duration(milliseconds: 500));
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const HomeScreen()),
      );
    }
  }

  void _showSecurityWarning() {
    setState(() {
      _isChecking = false;
      _statusMessage = 'Security Warning!';
    });

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('⚠️ Security Warning'),
        content: const Text(
          'Your device appears to be rooted or jailbroken.\n\n'
          'Najika cannot run on compromised devices for security reasons.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Exit'),
          ),
        ],
      ),
    );
  }

  void _showConnectionError() {
    setState(() {
      _isChecking = false;
      _statusMessage = 'Connection Failed';
    });

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('❌ Connection Error'),
        content: const Text(
          'Could not connect to Najika server.\n\n'
          'Please check:\n'
          '• WiFi/Mobile data is enabled\n'
          '• Server is running\n'
          '• Cloudflare Tunnel is active',
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _runSecurityChecks();
            },
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  void _showServerError() {
    setState(() {
      _isChecking = false;
      _statusMessage = 'Server Error';
    });

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('❌ Server Error'),
        content: const Text(
          'Server is not responding correctly.\n\n'
          'Please ensure the Najika server is running.',
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _runSecurityChecks();
            },
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Logo/Icon
              Icon(
                Icons.security,
                size: 80,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 32),

              // Title
              Text(
                'Najika Digivice',
                style: Theme.of(context).textTheme.displayMedium,
              ),
              const SizedBox(height: 8),

              Text(
                'Ultra-Secure Messenger',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 48),

              // Progress indicator
              if (_isChecking) ...[
                LinearProgressIndicator(
                  value: _progress,
                  backgroundColor: Colors.grey[800],
                ),
                const SizedBox(height: 16),
              ],

              // Status message
              Text(
                _statusMessage,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
