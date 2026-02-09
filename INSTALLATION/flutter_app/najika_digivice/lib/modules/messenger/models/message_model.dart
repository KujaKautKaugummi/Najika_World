import '../../../core/constants/app_constants.dart';

/// Message model
class Message {
  String id;
  String senderId;
  String recipientId;
  String content;
  MessageType type;
  DateTime timestamp;
  bool isRead;
  bool isSent;

  // Disappearing messages
  int? disappearAfterSeconds;
  DateTime? disappearsAt;

  // Media (for images, videos, etc.)
  String? mediaUrl;
  String? thumbnailUrl;
  int? mediaSize;

  // Reactions
  List<MessageReaction>? reactions;

  // Reply
  String? replyToMessageId;

  Message({
    required this.id,
    required this.senderId,
    required this.recipientId,
    required this.content,
    required this.type,
    required this.timestamp,
    this.isRead = false,
    this.isSent = false,
    this.disappearAfterSeconds,
    this.disappearsAt,
    this.mediaUrl,
    this.thumbnailUrl,
    this.mediaSize,
    this.reactions,
    this.replyToMessageId,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'sender_id': senderId,
      'recipient_id': recipientId,
      'content': content,
      'type': type.toString(),
      'timestamp': timestamp.toIso8601String(),
      'is_read': isRead,
      'is_sent': isSent,
      'disappear_after_seconds': disappearAfterSeconds,
      'disappears_at': disappearsAt?.toIso8601String(),
      'media_url': mediaUrl,
      'thumbnail_url': thumbnailUrl,
      'media_size': mediaSize,
      'reactions': reactions?.map((r) => r.toJson()).toList(),
      'reply_to_message_id': replyToMessageId,
    };
  }

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      senderId: json['sender_id'],
      recipientId: json['recipient_id'],
      content: json['content'],
      type: MessageType.values.firstWhere(
        (e) => e.toString() == json['type'],
        orElse: () => MessageType.text,
      ),
      timestamp: DateTime.parse(json['timestamp']),
      isRead: json['is_read'] ?? false,
      isSent: json['is_sent'] ?? false,
      disappearAfterSeconds: json['disappear_after_seconds'],
      disappearsAt: json['disappears_at'] != null
          ? DateTime.parse(json['disappears_at'])
          : null,
      mediaUrl: json['media_url'],
      thumbnailUrl: json['thumbnail_url'],
      mediaSize: json['media_size'],
      reactions: json['reactions'] != null
          ? (json['reactions'] as List)
              .map((r) => MessageReaction.fromJson(r))
              .toList()
          : null,
      replyToMessageId: json['reply_to_message_id'],
    );
  }

  /// Check if message has disappeared
  bool get hasDisappeared {
    if (disappearsAt == null) return false;
    return DateTime.now().isAfter(disappearsAt!);
  }

  /// Get time until disappearing
  Duration? get timeUntilDisappears {
    if (disappearsAt == null) return null;
    return disappearsAt!.difference(DateTime.now());
  }
}

/// Message reaction (emoji)
class MessageReaction {
  final String emoji;
  final String userId;
  final DateTime timestamp;

  MessageReaction({
    required this.emoji,
    required this.userId,
    required this.timestamp,
  });

  Map<String, dynamic> toJson() {
    return {
      'emoji': emoji,
      'user_id': userId,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  factory MessageReaction.fromJson(Map<String, dynamic> json) {
    return MessageReaction(
      emoji: json['emoji'],
      userId: json['user_id'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}
