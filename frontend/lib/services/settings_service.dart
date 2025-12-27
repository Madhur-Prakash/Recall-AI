import 'package:shared_preferences/shared_preferences.dart';

import 'package:flutter/foundation.dart';
class SettingsService {
  static const String _voiceEnabledKey = 'voice_enabled';
  static const String _vectorStoreKey = 'vector_store';
  static const String _serverUrlKey = 'server_url';
  static const String _darkModeKey = 'dark_mode';

  static bool _voiceEnabled = true;
  static final ValueNotifier<String> vectorStoreNotifier = ValueNotifier<String>('FAISS');
  static String _serverUrl = 'http://127.0.0.1:8000';
  static final ValueNotifier<bool> darkModeNotifier = ValueNotifier<bool>(true);

  static bool get voiceEnabled => _voiceEnabled;
  static String get vectorStore => vectorStoreNotifier.value;
  static String get serverUrl => _serverUrl;
  static bool get darkMode => darkModeNotifier.value;
  
  static Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _voiceEnabled = prefs.getBool(_voiceEnabledKey) ?? true;
    vectorStoreNotifier.value = prefs.getString(_vectorStoreKey) ?? 'FAISS';
    _serverUrl = prefs.getString(_serverUrlKey) ?? 'http://127.0.0.1:8000';
    darkModeNotifier.value = prefs.getBool(_darkModeKey) ?? true;
  }
  
  static Future<void> setVoiceEnabled(bool enabled) async {
    _voiceEnabled = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_voiceEnabledKey, enabled);
  }
  
  static Future<void> setVectorStore(String store) async {
    vectorStoreNotifier.value = store;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_vectorStoreKey, store);
  }
  
  static Future<void> setServerUrl(String url) async {
    _serverUrl = url;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_serverUrlKey, url);
  }
  
  static Future<void> setDarkMode(bool dark) async {
    darkModeNotifier.value = dark;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_darkModeKey, dark);
  }
}