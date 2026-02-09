import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../services/messenger_service.dart';
import '../models/conversation_model.dart';
import './chat_screen.dart';

/// Conversations List Screen
///
/// Shows all active conversations
class ConversationsScreen extends StatelessWidget {
  const ConversationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Messages'),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () {
              // TODO: Implement search
            },
          ),
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () {
              // TODO: Show menu
            },
          ),
        ],
      ),
      body: Consumer<MessengerService>(
        builder: (context, messenger, child) {
          final conversations = messenger.conversations;

          if (conversations.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.chat_bubble_outline,
                    size: 80,
                    color: Colors.grey[600],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'No conversations yet',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.grey[600],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Start a new chat to begin',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[500],
                    ),
                  ),
                ],
              ),
            );
          }

          // Sort conversations (pinned first, then by last activity)
          conversations.sort((a, b) {
            if (a.isPinned && !b.isPinned) return -1;
            if (!a.isPinned && b.isPinned) return 1;

            final aTime = a.lastActivity ?? a.lastMessage?.timestamp ?? DateTime(2000);
            final bTime = b.lastActivity ?? b.lastMessage?.timestamp ?? DateTime(2000);
            return bTime.compareTo(aTime);
          });

          return ListView.builder(
            itemCount: conversations.length,
            itemBuilder: (context, index) {
              final conversation = conversations[index];
              return ConversationTile(conversation: conversation);
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Show new conversation dialog
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}

/// Conversation Tile Widget
class ConversationTile extends StatelessWidget {
  final Conversation conversation;

  const ConversationTile({
    super.key,
    required this.conversation,
  });

  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: Key(conversation.id),
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        child: const Icon(Icons.delete, color: Colors.white),
      ),
      direction: DismissDirection.endToStart,
      onDismissed: (direction) {
        // TODO: Delete conversation
      },
      child: ListTile(
        leading: Stack(
          children: [
            CircleAvatar(
              radius: 28,
              backgroundImage: conversation.contactAvatarUrl != null
                  ? NetworkImage(conversation.contactAvatarUrl!)
                  : null,
              child: conversation.contactAvatarUrl == null
                  ? Text(
                      conversation.contactName[0].toUpperCase(),
                      style: const TextStyle(fontSize: 24),
                    )
                  : null,
            ),
            if (conversation.unreadCount > 0)
              Positioned(
                right: 0,
                top: 0,
                child: Container(
                  padding: const EdgeInsets.all(4),
                  decoration: const BoxDecoration(
                    color: Colors.red,
                    shape: BoxShape.circle,
                  ),
                  child: Text(
                    conversation.unreadCount > 99
                        ? '99+'
                        : conversation.unreadCount.toString(),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
          ],
        ),
        title: Row(
          children: [
            if (conversation.isPinned)
              const Padding(
                padding: EdgeInsets.only(right: 4),
                child: Icon(Icons.push_pin, size: 14),
              ),
            if (conversation.isMuted)
              const Padding(
                padding: EdgeInsets.only(right: 4),
                child: Icon(Icons.volume_off, size: 14),
              ),
            Expanded(
              child: Text(
                conversation.contactName,
                style: TextStyle(
                  fontWeight: conversation.unreadCount > 0
                      ? FontWeight.bold
                      : FontWeight.normal,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        subtitle: Text(
          conversation.lastMessagePreview,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            color: conversation.unreadCount > 0
                ? Colors.white
                : Colors.grey[400],
          ),
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              conversation.timeSinceLastActivity,
              style: TextStyle(
                fontSize: 12,
                color: conversation.unreadCount > 0
                    ? Theme.of(context).colorScheme.primary
                    : Colors.grey[500],
              ),
            ),
            if (conversation.lastMessage?.disappearAfterSeconds != null)
              const Padding(
                padding: EdgeInsets.only(top: 4),
                child: Icon(Icons.timer, size: 14),
              ),
          ],
        ),
        onTap: () {
          // Open chat
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ChatScreen(
                conversation: conversation,
              ),
            ),
          );

          // Mark as read
          Provider.of<MessengerService>(context, listen: false)
              .markAsRead(conversation.id);
        },
        onLongPress: () {
          // Show conversation options
          _showConversationOptions(context);
        },
      ),
    );
  }

  void _showConversationOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            leading: Icon(conversation.isPinned ? Icons.push_pin_outlined : Icons.push_pin),
            title: Text(conversation.isPinned ? 'Unpin' : 'Pin'),
            onTap: () {
              // TODO: Toggle pin
              Navigator.pop(context);
            },
          ),
          ListTile(
            leading: Icon(conversation.isMuted ? Icons.volume_up : Icons.volume_off),
            title: Text(conversation.isMuted ? 'Unmute' : 'Mute'),
            onTap: () {
              // TODO: Toggle mute
              Navigator.pop(context);
            },
          ),
          ListTile(
            leading: const Icon(Icons.delete, color: Colors.red),
            title: const Text('Delete', style: TextStyle(color: Colors.red)),
            onTap: () {
              // TODO: Delete conversation
              Navigator.pop(context);
            },
          ),
        ],
      ),
    );
  }
}
