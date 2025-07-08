# Design – Basic Recording and Transcription

## Purpose
Establish core functionality for Whisper Term by creating a minimal viable product that allows users to record audio and get transcriptions. This addresses the need for a simple proof-of-concept and provides the foundation for future streaming features.

## Desired State After Change
Users can:
1. Launch `whisper-term` from command line
2. Start recording by pressing a key (e.g., Space)
3. See visual feedback that recording is active
4. Stop recording by pressing a key again
5. Automatically get transcription displayed in terminal
6. Find saved audio and text files in organized `data/` folder structure

## Proposed Solution

### Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Terminal UI   │ -> │  Audio Recorder │ -> │   Transcriber   │
│   (main.py)     │    │  (sounddevice)  │    │   (whisper)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                v                       v
                       ┌─────────────────┐    ┌─────────────────┐
                       │  File Manager   │    │  Session Data   │
                       │  (save audio)   │    │  (save text)    │
                       └─────────────────┘    └─────────────────┘
```

### User Flow
1. **Launch**: `python main.py` or `whisper-term`
2. **Instructions**: Display "Press SPACE to start recording, SPACE again to stop"
3. **Recording**: Visual indicator (e.g., "🔴 Recording... Press SPACE to stop")
4. **Processing**: "Processing transcription..." message
5. **Result**: Display transcribed text and file paths
6. **Repeat**: Return to step 2 for new recording

### File Organization
```
data/
├── models/              # Whisper model cache
│   └── base.pt         # Downloaded base model
└── recordings/         # Session recordings
    └── 2025-07/
        └── 2025-07-08/
            ├── 20250708_143022.wav
            └── 20250708_143022.txt
```

### Hardcoded Settings
- **Model**: `base` (good balance of speed/accuracy)
- **Language**: `english` (for optimal performance)
- **Sample Rate**: 16000 Hz (Whisper standard)
- **Format**: WAV for audio, plain text for transcription

## Technical Details

### Core Components
1. **WhisperTermApp**: Main application class
2. **AudioRecorder**: Handles recording with sounddevice
3. **TranscriptionEngine**: Manages Whisper model and transcription
4. **FileManager**: Handles file organization and saving
5. **SessionManager**: Manages timestamps and session data

### Key Dependencies
- `openai-whisper`: Speech-to-text transcription
- `sounddevice`: Audio recording
- `numpy`: Audio data processing
- `keyboard` or `click`: Terminal input handling

### Data Models
```python
@dataclass
class RecordingSession:
    timestamp: datetime
    audio_path: Path
    text_path: Path
    transcription: str
    duration: float
```

## Benefits
- **Immediate Value**: Users can test speech-to-text functionality right away
- **Simple UX**: Single-key start/stop recording
- **Organized Storage**: Automatic file organization by date
- **Foundation**: Establishes architecture for future features
- **Offline**: No internet required, privacy-focused

## Risks & Mitigations

### Performance Risk
- **Risk**: Base model may be slow on older hardware
- **Mitigation**: Display processing message, consider model size detection

### Audio Quality Risk
- **Risk**: Poor microphone quality affects transcription
- **Mitigation**: Use standard sample rates, add audio level indicators

### File System Risk
- **Risk**: Permission issues with data folder creation
- **Mitigation**: Check/create directories on startup, handle errors gracefully

### Dependency Risk
- **Risk**: Complex installation due to audio dependencies
- **Mitigation**: Document installation steps, provide troubleshooting guide

### User Experience Risk
- **Risk**: Unclear when recording starts/stops
- **Mitigation**: Clear visual feedback, consistent key bindings
