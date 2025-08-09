# Recall AI

**An Advanced FastAPI-Based Intelligent Memory System**

---
## Overview
Recall AI is an innovative intelligent memory system that captures user activity through periodic screenshots, extracts text using OCR, and applies intelligent filters to remove sensitive information. The system then encrypts the cleaned text and converts it into vector embeddings for semantic search and contextual recall.
A standout feature of Recall AI is that users can interact with the integrated large language model (LLM) to ask questions and get meaningful responses based on the specific tasks they were performing, enabling a context-aware, task-focused conversational experience.

---

## 🚀 **Frontend Development Update & Contribution Invitation**  

The frontend of **Recall AI** is currently under active development and will be released soon. Meanwhile, the backend is fully functional and ready to use.   

For the frontend, I am specifically looking to develop a **desktop application** that offers an intuitive, responsive, and feature-rich interface for interacting with Recall AI’s backend services.  

If you're interested in contributing to the frontend and helping improve the user experience, feel free to fork the repository, work on the frontend, and submit a pull request. Contributions are welcome and will help bring Recall AI to life faster.

---

## Features
- **Continuous Activity Capture**: Periodically takes screenshots to capture user activity.
- **Intelligent Text Extraction**: Uses OCR to extract text from screenshots and applies filters to remove sensitive information.
- **Vector Embeddings**: Converts cleaned text into vector embeddings for efficient semantic search and contextual recall.
- **Flexible Storage Options**: Supports both FAISS for lightweight, local vector search and Qdrant for scalable, high-performance vector database operations.
- **Retrieval-Augmented Generation (RAG)**: Enables natural language querying of past activity with context-aware responses and strict privacy guardrails.
- **Real-Time LLM Streaming**: Ensures instant responses with asynchronous or synchronous model streaming.

---

## Technology Stack
- **Backend Framework**: FastAPI
- **Storage Backends**: FAISS, Qdrant
- **OCR Engine**: Tesseract-OCR
- **Programming Language**: Python

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Madhur-Prakash/Recall-AI.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Recall-AI
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
5. Set up the backend:
   - Configure the storage backend (FAISS or Qdrant) according to your preference.
   - Ensure the necessary dependencies for OCR and vector embeddings are installed.

6. Install Tesseract OCR:
   ```bash
   Download and install from:
   https://github.com/UB-Mannheim/tesseract/wiki # Follow installation instructions
   Ensure pytesseract can access the installed binary.
   ```
---

## Usage
1. Go to Backend directory:
   ```bash
   cd backend
   ```
2. Start the screen capture script
   ```bash
   python recall_ai/src/mss_screen.py
   ```
3. Start the Kafka worker:
   - For Qdrant (Vector DB):
   ```bash
   python recall_ai/config/quad_gen_vector_embedding.py
   ```

   - For FAISS (In-memory DB):
   ```bash
   python recall_ai/config/gen_vector_embedding.py
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn backend.app:app --reload
   ```
5. Access the API documentation at:
   ```
   http://127.0.0.1:8000/docs
   ```
   ---

## API Endpoints
### Activity Capture Endpoints
- **POST /quad_chat**: Chat with history using the index stored in Qdrant.
- **POST /chat**: Chat with history using the index stored in FAISS.
---

## Project Structure
```plaintext
RecallAI/
├── .gitignore  # gitignore file for GitHub
├── README.md  # Project documentation
├── backend
│   ├── Dockerfile
│   ├── __init__.py  # initializes package
│   ├── app.py  # main FastAPI app
│   ├── docker-compose.yml
│   ├── recall_ai
│   │   ├── __init__.py  # initializes package
│   │   ├── config
│   │   │   ├── __init__.py  # initializes package
│   │   │   ├── gen_vector_embedding.py
│   │   │   └── quad_gen_vector_embedding.py
│   │   ├── helpers
│   │   │   ├── __init__.py  # initializes package
│   │   │   ├── dependencies.py
│   │   │   ├── screen_shot.py
│   │   │   ├── utils.py
│   │   │   └── watch.py
│   │   ├── src
│   │   │   ├── __init__.py  # initializes package
│   │   │   ├── mss_screen.py
│   │   │   ├── quad_recall.py
│   │   │   └── recall.py
│   │   └── vector_embeddings
│   │       ├── __init__.py  # initializes package
│   │       ├── quad_vecor_embedding.py
│   │       └── store_vector_embedding.py
│   ├── requirements.txt
│   └── voice_config
│       ├── __init__.py  # initializes package
│       ├── voice-assistant.html
│       ├── voice.py
│       └── voice_api.py
└── frontend
    └── .gitkeep
```
---

## Future Enhancements
- **Improve OCR Accuracy**: Integrate more advanced OCR engines for better text extraction accuracy.
- **Enhance Query Capabilities**: Develop more sophisticated natural language processing techniques for querying past activity.
- **Expand Storage Options**: Support additional storage backends for increased flexibility.
---

## Contribution Guidelines
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and submit a pull request.
---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author
**Madhur-Prakash**  
[GitHub](https://github.com/Madhur-Prakash) | [Medium](https://medium.com/@madhurprakash2005)

---