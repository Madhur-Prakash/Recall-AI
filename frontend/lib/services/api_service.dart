import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';
  
  static Stream<String> chatWithFAISS(String query) async* {
    try {
      final request = http.Request('GET', Uri.parse('$baseUrl/chat?query=${Uri.encodeComponent(query)}'));
      request.headers['Accept'] = 'text/plain';
      
      final response = await request.send();
      
      if (response.statusCode == 200) {
        await for (List<int> chunk in response.stream) {
          yield utf8.decode(chunk);
        }
      } else {
        yield 'Error: ${response.statusCode}';
      }
    } catch (e) {
      yield 'Connection error: $e';
    }
  }
  
  static Stream<String> chatWithQdrant(String query) async* {
    try {
      final request = http.Request('GET', Uri.parse('$baseUrl/quad_chat?query=${Uri.encodeComponent(query)}'));
      request.headers['Accept'] = 'text/plain';
      
      final response = await request.send();
      
      if (response.statusCode == 200) {
        await for (List<int> chunk in response.stream) {
          yield utf8.decode(chunk);
        }
      } else {
        yield 'Error: ${response.statusCode}';
      }
    } catch (e) {
      yield 'Connection error: $e';
    }
  }
}