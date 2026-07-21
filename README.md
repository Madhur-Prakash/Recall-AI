<div align="center">

# 🧠 Recall AI

**An Intelligent Memory System — FastAPI Backend · Flutter Desktop Frontend**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![Tesseract](https://img.shields.io/badge/OCR-Tesseract-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![Vector DB](https://img.shields.io/badge/Vector_DB-FAISS_+_Qdrant-FF6B6B?style=for-the-badge)](#)
[![Groq](https://img.shields.io/badge/LLM-Groq-000000?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)

[![Stars](https://img.shields.io/github/stars/Madhur-Prakash/Recall-AI?style=flat-square)](https://github.com/Madhur-Prakash/Recall-AI/stargazers)
[![Forks](https://img.shields.io/github/forks/Madhur-Prakash/Recall-AI?style=flat-square)](https://github.com/Madhur-Prakash/Recall-AI/network)
[![Issues](https://img.shields.io/github/issues/Madhur-Prakash/Recall-AI?style=flat-square)](https://github.com/Madhur-Prakash/Recall-AI/issues)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Overview

Recall AI is an intelligent memory system that captures user activity through periodic screenshots, extracts text via OCR, and applies intelligent filters to remove sensitive information. The system encrypts cleaned text and manages semantic retrieval using on-device vector embeddings for contextual recall.

> **On-Device Processing First**
> All screenshot capture, OCR, sensitive data filtering, encryption, and vector embedding storage happen entirely on the user's device. Encrypted text files are processed in configurable batches. Once the threshold is reached, the system decrypts the batch locally, generates vector embeddings, and stores them on-device for semantic retrieval. The LLM is accessed via API (Groq) and can be replaced with a local model in future iterations.

**Key Innovation:** Users interact with an integrated LLM to ask questions and get contextual answers based on their specific activities — enabling a context-aware, task-focused conversational experience.

---

## Features

### Backend

| Feature | Description |
|---------|-------------|
| ![Capture](https://img.shields.io/badge/Screenshot_Capture-555?style=flat-square&logo=camera) | Automated periodic capture with MSS |
| ![OCR](https://img.shields.io/badge/OCR_Processing-555?style=flat-square&logo=google) | Tesseract & PaddleOCR for text extraction |
| ![Privacy](https://img.shields.io/badge/Privacy_Filter-555?style=flat-square&logo=shield) | Intelligent filtering of sensitive data |
| ![Encryption](https://img.shields.io/badge/AES_Encryption-555?style=flat-square&logo=lock) | AES encryption for all stored text |
| ![Embeddings](https://img.shields.io/badge/Vector_Embeddings-555?style=flat-square&logo=huggingface) | Semantic search with HuggingFace transformers |
| ![Storage](https://img.shields.io/badge/Dual_Storage-555?style=flat-square) | FAISS (local) & Qdrant (scalable) vector databases |
| ![RAG](https://img.shields.io/badge/RAG_Pipeline-555?style=flat-square&logo=groq) | Retrieval-Augmented Generation with Groq LLM |
| ![Streaming](https://img.shields.io/badge/Real--Time_Streaming-555?style=flat-square) | Async/sync model streaming responses |
| ![Watchdog](https://img.shields.io/badge/File_Watching-555?style=flat-square) | Automatic processing with Watchdog |

### Frontend

| Feature | Description |
|---------|-------------|
| ![UI](https://img.shields.io/badge/Flutter_UI-555?style=flat-square&logo=flutter) | Glassmorphism design with smooth animations |
| ![Themes](https://img.shields.io/badge/Dual_Themes-555?style=flat-square) | Animated dark/light mode switching |
| ![Chat](https://img.shields.io/badge/Chat_Interface-555?style=flat-square) | Markdown support with syntax highlighting |
| ![Voice](https://img.shields.io/badge/Voice_Input-555?style=flat-square&logo=google) | Speech-to-text with Windows integration |
| ![Settings](https://img.shields.io/badge/Settings_Management-555?style=flat-square) | Persistent configuration storage |
| ![Backend](https://img.shields.io/badge/Backend_Toggle-555?style=flat-square) | Switch between FAISS and Qdrant at runtime |
| ![Streaming](https://img.shields.io/badge/Live_Streaming-555?style=flat-square) | Real-time response display |
| ![Windows](https://img.shields.io/badge/Windows_Desktop-555?style=flat-square&logo=windows) | Optimized for Windows 10/11 |

---

## Technology Stack

<table>
<tr>
<td width="50%">

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
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

### Frontend

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Flutter](https://img.shields.io/badge/-Flutter-02569B?style=flat&logo=flutter&logoColor=white) | UI Framework | 3.10.1+ |
| ![Dart](https://img.shields.io/badge/-Dart-0175C2?style=flat&logo=dart&logoColor=white) | Language | 3.0+ |
| ![Material](https://img.shields.io/badge/-Material_Design-757575?style=flat&logo=material-design&logoColor=white) | Design System | 3.0 |
| ![Windows](https://img.shields.io/badge/-Windows-0078D4?style=flat&logo=windows&logoColor=white) | Target Platform | 10/11 |
| ![Speech](https://img.shields.io/badge/-Speech_to_Text-4285F4?style=flat&logo=google&logoColor=white) | Voice Input | - |
| ![Markdown](https://img.shields.io/badge/-Markdown-000000?style=flat&logo=markdown&logoColor=white) | Rich Text | - |
| ![Animate](https://img.shields.io/badge/-Flutter_Animate-02569B?style=flat&logo=flutter&logoColor=white) | Animations | - |

</td>
</tr>
</table>

---

## Quick Start

### Prerequisites

**Backend**

- ![Python](https://img.shields.io/badge/-Python_3.8+-3776AB?style=flat&logo=python&logoColor=white)
- ![Tesseract](https://img.shields.io/badge/-Tesseract_OCR-4285F4?style=flat&logo=google&logoColor=white) — [Download](https://github.com/UB-Mannheim/tesseract/wiki)
- ![Groq](https://img.shields.io/badge/-Groq_API_Key-000000?style=flat&logo=groq&logoColor=white) — [Get API Key](https://console.groq.com)

**Frontend**

- ![Flutter](https://img.shields.io/badge/-Flutter_SDK_3.10.1+-02569B?style=flat&logo=flutter&logoColor=white)
- ![Windows](https://img.shields.io/badge/-Windows_10%2F11-0078D4?style=flat&logo=windows&logoColor=white)
- ![VS](https://img.shields.io/badge/-Visual_Studio_Build_Tools-5C2D91?style=flat&logo=visual-studio&logoColor=white)

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Madhur-Prakash/Recall-AI.git
cd Recall-AI
```

**2. Backend setup**

```bash
cd backend

# Standard (pip)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.sample .env
```

**Alternative — using [uv](https://docs.astral.sh/uv/getting-started/installation/) (faster)**

```bash
cd backend
uv venv
.\venv\Scripts\activate
uv sync
copy .env.sample .env
```

**3. Frontend setup**

```bash
cd ../frontend
flutter pub get
flutter build windows --release
```

**4. Tesseract installation**

Tesseract is required for OCR. Install it for your platform, then verify with `tesseract --version`.

<details>
<summary><strong>Windows</strong></summary>

1. Download the installer from the [UB Mannheim Tesseract wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run with default settings
3. Add to PATH: `C:\Program Files\Tesseract-OCR`
4. Verify: `tesseract --version`

</details>

<details>
<summary><strong>macOS</strong></summary>

```bash
brew install tesseract
```

</details>

<details>
<summary><strong>Linux</strong></summary>

Ubuntu / Debian:
```bash
sudo apt install tesseract-ocr
```

Fedora / RHEL:
```bash
sudo dnf install tesseract
```

Arch Linux:
```bash
sudo pacman -S tesseract
```

</details>

---

## Usage

### Backend

> **Note:** The backend can be started with Docker Compose (recommended) or manually.
>
> - Docker setup: set `DEVELOPMENT_ENV = "docker"` in `.env`
> - Local setup: set `DEVELOPMENT_ENV = "local"` or omit the variable

> **Important:** Even when using Docker, the screen capture script must run on the **host system** — containers cannot reliably access the host display.

**Option A — Docker Compose**

```bash
docker-compose up --build
```

Then on the host machine:

```bash
python recall_ai/src/mss_screen.py
```

**Option B — Manual**

```bash
# 1. Start screen capture
cd backend
python recall_ai/src/mss_screen.py

# 2a. Vector processing — FAISS (local)
python recall_ai/config/gen_vector_embedding.py

# 2b. Vector processing — Qdrant
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
python recall_ai/config/quad_gen_vector_embedding.py

# 3. Start API server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# Development
cd frontend
flutter run -d windows

# Production build
flutter build windows --release
# Output: build/windows/x64/runner/Release/recall_frontend.exe
```

---

## API Reference

| Endpoint | Method | Description | Backend |
|----------|--------|-------------|---------|
| `/chat` | `GET` | Chat with FAISS backend | ![FAISS](https://img.shields.io/badge/-FAISS-FF6B6B?style=flat) |
| `/quad_chat` | `GET` | Chat with Qdrant backend | ![Qdrant](https://img.shields.io/badge/-Qdrant-DC382D?style=flat) |
| `/docs` | `GET` | Interactive API documentation | — |
| `/` | `GET` | Health check | — |

**Example request**

```bash
curl "http://localhost:8000/chat?query=What was I working on yesterday?"
```

---

## Project Structure

```
RecallAI/
├── backend/                        # Python FastAPI backend
│   ├── images_taken/               # Encrypted screenshot data
│   ├── img_vector_store/           # FAISS vector database
│   ├── logs/                       # Application logs
│   ├── recall_ai/
│   │   ├── config/                 # Vector processing workers
│   │   ├── helpers/                # Utility functions
│   │   ├── src/                    # Main application logic
│   │   └── vector_embeddings/      # Embedding processing
│   ├── app.py                      # FastAPI entry point
│   ├── requirements.txt
│   └── .env.sample
├── frontend/                       # Flutter desktop app
│   ├── lib/
│   │   ├── models/
│   │   ├── screens/
│   │   ├── services/
│   │   └── main.dart
│   ├── windows/
│   └── pubspec.yaml
├── README.md
└── LICENSE
```

---

## Configuration

### Environment Variables (`.env`)

```env
GROQ_API_KEY="your_groq_api_key_here"
SESSION_SECRET_KEY="your_session_secret"
DEVELOPMENT_ENV="local"              # or "docker"
IMAGES_DIR="YOUR_IMAGES_DIR"
TEXT_FILE_LIMIT=34 # Maximum number of text files to process in a batch
FAISS_VECTOR_STORE_DIR="YOUR_FAISS_VECTOR_STORE_DIR"
```

### Key Parameters

| Parameter | Default | Configured In |
|-----------|---------|---------------|
| Screenshot interval | 30 seconds | `mss_screen.py` |
| Text file batch limit | 34 files | `gen_vector_embedding.py` |
| Vector dimensions | 384 | `all-MiniLM-L6-v2` |
| Retrieval count | 16 documents | query config |

### Frontend Options

| Option | Description |
|--------|-------------|
| Theme mode | Dark / Light with animated transitions |
| Voice input | Enable or disable speech recognition |
| Vector store | Switch between FAISS and Qdrant |
| Server URL | Configure backend endpoint |

---

## Privacy & Security

### On-Device Processing

- Sensitive data filtering removes passwords, API keys, and tokens before any storage
- OCR and filtering run entirely locally
- AES-256 encryption for all stored text

### LLM Execution Model

- OCR, filtering, encryption, and embeddings run fully on-device
- Groq LLM is accessed via API only for response generation — no raw screenshots or sensitive data are sent
- Architecture supports future local LLM integration

---

## Performance

| Metric | Benchmark |
|--------|-----------|
| Screenshot processing | ~2–3 seconds / image |
| OCR extraction | ~1–2 seconds / screenshot |
| Vector search | < 100 ms |
| LLM response | ~1–3 seconds (Groq API) |

**Optimizations:** async I/O · streaming responses · vector caching · batch embedding generation · automatic memory rotation

---

## Troubleshooting

**Voice input not working**

```bash
# Windows Settings → Privacy & Security → Microphone → Allow desktop apps
# Windows Settings → System → Sound → verify input device
# Windows Settings → Time & Language → Speech → enable Windows Speech Recognition
```

**OCR issues**

```bash
tesseract --version
echo $env:PATH | Select-String "Tesseract"
# If missing, reinstall from https://github.com/UB-Mannheim/tesseract/wiki
```

**Connection errors**

```bash
curl http://localhost:8000/
# Check .env for correct GROQ_API_KEY
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.groq.com/openai/v1/models
```

---

## Roadmap

**Planned features**

- Multi-platform support — macOS and Linux
- Audio capture — meeting and call transcription
- Analytics dashboard — activity insights
- Local LLM integration
- Mobile clients — iOS and Android
- Cross-device cloud sync
- Internationalization

**Technical improvements**

- Faster processing pipelines
- Multi-engine OCR for improved accuracy
- Semantic and temporal search filtering
- Distributed processing support

---

## Contributing

Contributions are welcome across all areas:

| Area | Examples |
|------|---------|
| ![Bug](https://img.shields.io/badge/-Bug_Fixes-d73a4a?style=flat) | Reproduce and resolve open issues |
| ![Feature](https://img.shields.io/badge/-New_Features-0075ca?style=flat) | Implement items from the roadmap |
| ![Docs](https://img.shields.io/badge/-Documentation-0075ca?style=flat) | Improve guides and examples |
| ![UI](https://img.shields.io/badge/-UI%2FUX-e4e669?style=flat&logoColor=black) | Design and interaction improvements |
| ![Tests](https://img.shields.io/badge/-Testing-brightgreen?style=flat) | Add or expand test coverage |
| ![i18n](https://img.shields.io/badge/-Localization-blueviolet?style=flat) | Add language support |

```bash
# 1. Fork the repository
# 2. Create a feature branch
git checkout -b feature/your-feature

# 3. Commit your changes
git commit -m "feat: add your feature"

# 4. Push and open a pull request
git push origin feature/your-feature
```

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Madhur Prakash**

[![GitHub](https://img.shields.io/badge/-GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Madhur-Prakash)
[![Medium](https://img.shields.io/badge/-Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@madhurprakash2005)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/madhurprakashmangal/)

*Building the future of intelligent memory systems*

</div>
