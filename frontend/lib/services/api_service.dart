import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000';
  
  static Stream<String> chatWithFAISS(String query) async* {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/chat?query=${Uri.encodeComponent(query)}'),
        headers: {'Accept': 'text/plain'},
      );
      
      if (response.statusCode == 200) {
        yield response.body;
      } else {
        yield 'Error: ${response.statusCode}';
      }
    } catch (e) {
      yield 'Connection error: $e';
    }
  }
  
  static Stream<String> chatWithQdrant(String query) async* {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/quad_chat?query=${Uri.encodeComponent(query)}'),
        headers: {'Accept': 'text/plain'},
      );
      
      if (response.statusCode == 200) {
        yield response.body;
      } else {
        yield 'Error: ${response.statusCode}';
      }
    } catch (e) {
      yield 'Connection error: $e';
    }
  }
}