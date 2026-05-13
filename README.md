<div align="center">

# 🧠 Recall AI

**An Advanced FastAPI-Based Intelligent Memory System with Modern Flutter Frontend**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![OCR](https://img.shields.io/badge/OCR-Tesseract-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![Vector DB](https://img.shields.io/badge/Vector_DB-FAISS_+_Qdrant-FF6B6B?style=for-the-badge)](#)
[![LLM](https://img.shields.io/badge/LLM-Groq-000000?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)

</div>

---

## 🌟 Overview

Recall AI is an innovative intelligent memory system that captures user activity through periodic screenshots, extracts text using advanced OCR technology, and applies intelligent filters to remove sensitive information. The system encrypts cleaned text and securely manages semantic retrieval using on-device vector embeddings for contextual recall.

🔒 **On-Device Processing First**  
All screenshot capture, OCR, sensitive data filtering, encryption, and vector embedding storage happen entirely on the user’s device. Encrypted text files are processed in configurable batches, with the batch limit managed through a `.env` file. Once the threshold is reached, the system securely decrypts the batch locally, generates vector embeddings, and stores them on-device for semantic retrieval.The LLM is accessed via API (Groq) and can be replaced with a local model in future iterations. 
> This architecture ensures that raw screenshots and sensitive data never leave the user’s device, prioritizing privacy and security while still enabling powerful contextual recall capabilities.

**🎯 Key Innovation**: Users can interact with an integrated large language model (LLM) to ask questions and get meaningful responses based on their specific activities, enabling a context-aware, task-focused conversational experience.

---

## ✨ Features

### 🖥️ **Backend Capabilities**
- 📸 **Continuous Activity Capture** - Automated screenshot capture with MSS
- 🔍 **Advanced OCR Processing** - Tesseract & PaddleOCR for text extraction
- 🛡️ **Privacy Protection** - Intelligent filtering of sensitive information
- 🔐 **Data Encryption** - AES encryption for stored text data
- 🧠 **Vector Embeddings** - Semantic search with HuggingFace transformers
- 🗄️ **Dual Storage Options** - FAISS (local) & Qdrant (scalable) vector databases
- 🤖 **RAG Implementation** - Retrieval-Augmented Generation with Groq LLM
- ⚡ **Real-Time Streaming** - Async/sync model streaming responses
- 📊 **Comprehensive Logging** - Detailed activity and error tracking
- 👀 **File Watching** - Automatic processing with Watchdog

### 📱 **Frontend Features**
- 🎨 **Modern Flutter UI** - Beautiful glassmorphism design
- 🌙 **Dual Themes** - Animated dark/light mode switching
- 💬 **Enhanced Chat Interface** - Markdown support with syntax highlighting
- 🎤 **Voice Input** - Speech-to-text with Windows integration
- ⚙️ **Settings Management** - Persistent configuration storage
- 🔄 **Backend Switching** - Toggle between FAISS/Qdrant
- 📡 **Real-Time Streaming** - Live response display
- 🪟 **Windows Desktop** - Optimized for Windows 10/11

---

## 🛠️ Technology Stack

<table>
<tr>
<td width="50%">

### 🐍 **Backend Technologies**
| Technology | Purpose | Version |
|------------|---------|----------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Core Language | 3.8+ |
| ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | Web Framework | Latest |
| ![Tesseract](https://img.shields.io/badge/-Tesseract-4285F4?style=flat&logo=google&logoColor=white) | OCR Engine | 5.0+ |
| ![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) | Image Processing | Latest |
| ![HuggingFace](https://img.shields.io/badge/-HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black) | Embeddings | Transformers |
| ![FAISS](https://img.shields.io/badge/-FAISS-FF6B6B?style=flat&logo=meta&logoColor=white) | Vector Search | CPU |
| ![Qdrant](https://img.shields.io/badge/-Qdrant-DC382D?style=flat&logo=qdrant&logoColor=white) | Vector Database | Latest |
| ![Groq](https://img.shields.io/badge/-Groq-000000?style=flat&logo=groq&logoColor=white) | LLM Provider | API |

</td>
<td width="50%">

### 📱 **Frontend Technologies**
| Technology | Purpose | Version |
|------------|---------|----------|
| ![Flutter](https://img.shields.io/badge/-Flutter-02569B?style=flat&logo=flutter&logoColor=white) | UI Framework | 3.10.1+ |
| ![Dart](https://img.shields.io/badge/-Dart-0175C2?style=flat&logo=dart&logoColor=white) | Programming Language | 3.0+ |
| ![Material](https://img.shields.io/badge/-Material_Design-757575?style=flat&logo=material-design&logoColor=white) | Design System | 3.0 |
| ![Windows](https://img.shields.io/badge/-Windows-0078D4?style=flat&logo=windows&logoColor=white) | Target Platform | 10/11 |
| ![Glassmorphism](https://img.shields.io/badge/-Glassmorphism-9333EA?style=flat&logo=css3&logoColor=white) | UI Effects | - |
| ![Speech](https://img.shields.io/badge/-Speech_to_Text-4285F4?style=flat&logo=google&logoColor=white) | Voice Input | - |
| ![Markdown](https://img.shields.io/badge/-Markdown-000000?style=flat&logo=markdown&logoColor=white) | Rich Text Support | - |
| ![Animations](https://img.shields.io/badge/-Flutter_Animate-02569B?style=flat&logo=flutter&logoColor=white) | Smooth Animations | - |

</td>
</tr>
</table>

---

## 🚀 Quick Start

### 📋 Prerequisites

#### 🐍 Backend Requirements
- ![Python](https://img.shields.io/badge/-Python_3.8+-3776AB?style=flat&logo=python&logoColor=white)
- ![Tesseract](https://img.shields.io/badge/-Tesseract_OCR-4285F4?style=flat&logo=google&logoColor=white) - [Download Here](https://github.com/UB-Mannheim/tesseract/wiki)
- ![Groq](https://img.shields.io/badge/-Groq_API_Key-000000?style=flat&logo=groq&logoColor=white) - [Get API Key](https://console.groq.com)

#### 📱 Frontend Requirements
- ![Flutter](https://img.shields.io/badge/-Flutter_SDK-02569B?style=flat&logo=flutter&logoColor=white) (3.10.1+)
- ![Windows](https://img.shields.io/badge/-Windows_10/11-0078D4?style=flat&logo=windows&logoColor=white)
- ![Visual Studio](https://img.shields.io/badge/-Visual_Studio_Build_Tools-5C2D91?style=flat&logo=visual-studio&logoColor=white)

### 📥 Installation

#### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/Madhur-Prakash/Recall-AI.git
cd Recall-AI
```

#### 2️⃣ **Backend Setup**
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # activate virtual environment

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
copy .env.sample .env
```

### 🔁 Alternative: Using uv (Faster Dependency Management) - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
```bash
# Navigate to backend
cd backend

# create virtual environment
uv venv
.\venv\Scripts\activate  # activate virtual environment

# install dependencies
uv sync

# Setup environment variables
copy .env.sample .env
```

#### 3️⃣ **Frontend Setup**
```bash
# Navigate to frontend
cd ../frontend

# Install Flutter dependencies
flutter pub get

# Build for Windows
flutter build windows --release
```

#### 4️⃣ **Tesseract Installation**
1. Download from [Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install with default settings
3. Add to PATH: `C:\Program Files\Tesseract-OCR`
4. Verify: `tesseract --version`

---

## 🎮 Usage

### 🖥️ **Backend Services**

## Note:
You can get the backend up and running using either **Docker Compose** (the easiest method) or by setting it up **manually** for more  control.

> 📌 **Important:**  
> - For Docker setup, set `DEVELOPMENT_ENV = "docker"` in your `.env` file.  
> - For local development, either set `DEVELOPMENT_ENV = "local"` or comment out the line entirely.  
>  
> This ensures the application loads the correct configuration and prevents environment-related issues.

> 📢 **Additional Requirement (Very Important):**
> Even if you are running the backend using Docker, the **screen capture script must be executed directly on your host system**, not inside the container.


1. **Using Docker Compose (Easiest Method)**

    #### Start docker services:
    ```bash
    docker-compose up --build
    ```
    #### Run the following script locally on your machine:

    ```bash
    python recall_ai/src/mss_screen.py
    ```

    > This is required because screen capture needs direct access to the host OS display, which Docker containers cannot reliably access.

2. **Manual Setup (More Control)**
    #### 1️⃣ **Start Screen Capture**
    ```bash
    cd backend
    python recall_ai/src/mss_screen.py
    ```

    #### 2️⃣ **Start Vector Processing**

    **For FAISS (Local):**
    ```bash
    python recall_ai/config/gen_vector_embedding.py
    ```

    **For Qdrant (Cloud):**
    ```bash
    # Start Qdrant server first
    docker run -p 6333:6333 qdrant/qdrant

    # Then start processing
    python recall_ai/config/quad_gen_vector_embedding.py
    ```

    #### 3️⃣ **Start API Server**
    ```bash
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
    ```

### 📱 **Frontend Application**

#### 🚀 **Development Mode**
```bash
cd frontend
flutter run -d windows
```

#### 📦 **Production Build**
```bash
flutter build windows --release
# Executable: build/windows/x64/runner/Release/recall_frontend.exe
```

---

## 🌐 API Endpoints

### 📡 **Chat Endpoints**
| Endpoint | Method | Description | Vector Store |
|----------|--------|-------------|--------------|
| `/chat` | GET | Chat with FAISS backend | ![FAISS](https://img.shields.io/badge/-FAISS-FF6B6B?style=flat) |
| `/quad_chat` | GET | Chat with Qdrant backend | ![Qdrant](https://img.shields.io/badge/-Qdrant-DC382D?style=flat) |
| `/docs` | GET | Interactive API documentation | - |
| `/` | GET | Health check endpoint | - |

### 📝 **Example Request**
```bash
curl "http://localhost:8000/chat?query=What was I working on yesterday?"
```

---

## 📁 Project Structure

```
RecallAI/
├── 🐍 backend/                     # Python FastAPI Backend
│   ├── 📸 images_taken/            # Encrypted screenshot data
│   ├── 🗄️ img_vector_store/        # FAISS vector database
│   ├── 📊 logs/                    # Application logs
│   ├── 🧠 recall_ai/              # Core application
│   │   ├── ⚙️ config/              # Vector processing workers
│   │   ├── 🛠️ helpers/             # Utility functions
│   │   ├── 🚀 src/                 # Main application logic
│   │   └── 🔢 vector_embeddings/   # Embedding processing
│   ├── 🌐 app.py                   # FastAPI application
│   ├── 📋 requirements.txt         # Python dependencies
│   └── 🔐 .env.sample             # Environment template
├── 📱 frontend/                    # Flutter Desktop App
│   ├── 📚 lib/                     # Dart source code
│   │   ├── 📄 models/              # Data models
│   │   ├── 🖼️ screens/             # UI screens
│   │   ├── 🔧 services/            # Business logic
│   │   └── 🎯 main.dart           # App entry point
│   ├── 🪟 windows/                 # Windows-specific files
│   └── 📦 pubspec.yaml            # Flutter dependencies
├── 📄 README.md                   # This file
└── 📜 LICENSE                     # MIT License
```

---

## ⚙️ Configuration

### 🔧 **Backend Settings**

#### 📝 **Environment Variables (.env)**
```env
GROQ_API_KEY="your_groq_api_key_here"
SESSION_SECRET_KEY="your_session_secret"
DEVELOPMENT_ENV="local"  # or "docker"
IMAGES_DIR = "YOUR_IMAGES_DIR"  # Directory path for storing captured images and OCR data
FAISS_VECTOR_STORE_DIR  = "YOUR_FAISS_VECTOR_STORE_DIR "
```

#### 🎛️ **Key Parameters**
- **Screenshot Interval**: 30 seconds (configurable in `mss_screen.py`)
- **Text File Limit**: 34 files before processing (configurable in `gen_vector_embedding.py`)
- **Vector Dimensions**: 384 (sentence-transformers/all-MiniLM-L6-v2)
- **Retrieval Count**: 16 documents per query

### 📱 **Frontend Settings**

#### ⚙️ **Available Options**
- 🌙 **Theme Mode**: Dark/Light with animated transitions
- 🎤 **Voice Input**: Enable/disable speech recognition
- 🗄️ **Vector Store**: Switch between FAISS/Qdrant
- 🌐 **Server URL**: Configure backend endpoint

---

## 🔒 Privacy & Security

### 🛡️ **Privacy Protection**
- **Sensitive Data Filtering**: Automatic removal of passwords, API keys, tokens
- **Local Processing**: OCR and filtering happen locally
- **Encrypted Storage**: AES encryption for all text data

### 🔐 **Security Features**
- **Data Encryption**: AES-256 encryption for stored text
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error responses without data leakage

### 🤖 LLM Execution Model
- OCR, filtering, encryption, and embeddings run fully on-device
- Groq LLM is currently accessed via API for response generation
- No raw screenshots or sensitive data are sent to the LLM
- Architecture supports future on-device / local LLM integration

---

## 🚀 Performance

### ⚡ **Optimization Features**
- **Async Processing**: Non-blocking I/O operations
- **Streaming Responses**: Real-time LLM output
- **Vector Caching**: Efficient similarity search
- **Batch Processing**: Optimized embedding generation
- **Memory Management**: Automatic cleanup and rotation

### 📊 **Benchmarks**
- **Screenshot Processing**: ~2-3 seconds per image
- **OCR Extraction**: ~1-2 seconds per screenshot
- **Vector Search**: <100ms for similarity queries
- **LLM Response**: ~1-3 seconds (depends on Groq API)

---

## 🔧 Troubleshooting

### 🐛 **Common Issues**

#### 🎤 **Voice Input Not Working**
```bash
# Check Windows microphone permissions
# Settings → Privacy & Security → Microphone → Allow desktop apps

# Verify default microphone
# Settings → System → Sound → Input device

# Enable Windows Speech Recognition
# Settings → Time & Language → Speech
```

#### 🔍 **OCR Issues**
```bash
# Verify Tesseract installation
tesseract --version

# Check PATH environment variable
echo $env:PATH | Select-String "Tesseract"

# Reinstall if needed
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### 🌐 **Connection Errors**
```bash
# Check backend server status
curl http://localhost:8000/

# Verify Groq API key
# Check .env file configuration

# Test API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.groq.com/openai/v1/models
```

---

## 🔮 Future Enhancements

### 🎯 **Planned Features**
- 🌐 **Multi-Platform Support** - macOS and Linux compatibility
- 🔊 **Audio Capture** - Meeting and call transcription
- 📊 **Analytics Dashboard** - Activity insights and patterns
- 🤖 **Custom Models** - Local LLM integration
- 📱 **Mobile App** - iOS and Android clients
- 🔄 **Cloud Sync** - Cross-device synchronization
- 🎨 **UI Themes** - Additional theme options
- 🌍 **Internationalization** - Multi-language support

### 🛠️ **Technical Improvements**
- ⚡ **Performance Optimization** - Faster processing pipelines
- 🧠 **Advanced OCR** - Better accuracy with multiple engines
- 🔍 **Enhanced Search** - Semantic and temporal filtering
- 📈 **Scalability** - Distributed processing support

---

## 🤝 Contributing

Contributions are welcome! To contribute:

### 🎯 **Areas for Contribution**
- 🐛 **Bug Fixes** - Report and fix issues
- ✨ **New Features** - Implement planned enhancements
- 📚 **Documentation** - Improve guides and examples
- 🎨 **UI/UX** - Design improvements
- 🧪 **Testing** - Add test coverage
- 🌍 **Localization** - Add language support

### 📝 **Contribution Process**
1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Author

<div align="center">

**Madhur Prakash**

[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Madhur-Prakash)
[![Medium](https://img.shields.io/badge/-Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@madhurprakash2005)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/madhurprakashmangal/)

*Building the future of intelligent memory systems* 🚀

</div>

---

<div align="center">

### 🌟 **Star this repository if you found it helpful!** 🌟

![Stars](https://img.shields.io/github/stars/Madhur-Prakash/Recall-AI?)
![Forks](https://img.shields.io/github/forks/Madhur-Prakash/Recall-AI)
![Issues](https://img.shields.io/github/issues/Madhur-Prakash/Recall-AI)

**Made with ❤️ and lots of ☕**

</div>