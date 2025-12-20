import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  static final stt.SpeechToText _speech = stt.SpeechToText();
  static bool _isInitialized = false;
  
  static Future<bool> initialize() async {
    if (!_isInitialized) {
      _isInitialized = await _speech.initialize();
    }
    return _isInitialized;
  }
  
  static bool get isListening => _speech.isListening;
  static bool get isAvailable => _speech.isAvailable;
  
  static Future<void> startListening({
    required Function(String) onResult,
    required Function(String) onError,
  }) async {
    if (!_isInitialized) {
      await initialize();
    }
    
    if (_isInitialized && !_speech.isListening) {
      await _speech.listen(
        onResult: (result) => onResult(result.recognizedWords),
        onSoundLevelChange: (level) {},
        cancelOnError: true,
        partialResults: true,
        listenMode: stt.ListenMode.confirmation,
      );
    }
  }
  
  static Future<void> stopListening() async {
    if (_speech.isListening) {
      await _speech.stop();
    }
  }
}