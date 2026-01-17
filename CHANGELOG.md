# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
* OnDevice LLM integration for local processing
* Optional encryption for stored embeddings
* UI enhancements and system tray integration
* Advanced search filters and timeline view
* Auto-update mechanism
* Code-signing for Windows executable
