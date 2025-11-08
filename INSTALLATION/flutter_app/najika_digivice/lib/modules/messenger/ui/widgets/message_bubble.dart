import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../models/message_model.dart';

/// Message Bubble Widget
///
/// Displays a single message in the chat
class MessageBubble extends StatelessWidget {
  final Message message;
  final bool isMe;

  const MessageBubble({
    super.key,
    required this.message,
    required this.isMe,
  });

  @override
  Widget build(BuildContext context) {
    // Check if message has disappeared
    if (message.hasDisappeared) {
      return _buildDisappearedMessage(context);
    }

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: isMe ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (!isMe) _buildAvatar(),
          const SizedBox(width: 8),
          Flexible(
            child: Column(
              crossAxisAlignment: isMe ? CrossAxisAlignment.end : CrossAxisAlignment.start,
              children: [
                _buildMessageBubble(context),
                const SizedBox(height: 2),
                _buildMessageInfo(context),
              ],
            ),
          ),
          const SizedBox(width: 8),
          if (isMe) _buildAvatar(),
        ],
      ),
    );
  }

  Widget _buildAvatar() {
    return CircleAvatar(
      radius: 16,
      child: Text(
        isMe ? 'Me'[0] : 'U'[0],
        style: const TextStyle(fontSize: 12),
      ),
    );
  }

  Widget _buildMessageBubble(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: isMe
            ? Theme.of(context).colorScheme.primary
            : Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            offset: const Offset(0, 2),
            blurRadius: 4,
            color: Colors.black.withOpacity(0.1),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildMessageContent(context),
          if (message.disappearAfterSeconds != null)
            _buildDisappearTimer(context),
        ],
      ),
    );
  }

  Widget _buildMessageContent(BuildContext context) {
    switch (message.type) {
      case MessageType.text:
      case MessageType.disappearing:
        return Text(
          message.content,
          style: TextStyle(
            color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
          ),
        );

      case MessageType.image:
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (message.mediaUrl != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.network(
                  message.mediaUrl!,
                  width: 200,
                  fit: BoxFit.cover,
                ),
              ),
            if (message.content.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  message.content,
                  style: TextStyle(
                    color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
                  ),
                ),
              ),
          ],
        );

      case MessageType.video:
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                if (message.thumbnailUrl != null)
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      message.thumbnailUrl!,
                      width: 200,
                      fit: BoxFit.cover,
                    ),
                  ),
                Container(
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(0.5),
                    shape: BoxShape.circle,
                  ),
                  padding: const EdgeInsets.all(16),
                  child: const Icon(
                    Icons.play_arrow,
                    color: Colors.white,
                    size: 32,
                  ),
                ),
              ],
            ),
            if (message.content.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  message.content,
                  style: TextStyle(
                    color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
                  ),
                ),
              ),
          ],
        );

      case MessageType.audio:
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.play_circle_outline, size: 32),
            const SizedBox(width: 8),
            Text(
              _formatDuration(message.mediaSize ?? 0),
              style: TextStyle(
                color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
              ),
            ),
          ],
        );

      case MessageType.file:
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.insert_drive_file, size: 32),
            const SizedBox(width: 8),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  message.content,
                  style: TextStyle(
                    color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
                  ),
                ),
                Text(
                  _formatFileSize(message.mediaSize ?? 0),
                  style: TextStyle(
                    fontSize: 12,
                    color: isMe ? Colors.white70 : Colors.grey,
                  ),
                ),
              ],
            ),
          ],
        );

      case MessageType.voiceCall:
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.call, size: 16),
            const SizedBox(width: 8),
            Text(
              'Voice call',
              style: TextStyle(
                color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
                fontStyle: FontStyle.italic,
              ),
            ),
          ],
        );

      case MessageType.avatarCall:
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.videocam, size: 16),
            const SizedBox(width: 8),
            Text(
              'Avatar call',
              style: TextStyle(
                color: isMe ? Colors.white : Theme.of(context).textTheme.bodyLarge?.color,
                fontStyle: FontStyle.italic,
              ),
            ),
          ],
        );

      default:
        return Text(message.content);
    }
  }

  Widget _buildDisappearTimer(BuildContext context) {
    if (message.timeUntilDisappears == null) {
      return const SizedBox.shrink();
    }

    return Padding(
      padding: const EdgeInsets.only(top: 8),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.timer,
            size: 14,
            color: isMe ? Colors.white70 : Colors.grey,
          ),
          const SizedBox(width: 4),
          Text(
            _formatDuration(message.timeUntilDisappears!.inSeconds),
            style: TextStyle(
              fontSize: 12,
              color: isMe ? Colors.white70 : Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageInfo(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          DateFormat('HH:mm').format(message.timestamp),
          style: TextStyle(
            fontSize: 10,
            color: Colors.grey[600],
          ),
        ),
        if (isMe) ...[
          const SizedBox(width: 4),
          Icon(
            message.isRead
                ? Icons.done_all
                : message.isSent
                    ? Icons.done
                    : Icons.schedule,
            size: 14,
            color: message.isRead ? Colors.blue : Colors.grey[600],
          ),
        ],
      ],
    );
  }

  Widget _buildDisappearedMessage(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Center(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.grey.withOpacity(0.2),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.visibility_off, size: 14, color: Colors.grey),
              const SizedBox(width: 6),
              Text(
                'Message disappeared',
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey[600],
                  fontStyle: FontStyle.italic,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDuration(int seconds) {
    final duration = Duration(seconds: seconds);
    final minutes = duration.inMinutes;
    final secs = duration.inSeconds % 60;
    return '${minutes.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  String _formatFileSize(int bytes) {
    if (bytes < 1024) {
      return '$bytes B';
    } else if (bytes < 1024 * 1024) {
      return '${(bytes / 1024).toStringAsFixed(1)} KB';
    } else if (bytes < 1024 * 1024 * 1024) {
      return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
    } else {
      return '${(bytes / (1024 * 1024 * 1024)).toStringAsFixed(1)} GB';
    }
  }
}
