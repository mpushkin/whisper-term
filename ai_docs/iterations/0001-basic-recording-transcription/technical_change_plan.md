# Technical Change Plan – Basic Recording and Transcription

## Summary
Implement core Whisper Term functionality: record audio via terminal interface, transcribe using local Whisper model, save organized files. See `design.md` for architecture details.

## Code Changes (by module / file)
| Path | Change Type | Description |
|------|-------------|-------------|
| main.py | new | Entry point with CLI interface and main loop |
| src/whisper_term/app.py | new | Main application class `WhisperTermApp` |
| src/whisper_term/audio_recorder.py | new | `AudioRecorder` class using sounddevice |
| src/whisper_term/transcription_engine.py | new | `TranscriptionEngine` class managing Whisper model |
| src/whisper_term/file_manager.py | new | `FileManager` class for file organization |
| src/whisper_term/session_manager.py | new | `SessionManager` for timestamps and session data |
| src/whisper_term/models.py | new | Data models (RecordingSession dataclass) |
| requirements.txt | new | Project dependencies |
| pyproject.toml | new | Project configuration and build settings |
| .gitignore | new | Ignore data/ folder and Python cache files |

## Data & Schema Changes
- Create `data/` directory structure:
  - `data/models/` - Whisper model cache
  - `data/recordings/YYYY-MM/YYYY-MM-DD/` - Session recordings
- File formats:
  - Audio: WAV format (16kHz, mono)
  - Text: UTF-8 plain text files
  - Naming: `YYYYMMDD_HHMMSS.{wav,txt}`

## API / Interface Changes
No external APIs. CLI interface:
- `python main.py` or `whisper-term` command
- Space key for start/stop recording
- Ctrl+C to exit application

## Dependencies & Configuration
```
openai-whisper>=20231117
sounddevice>=0.5.2
numpy>=1.24.0
keyboard>=0.13.5
```

Hardcoded configuration:
- Model: "base"
- Language: "english"
- Sample rate: 16000 Hz
- Model cache: `data/models/`

## Detailed Steps
1. **Project Setup**
   - Create project structure with src/ layout
   - Add requirements.txt and pyproject.toml
   - Configure .gitignore

2. **Core Data Models**
   - Implement RecordingSession dataclass
   - Add timestamp and path utilities

3. **Audio Recording**
   - Implement AudioRecorder with sounddevice
   - Add start/stop recording methods
   - Handle audio buffer management

4. **Transcription Engine**
   - Implement TranscriptionEngine class
   - Add model loading and caching
   - Add transcription method with error handling

5. **File Management**
   - Implement FileManager for directory creation
   - Add save_audio and save_text methods
   - Implement date-based folder organization

6. **Session Management**
   - Implement SessionManager for timestamps
   - Add session creation and metadata tracking

7. **Main Application**
   - Implement WhisperTermApp class
   - Add terminal UI with keyboard handling
   - Integrate all components

8. **Entry Point**
   - Create main.py with CLI interface
   - Add basic error handling and help

## Testing Strategy
- **Unit tests**: 
  - `test_audio_recorder.py` - Mock sounddevice, test recording
  - `test_transcription_engine.py` - Mock whisper model
  - `test_file_manager.py` - Test file operations
  - `test_session_manager.py` - Test timestamp generation
- **Integration tests**:
  - End-to-end recording and transcription flow
  - File organization and saving
- **Manual verification**:
  - Test recording quality with different microphones
  - Verify transcription accuracy
  - Test keyboard interactions

## Rollback / Migration Plan
No database migrations required. Rollback approach:
1. Remove installed package
2. Data files remain in `data/` folder (user choice to keep/delete)
3. No system-wide changes to revert

## Risks & Mitigations (technical only)

### Audio Dependencies
- **Risk**: sounddevice installation issues on different platforms
- **Mitigation**: Document platform-specific installation steps

### Model Download
- **Risk**: Whisper model download fails or is slow
- **Mitigation**: Handle download errors gracefully, show progress

### File Permissions
- **Risk**: Cannot create data/ directories
- **Mitigation**: Check permissions on startup, clear error messages

### Keyboard Handling
- **Risk**: Keyboard library conflicts or platform issues
- **Mitigation**: Test on multiple platforms, provide fallback options

### Memory Usage
- **Risk**: Large audio buffers consume memory
- **Mitigation**: Use streaming approach, limit buffer size

### Threading
- **Risk**: Audio recording thread synchronization issues
- **Mitigation**: Use thread-safe queues, proper cleanup
