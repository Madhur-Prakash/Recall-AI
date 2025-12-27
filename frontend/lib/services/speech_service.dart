import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  static final stt.SpeechToText _speech = stt.SpeechToText();
  static bool _isInitialized = false;
  
  static Future<bool> initialize() async {
    if (!_isInitialized) {
      _isInitialized = await _speech.initialize(
        onError: (error) => print('Speech error: $error'),
        onStatus: (status) => print('Speech status: $status'),
      );
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
      final initialized = await initialize();
      if (!initialized) {
        onError('Failed to initialize speech recognition');
        return;
      }
    }
    
    if (_isInitialized && !_speech.isListening) {
      try {
        await _speech.listen(
          onResult: (result) {
            onResult(result.recognizedWords);
          },
          listenFor: const Duration(seconds: 10),
          pauseFor: const Duration(seconds: 2),
          partialResults: true,
          cancelOnError: true,
          listenMode: stt.ListenMode.confirmation,
        );
      } catch (e) {
        onError('Error starting speech recognition: $e');
      }
    }
  }
  
  static Future<void> stopListening() async {
    if (_speech.isListening) {
      await _speech.stop();
    }
  }
}