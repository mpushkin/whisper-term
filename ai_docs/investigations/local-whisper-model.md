# Local Whisper Model Investigation

## Overview
Investigation into implementing local OpenAI Whisper model for speech-to-text transcription in a Python terminal application.

## Key Findings

### Whisper Library Installation
```bash
pip install openai-whisper
```

### Model Download & Management
- **Automatic Download**: Models are downloaded automatically on first use
- **Storage Location**: Models cached in `~/.cache/whisper/` by default
- **Custom Location**: Can specify custom download directory with `download_root` parameter
- **Available Models**: tiny, base, small, medium, large, turbo (latest)

### Basic Usage
```python
import whisper

# Load model (downloads if not cached)
model = whisper.load_model("turbo")

# Transcribe audio file
result = model.transcribe("audio.mp3")
print(result["text"])

# Custom download location
model = whisper.load_model("base", download_root="./data/models/")
```

### Model Sizes & Performance
| Model | Size | Performance |
|-------|------|-------------|
| tiny  | ~39MB | Fastest, lowest accuracy |
| base  | ~74MB | Good balance for testing |
| small | ~244MB | Better accuracy |
| medium| ~769MB | High accuracy |
| large | ~1550MB | Highest accuracy |
| turbo | ~809MB | Latest, optimized for English |

### Real-time Audio Recording

#### Audio Libraries (2025)
**SoundDevice (Recommended)**
- Latest version: 0.5.2 (May 2025)
- Records to NumPy arrays (ideal for processing)
- Simplified, user-friendly interface
- Installation: `pip install sounddevice`

**PyAudio (Alternative)**
- More low-level control
- Records to bytes objects
- Closer to PortAudio interface

#### Real-time Implementation Approaches
1. **Threaded Recording**: Continuous audio recording in background thread
2. **Voice Activity Detection (VAD)**: Only process when speech detected
3. **Chunk Processing**: Process audio in small segments (e.g., 1-5 seconds)
4. **Buffer Management**: Concatenate previous audio with new data for context

### Real-time Solutions
- **WhisperLive**: Nearly-live implementation with VAD
- **Whisper-Streaming**: Real-time with 3.3s latency
- **Custom Implementation**: Thread-based recording with periodic transcription

### Code Example for Real-time Recording
```python
import sounddevice as sd
import numpy as np
import whisper
import threading
import queue

class WhisperRealtime:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.recording = False
        
    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())
    
    def start_recording(self):
        self.recording = True
        with sd.InputStream(callback=self.audio_callback, 
                          channels=1, 
                          samplerate=self.sample_rate):
            while self.recording:
                if not self.audio_queue.empty():
                    # Process audio chunks
                    audio_data = self.audio_queue.get()
                    # Add processing logic here
                    pass
```

### File Organization Strategy
Based on requirements:
```
data/
├── models/               # Whisper model cache
│   ├── tiny.pt
│   ├── base.pt
│   └── ...
└── recordings/          # Session recordings
    └── YYYY-MM/
        └── YYYY-MM-DD/
            ├── timestamp.wav
            └── timestamp.txt
```

### Implementation Recommendations

#### Dependencies
```bash
pip install openai-whisper sounddevice numpy scipy
```

#### Model Selection Strategy
- **Development**: Use `base` model for fast testing
- **Production**: Allow user to select from predefined list
- **Default**: `turbo` for English, `small` for multilingual

#### Architecture
1. **Model Manager**: Handle model downloading and caching
2. **Audio Recorder**: Real-time recording with sounddevice
3. **Transcriber**: Process audio chunks with Whisper
4. **Session Manager**: Handle file organization and saving

### Challenges & Solutions

#### Performance
- **Challenge**: Whisper processes 30-second chunks
- **Solution**: Use overlapping chunks or streaming implementations

#### Real-time Streaming
- **Challenge**: Whisper not designed for real-time
- **Solution**: Process in small chunks (1-5 seconds) with buffering

#### Quality vs Speed
- **Challenge**: Larger models are more accurate but slower
- **Solution**: Allow user configuration, default to balanced model

### Next Steps
1. Create proof-of-concept with `base` model
2. Test real-time recording with sounddevice
3. Implement basic transcription pipeline
4. Add model management functionality
5. Create session-based file organization

## Conclusion
Local Whisper implementation is feasible with the openai-whisper library. Real-time functionality requires custom implementation using threading and audio buffering. SoundDevice provides the best audio recording capabilities for 2025.