class Broadcast {
  final int id;
  final String title;
  final String message;
  final String status;
  final String createdAt;
  final String? sentAt;

  Broadcast({
    required this.id,
    required this.title,
    required this.message,
    required this.status,
    required this.createdAt,
    this.sentAt,
  });

  factory Broadcast.fromJson(Map<String, dynamic> json) {
    return Broadcast(
      id: json['id'],
      title: json['title'],
      message: json['message'],
      status: json['status'],
      createdAt: json['created_at'],
      sentAt: json['sent_at'],
    );
  }
}
