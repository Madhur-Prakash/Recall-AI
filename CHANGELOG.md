# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] – On-Device LLM Migration (21-07-2026)

### Changed

* Replaced Groq (cloud LLM API) with Ollama for fully on-device LLM inference
* Default model set to `qwen3:8b`, a strong on-device reasoning model
* Model is configurable via `OLLAMA_MODEL`; any installed Ollama model can be used
* `GROQ_API_KEY` and all Groq dependencies removed from the project

### Added

* Startup pre-flight check that verifies the configured Ollama model is installed before the server starts
* Interactive prompt to download the model on first run if it is missing, pulling it before startup continues
* `OLLAMA_AUTO_PULL` flag to auto-download the model in non-interactive environments (Docker, CI)
* Optional `OLLAMA_REASONING` flag for models with Ollama "thinking" support (e.g. `qwen3`, `deepseek-r1`)
* Automatic stripping of `<think>...</think>` reasoning traces from streamed responses, so only the final answer reaches the chat UI

### Security

* No queries, context, or screenshots are ever sent to a third-party LLM API
* LLM inference now runs fully on the user's own machine, alongside OCR, filtering, encryption, and embeddings

### Fixed

* Startup crash caused by an incorrect import path introduced during the Ollama migration
* Reasoning flag handling now uses a shared, tested truthy-value parser instead of duplicated inline logic

### Known Limitations

* Response speed now depends on local hardware rather than a cloud API, so performance varies by machine
* Enabling `OLLAMA_REASONING` on a model without thinking support causes Ollama to reject the request; leave it unset unless the selected model supports it

---

## [1.0.0] – Initial Stable Release (18-01-2026)

### Added

* Desktop application for Recall AI with background screen capture support
* Automated screenshot capture using system-level APIs
* OCR pipeline to extract text from captured screens
* Intelligent filtering to reduce noise and irrelevant data
* Secure local storage for processed data
* Vector-based embedding generation for semantic search
* Query interface to retrieve past activity using natural language
* Configurable capture intervals and application settings
* Logging mechanism for debugging and monitoring
* `.env`-based configuration support

### Security

* No raw screenshots are transmitted externally
* Sensitive content filtering before processing
* All processing performed locally unless explicitly configured otherwise
* Clear user consent required before enabling screen capture

### Performance

* Optimized screen capture to minimize CPU usage
* Batched processing for OCR and embeddings
* Improved memory handling for long-running sessions

### Known Limitations

* Windows-only support in this release
* Unsigned executable may trigger Windows SmartScreen warnings
* Initial startup may take longer due to model loading

---

### Planned for Future Releases

* macOS and Linux support
* Optional encryption for stored embeddings
* UI enhancements and system tray integration
* Advanced search filters and timeline view
* Auto-update mechanism
* Code-signing for Windows executable
