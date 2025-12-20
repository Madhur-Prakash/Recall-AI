# Recall AI Frontend

A modern Flutter desktop application for Recall AI with chat and voice input capabilities.

## Features

- 🎨 **Modern Dark UI** - Beautiful gradient-based design with smooth animations
- 💬 **Chat Interface** - Clean and intuitive chat experience
- 🎤 **Voice Input** - Speech-to-text functionality for hands-free interaction
- 🔄 **Dual Backend Support** - Switch between FAISS and Qdrant vector stores
- ⚡ **Real-time Streaming** - Live responses from the AI backend
- 🪟 **Windows Desktop** - Optimized for Windows desktop experience

## Prerequisites

- Flutter SDK (3.10.1 or higher)
- Windows 10/11
- Running Recall AI backend server (http://127.0.0.1:8000)

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend/recall_frontend
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Ensure the backend server is running:
   ```bash
   # From the backend directory
   uvicorn backend.app:app --reload
   ```

## Running the Application

### Development Mode
```bash
flutter run -d windows
```

### Build Release
```bash
flutter build windows --release
```

The executable will be located at:
```
build/windows/x64/runner/Release/recall_frontend.exe
```

## Usage

1. **Text Input**: Type your question in the input field and press Enter or click the send button
2. **Voice Input**: Click the microphone button to start voice recording, speak your question, and click again to stop
3. **Switch Backend**: Use the toggle switch in the app bar to switch between FAISS and Qdrant backends

## Configuration

To change the backend URL, edit `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'http://127.0.0.1:8000';
```

## Troubleshooting

### Speech Recognition Not Working
- Ensure microphone permissions are granted
- Check Windows microphone settings
- Restart the application

### Connection Error
- Verify the backend server is running
- Check if the backend URL is correct
- Ensure no firewall is blocking the connection

## Tech Stack

- **Flutter** - UI Framework
- **speech_to_text** - Voice input
- **flutter_animate** - Smooth animations
- **google_fonts** - Typography
- **http** - API communication

## License

MIT License - See main project LICENSE file
