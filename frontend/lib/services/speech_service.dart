import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  static final stt.SpeechToText _speech = stt.SpeechToText();
  static bool _isInitialized = false;
  
  static Future<bool> initialize() async {
    try {
      if (!_isInitialized) {
        _isInitialized = await _speech.initialize(
          onError: (error) => print('Speech error: $error'),
          onStatus: (status) => print('Speech status: $status'),
          debugLogging: true,
        );
        print('Speech initialized: $_isInitialized');
        print('Speech available: ${_speech.isAvailable}');
      }
      return _isInitialized && _speech.isAvailable;
    } catch (e) {
      print('Speech initialization error: $e');
      return false;
    }
  }
  
  static bool get isListening => _speech.isListening;
  static bool get isAvailable => _speech.isAvailable;
  
  static Future<void> startListening({
    required Function(String) onResult,
    required Function(String) onError,
  }) async {
    try {
      if (!_isInitialized || !_speech.isAvailable) {
        final initialized = await initialize();
        if (!initialized) {
          onError('Speech recognition not available on this device');
          return;
        }
      }
      
      if (_speech.isListening) {
        await _speech.stop();
      }
      
      await _speech.listen(
        onResult: (result) {
          print('Speech result: ${result.recognizedWords}');
          if (result.recognizedWords.isNotEmpty) {
            onResult(result.recognizedWords);
          }
        },
        listenFor: const Duration(seconds: 10),
        pauseFor: const Duration(seconds: 2),
        partialResults: false,
        cancelOnError: true,
        listenMode: stt.ListenMode.confirmation,
      );
    } catch (e) {
      print('Start listening error: $e');
      onError('Error starting speech recognition: $e');
    }
  }
  
  static Future<void> stopListening() async {
    try {
      if (_speech.isListening) {
        await _speech.stop();
      }
    } catch (e) {
      print('Stop listening error: $e');
    }
  }
}