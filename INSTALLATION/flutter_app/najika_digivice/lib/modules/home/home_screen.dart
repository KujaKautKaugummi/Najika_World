import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../messenger/ui/conversations_screen.dart';
import '../messenger/services/messenger_service.dart';
import '../../services/network/connection_manager.dart';
import '../../services/security/security_service.dart';

/// Home Screen
///
/// Main navigation hub
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const ConversationsScreen(),
    const ContactsScreen(),
    const SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.chat_bubble_outline),
            selectedIcon: Icon(Icons.chat_bubble),
            label: 'Messages',
          ),
          NavigationDestination(
            icon: Icon(Icons.people_outline),
            selectedIcon: Icon(Icons.people),
            label: 'Contacts',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: 'Settings',
          ),
        ],
      ),
    );
  }
}

/// Contacts Screen (Placeholder)
class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Contacts'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.people_outline,
              size: 80,
              color: Colors.grey[600],
            ),
            const SizedBox(height: 16),
            Text(
              'No contacts yet',
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () {
                // TODO: Add contact
              },
              icon: const Icon(Icons.person_add),
              label: const Text('Add Contact'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Settings Screen
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          // Account section
          _buildSectionHeader('Account'),
          ListTile(
            leading: const CircleAvatar(
              child: Icon(Icons.person),
            ),
            title: const Text('Profile'),
            subtitle: const Text('Edit your profile information'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              // TODO: Profile settings
            },
          ),

          const Divider(),

          // Security section
          _buildSectionHeader('Security'),
          Consumer<SecurityService>(
            builder: (context, security, child) {
              return Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.security),
                    title: const Text('Security Level'),
                    subtitle: Text(_getSecurityLevelText(security.securityLevel)),
                    trailing: Icon(
                      _getSecurityIcon(security.securityLevel),
                      color: _getSecurityColor(security.securityLevel),
                    ),
                  ),
                  if (security.isRooted)
                    ListTile(
                      leading: const Icon(Icons.warning, color: Colors.red),
                      title: const Text('Device Rooted', style: TextStyle(color: Colors.red)),
                      subtitle: const Text('This device is compromised'),
                    ),
                ],
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.fingerprint),
            title: const Text('Biometric Lock'),
            subtitle: const Text('Use fingerprint/face to unlock'),
            trailing: Switch(
              value: true, // TODO: Get from settings
              onChanged: (value) {
                // TODO: Toggle biometric
              },
            ),
          ),
          ListTile(
            leading: const Icon(Icons.lock),
            title: const Text('Change PINs'),
            subtitle: const Text('Unlock / Panic / Duress PINs'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              // TODO: Change PINs
            },
          ),
          ListTile(
            leading: const Icon(Icons.screenshot),
            title: const Text('Screenshot Protection'),
            subtitle: const Text('Notify sender on screenshot'),
            trailing: Switch(
              value: true,
              onChanged: (value) {
                // TODO: Toggle screenshot detection
              },
            ),
          ),

          const Divider(),

          // Connection section
          _buildSectionHeader('Connection'),
          Consumer<ConnectionManager>(
            builder: (context, connection, child) {
              return ListTile(
                leading: Icon(
                  connection.isConnected ? Icons.cloud_done : Icons.cloud_off,
                  color: connection.isConnected ? Colors.green : Colors.red,
                ),
                title: const Text('Connection Status'),
                subtitle: Text(connection.getConnectionStatusMessage()),
                trailing: Text(
                  '${connection.getConnectionQuality()}%',
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              );
            },
          ),

          const Divider(),

          // Messenger section
          _buildSectionHeader('Messenger'),
          ListTile(
            leading: const Icon(Icons.key),
            title: const Text('Encryption'),
            subtitle: const Text('Post-Quantum E2E Encryption'),
            trailing: const Icon(Icons.check_circle, color: Colors.green),
          ),
          ListTile(
            leading: const Icon(Icons.shield),
            title: const Text('Zero-Knowledge'),
            subtitle: const Text('Server never sees message content'),
            trailing: const Icon(Icons.check_circle, color: Colors.green),
          ),
          ListTile(
            leading: const Icon(Icons.location_off),
            title: const Text('GPS Disabled'),
            subtitle: const Text('No location tracking'),
            trailing: const Icon(Icons.check_circle, color: Colors.green),
          ),

          const Divider(),

          // Danger zone
          _buildSectionHeader('Danger Zone', color: Colors.red),
          ListTile(
            leading: const Icon(Icons.warning, color: Colors.red),
            title: const Text('Panic Button', style: TextStyle(color: Colors.red)),
            subtitle: const Text('Emergency wipe (IRREVERSIBLE)'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              _showPanicWarning(context);
            },
          ),

          const Divider(),

          // About section
          _buildSectionHeader('About'),
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: const Text('Version'),
            subtitle: const Text('1.0.0 (Post-Quantum)'),
          ),
          ListTile(
            leading: const Icon(Icons.bug_report_outlined),
            title: const Text('Report Issue'),
            onTap: () {
              // TODO: Report issue
            },
          ),

          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title, {Color? color}) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title.toUpperCase(),
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.bold,
          color: color ?? Colors.grey[600],
        ),
      ),
    );
  }

  String _getSecurityLevelText(SecurityLevel level) {
    switch (level) {
      case SecurityLevel.high:
        return 'High - All security features active';
      case SecurityLevel.medium:
        return 'Medium - Some warnings detected';
      case SecurityLevel.low:
        return 'Low - Multiple warnings';
      case SecurityLevel.compromised:
        return 'Compromised - Device rooted';
      case SecurityLevel.unknown:
        return 'Unknown';
    }
  }

  IconData _getSecurityIcon(SecurityLevel level) {
    switch (level) {
      case SecurityLevel.high:
        return Icons.security;
      case SecurityLevel.medium:
        return Icons.warning_amber;
      case SecurityLevel.low:
        return Icons.error_outline;
      case SecurityLevel.compromised:
        return Icons.dangerous;
      case SecurityLevel.unknown:
        return Icons.help_outline;
    }
  }

  Color _getSecurityColor(SecurityLevel level) {
    switch (level) {
      case SecurityLevel.high:
        return Colors.green;
      case SecurityLevel.medium:
        return Colors.orange;
      case SecurityLevel.low:
        return Colors.deepOrange;
      case SecurityLevel.compromised:
        return Colors.red;
      case SecurityLevel.unknown:
        return Colors.grey;
    }
  }

  void _showPanicWarning(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.warning, color: Colors.red),
            SizedBox(width: 8),
            Text('⚠️ PANIC BUTTON'),
          ],
        ),
        content: const Text(
          'The Panic Button will:\n\n'
          '• Wipe ALL local data\n'
          '• Delete server messages\n'
          '• Use 7-pass DOD secure delete\n\n'
          'This is IRREVERSIBLE!\n\n'
          'Use Panic PIN to trigger.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // TODO: Show panic PIN info
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Understood'),
          ),
        ],
      ),
    );
  }
}
