import 'package:flutter/material.dart';
import 'settings_service.dart';

class ThemeService extends ChangeNotifier {
  static final ThemeService _instance = ThemeService._internal();
  factory ThemeService() => _instance;
  ThemeService._internal();

  bool get isDarkMode => SettingsService.darkMode;

  ThemeData get darkTheme => ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: const Color(0xFF000000),
    primaryColor: const Color(0xFF8B5CF6),
    colorScheme: const ColorScheme.dark(
      primary: Color(0xFF8B5CF6),
      secondary: Color(0xFFEC4899),
      surface: Color(0xFF1A0D2E),
      background: Color(0xFF000000),
    ),
  );

  ThemeData get lightTheme => ThemeData(
    brightness: Brightness.light,
    scaffoldBackgroundColor: Colors.white,
    primaryColor: const Color(0xFF8B5CF6),
    colorScheme: ColorScheme.light(
      primary: const Color(0xFF8B5CF6),
      secondary: const Color(0xFFEC4899),
      surface: Colors.grey[100]!,
      background: Colors.white,
    ),
  );

  ThemeData get currentTheme => isDarkMode ? darkTheme : lightTheme;

  List<Color> get backgroundGradient => isDarkMode
      ? [
          const Color(0xFF000000),
          const Color(0xFF1A0D2E),
          const Color(0xFF2D1B3D),
        ]
      : [
          Colors.white,
          Colors.grey[50]!,
          Colors.grey[100]!,
        ];

  Color get textColor => isDarkMode ? Colors.white : Colors.black;
  Color get cardColor => isDarkMode 
      ? Colors.black.withOpacity(0.2) 
      : Colors.white.withOpacity(0.8);
  Color get borderColor => isDarkMode 
      ? Colors.white.withOpacity(0.1) 
      : Colors.grey.withOpacity(0.3);

  Future<void> toggleTheme() async {
    await SettingsService.setDarkMode(!isDarkMode);
    notifyListeners();
  }
}