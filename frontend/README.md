# Recall AI Frontend

A beautiful Flutter desktop application for Recall AI with modern UI, chat interface, and voice input capabilities.

## ✨ Features

- 🎨 **Beautiful Modern UI** - Gradient-based design with smooth animations
- 🌟 **Splash Screen** - Animated startup with gradient "RecallAI" text
- 💬 **Enhanced Chat Interface** - Clean bubbles with gradient backgrounds
- 🎤 **Fixed Voice Input** - Proper speech-to-text with permission handling
- 🔄 **Dual Backend Support** - Toggle between FAISS and Qdrant
- ⚡ **Real-time Streaming** - Live AI responses
- 🪟 **Windows Desktop** - Optimized for Windows
- 🎭 **Rich Animations** - Fade-ins, slides, pulses, and loading effects

## 🚀 Quick Start

### Development Mode
```bash
# Double-click or run:
run_dev.bat
```

### Build & Run Release
```bash
# Double-click or run:
build_and_run.bat
```

## 📋 Prerequisites

- Flutter SDK (3.10.1+)
- Windows 10/11
- Microphone access for voice input
- Running backend server at http://127.0.0.1:8000

## 🎯 Usage

1. **Splash Screen** - Beautiful animated startup (3 seconds)
2. **Text Chat** - Type questions and get AI responses
3. **Voice Input** - Click mic button, speak, and get automatic responses
4. **Backend Toggle** - Switch between FAISS/Qdrant in the top bar

## 🎨 UI Highlights

- **Gradient Text** - "RecallAI" with purple-violet-pink gradient
- **Animated Loading** - Pulsing dots with gradient colors
- **Voice Feedback** - Pulsing red animation when listening
- **Message Bubbles** - Gradient backgrounds for user/AI messages
- **Empty State** - Beautiful welcome screen with animations

## 🔧 Technical Details

- **Voice Recognition** - `speech_to_text` with permission handling
- **Animations** - `flutter_animate` for smooth effects
- **Typography** - Google Fonts (Inter)
- **Permissions** - `permission_handler` for microphone access
- **HTTP** - Direct API communication with FastAPI backend

## 🐛 Troubleshooting

### Voice Input Issues
- Grant microphone permissions when prompted
- Check Windows microphone settings
- Restart app if voice stops working

### Connection Errors
- Ensure backend is running: `uvicorn backend.app:app --reload`
- Check firewall settings
- Verify backend URL in `lib/services/api_service.dart`

## 📁 Project Structure

```
frontend/
├── lib/
│   ├── main.dart                 # App entry with splash screen
│   ├── models/message.dart       # Message data model
│   ├── screens/
│   │   ├── splash_screen.dart    # Beautiful animated splash
│   │   └── chat_screen.dart      # Enhanced chat interface
│   └── services/
│       ├── api_service.dart      # Backend communication
│       └── speech_service.dart   # Fixed voice input
├── run_dev.bat                   # Development runner
├── build_and_run.bat            # Release builder
└── README.md                     # This file
```

## 🎨 Color Palette

- **Purple**: `#8B5CF6` (purple-500)
- **Violet**: `#7C3AED` (violet-500) 
- **Pink**: `#EC4899` (pink-500)
- **Background**: `#0F0F23` → `#1A1A2E`
- **Cards**: `#1A1A2E` → `#16213E`

## 📄 License

MIT License - See main project LICENSE file
