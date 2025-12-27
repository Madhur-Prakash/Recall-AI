import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'services/settings_service.dart';
import 'services/theme_service.dart';
import 'screens/splash_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SettingsService.init();
  runApp(const RecallAIApp());
}

class RecallAIApp extends StatelessWidget {
  const RecallAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: ThemeService(),
      builder: (context, child) {
        return MaterialApp(
          title: 'Recall AI',
          debugShowCheckedModeBanner: false,
          theme: ThemeService().currentTheme,
          home: const SplashScreen(),
        );
      },
    );
  }
}