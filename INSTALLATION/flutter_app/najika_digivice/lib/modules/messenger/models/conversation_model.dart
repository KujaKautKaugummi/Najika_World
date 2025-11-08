import './message_model.dart';

/// Conversation model
class Conversation {
  final String id;
  final String contactId;
  String contactName;
  String? contactAvatarUrl;
  Message? lastMessage;
  int unreadCount;
  bool isMuted;
  bool isPinned;
  DateTime? lastActivity;

  Conversation({
    required this.id,
    required this.contactId,
    required this.contactName,
    this.contactAvatarUrl,
    this.lastMessage,
    this.unreadCount = 0,
    this.isMuted = false,
    this.isPinned = false,
    this.lastActivity,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'contact_id': contactId,
      'contact_name': contactName,
      'contact_avatar_url': contactAvatarUrl,
      'last_message': lastMessage?.toJson(),
      'unread_count': unreadCount,
      'is_muted': isMuted,
      'is_pinned': isPinned,
      'last_activity': lastActivity?.toIso8601String(),
    };
  }

  factory Conversation.fromJson(Map<String, dynamic> json) {
    return Conversation(
      id: json['id'],
      contactId: json['contact_id'],
      contactName: json['contact_name'],
      contactAvatarUrl: json['contact_avatar_url'],
      lastMessage: json['last_message'] != null
          ? Message.fromJson(json['last_message'])
          : null,
      unreadCount: json['unread_count'] ?? 0,
      isMuted: json['is_muted'] ?? false,
      isPinned: json['is_pinned'] ?? false,
      lastActivity: json['last_activity'] != null
          ? DateTime.parse(json['last_activity'])
          : null,
    );
  }

  /// Get last message preview
  String get lastMessagePreview {
    if (lastMessage == null) return 'No messages yet';

    switch (lastMessage!.type) {
      case MessageType.text:
        return lastMessage!.content;
      case MessageType.image:
        return '📷 Image';
      case MessageType.video:
        return '🎥 Video';
      case MessageType.audio:
        return '🎵 Audio';
      case MessageType.file:
        return '📎 File';
      case MessageType.disappearing:
        return '⏱️ Disappearing message';
      case MessageType.voiceCall:
        return '📞 Voice call';
      case MessageType.avatarCall:
        return '👤 Avatar call';
      default:
        return 'Message';
    }
  }

  /// Get time since last activity
  String get timeSinceLastActivity {
    if (lastActivity == null && lastMessage == null) {
      return '';
    }

    final time = lastActivity ?? lastMessage!.timestamp;
    final now = DateTime.now();
    final difference = now.difference(time);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else if (difference.inDays == 1) {
      return 'Yesterday';
    } else if (difference.inDays < 7) {
      return '${difference.inDays}d ago';
    } else {
      return '${time.day}/${time.month}/${time.year}';
    }
  }
}

/// Contact model
class Contact {
  final String id;
  final String name;
  final String? username;
  final String? avatarUrl;
  final String? statusMessage;
  bool isOnline;
  DateTime? lastSeen;
  bool isBlocked;
  bool isFavorite;

  Contact({
    required this.id,
    required this.name,
    this.username,
    this.avatarUrl,
    this.statusMessage,
    this.isOnline = false,
    this.lastSeen,
    this.isBlocked = false,
    this.isFavorite = false,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'username': username,
      'avatar_url': avatarUrl,
      'status_message': statusMessage,
      'is_online': isOnline,
      'last_seen': lastSeen?.toIso8601String(),
      'is_blocked': isBlocked,
      'is_favorite': isFavorite,
    };
  }

  factory Contact.fromJson(Map<String, dynamic> json) {
    return Contact(
      id: json['id'],
      name: json['name'],
      username: json['username'],
      avatarUrl: json['avatar_url'],
      statusMessage: json['status_message'],
      isOnline: json['is_online'] ?? false,
      lastSeen: json['last_seen'] != null
          ? DateTime.parse(json['last_seen'])
          : null,
      isBlocked: json['is_blocked'] ?? false,
      isFavorite: json['is_favorite'] ?? false,
    );
  }

  /// Get status text
  String get statusText {
    if (isOnline) return 'Online';
    if (lastSeen == null) return 'Offline';

    final now = DateTime.now();
    final difference = now.difference(lastSeen!);

    if (difference.inMinutes < 5) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else {
      return '${difference.inDays}d ago';
    }
  }
}
