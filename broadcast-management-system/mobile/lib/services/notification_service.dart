import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';

class NotificationService extends ChangeNotifier {
  final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  List<Map<String, dynamic>> _notifications = [];

  List<Map<String, dynamic>> get notifications => _notifications;

  NotificationService() {
    _initializeNotifications();
  }

  Future<void> _initializeNotifications() async {
    try {
      // Request permission for iOS
      await _firebaseMessaging.requestPermission();

      // Get FCM token
      String? token = await _firebaseMessaging.getToken();
      if (kDebugMode) {
        print('FCM Token: $token');
      }

      // Handle foreground messages
      FirebaseMessaging.onMessage.listen((RemoteMessage message) {
        if (kDebugMode) {
          print('Received message: ${message.data}');
        }

        _addNotification(message);
        notifyListeners();
      });

      // Handle background messages
      FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
        if (kDebugMode) {
          print('Message opened: ${message.data}');
        }

        _addNotification(message);
        notifyListeners();
      });

      // Handle terminated state
      RemoteMessage? initialMessage =
          await _firebaseMessaging.getInitialMessage();
      if (initialMessage != null) {
        _addNotification(initialMessage);
        notifyListeners();
      }
    } catch (e) {
      if (kDebugMode) {
        print('Notification initialization error: $e');
      }
    }
  }

  void _addNotification(RemoteMessage message) {
    _notifications.insert(
      0,
      {
        'title': message.notification?.title ?? 'Broadcast',
        'message': message.notification?.body ?? '',
        'data': message.data,
        'timestamp': DateTime.now().toIso8601String(),
      },
    );
  }

  void clearNotifications() {
    _notifications.clear();
    notifyListeners();
  }
}
