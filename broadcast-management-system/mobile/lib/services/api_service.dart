import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/user.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:5000/api';
  late SharedPreferences _prefs;

  ApiService() {
    _initPrefs();
  }

  void _initPrefs() async {
    _prefs = await SharedPreferences.getInstance();
  }

  String? get _token => _prefs.getString('access_token');

  Map<String, String> _getHeaders() {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (_token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    return headers;
  }

  Future<Map<String, dynamic>> signup(
    String username,
    String email,
    String password,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/signup'),
        headers: _getHeaders(),
        body: jsonEncode({
          'username': username,
          'email': email,
          'password': password,
        }),
      );

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        await _prefs.setString('access_token', data['access_token']);
        await _prefs.setString('user', jsonEncode(data['user']));
        return {'success': true, 'user': User.fromJson(data['user'])};
      } else {
        final error = jsonDecode(response.body);
        return {'success': false, 'error': error['error']};
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: $e'};
    }
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: _getHeaders(),
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _prefs.setString('access_token', data['access_token']);
        await _prefs.setString('user', jsonEncode(data['user']));
        return {'success': true, 'user': User.fromJson(data['user'])};
      } else {
        final error = jsonDecode(response.body);
        return {'success': false, 'error': error['error']};
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: $e'};
    }
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/auth/me'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'user': User.fromJson(data)};
      } else {
        return {'success': false, 'error': 'Failed to fetch user'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: $e'};
    }
  }

  Future<Map<String, dynamic>> getNotifications({
    int page = 1,
    int perPage = 10,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/broadcasts/notifications/all?page=$page&per_page=$perPage'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return {'success': true, 'data': data};
      } else {
        return {'success': false, 'error': 'Failed to fetch notifications'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Network error: $e'};
    }
  }

  Future<void> logout() async {
    try {
      await http.post(
        Uri.parse('$baseUrl/auth/logout'),
        headers: _getHeaders(),
      );
    } catch (e) {
      // Handle error
    }
    await _prefs.remove('access_token');
    await _prefs.remove('user');
  }

  Future<void> saveFcmToken(String fcmToken) async {
    await _prefs.setString('fcm_token', fcmToken);
  }

  String? getFcmToken() => _prefs.getString('fcm_token');

  bool get isLoggedIn => _token != null;
}
