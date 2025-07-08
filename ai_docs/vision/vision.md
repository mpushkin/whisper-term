# Whisper Term Vision

## Overview

Whisper Term is a Python-based terminal application for real-time speech-to-text transcription using OpenAI's open-source Whisper model. The app provides an interactive dictation experience with automatic saving and model management.

## Core Features

### Interactive Mode
- Start dictation sessions from the terminal
- Stream transcribed text to the terminal in real-time
- Save both audio and transcribed text automatically

### Model Management
- Select from predefined list of Whisper models
- Automatic model downloading and caching
- Simple model management (download, cache, use)

### Data Organization
- Automatic session-based file organization
- Date-based folder structure for recordings and transcriptions
- Gitignored data storage for privacy

## Technical Architecture

### Technology Stack
- **Language**: Python
- **Speech-to-Text**: OpenAI Whisper (open-source)
- **Interface**: CLI/Terminal-based
- **Audio Processing**: Real-time audio capture

### File Structure
```
data/
├── recordings/
│   └── YYYY-MM/
│       └── YYYY-MM-DD/
│           ├── timestamp.wav (audio)
│           └── timestamp.txt (transcription)
└── models/
    └── [cached whisper models]
```

### Model Selection
- Predefined list of available Whisper models (tiny, small, medium, large, etc.)
- User can select model at startup or configure default
- Models downloaded on first use and cached locally

## User Experience

### Default Interactive Mode
1. Launch app (`whisper-term`)
2. Select or use default model
3. Start dictation session
4. Real-time transcription streams to terminal
5. Audio and text automatically saved to date-based folders
6. Easy session management and review

### Data Management
- All recordings organized by date
- Easy access to previous sessions
- Privacy-focused with gitignored storage
- Timestamped files for easy reference

## Future Considerations
- Multiple output formats
- Configuration file for user preferences
- Batch processing mode
- Integration with other tools