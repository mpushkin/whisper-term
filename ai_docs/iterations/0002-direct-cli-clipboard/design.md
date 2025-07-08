# Design – Direct CLI with Clipboard

## Purpose
Enable power users to perform quick transcription tasks without navigating interactive prompts. Address the need for faster workflows, clipboard integration, and basic automation support while maintaining simplicity.

## Desired State After Change
Users can:
1. Start recording immediately with `whisper-term --record --model base`
2. Specify model and language via CLI arguments
3. Get transcribed text automatically copied to clipboard
4. Use the tool in scripts and automation workflows
5. Still access interactive mode when no `--record` flag is provided

## Proposed Solution

### Architecture Overview
```
CLI Arguments → DirectModeHandler → Existing Components
     ↓                 ↓                    ↓
  --record         RecordingFlow      AudioRecorder
  --model          ModelSelection     TranscriptionEngine
  --language       ClipboardCopy      FileManager
```

### User Experience Flow

#### **Direct Mode Usage**
```bash
# Quick transcription with default settings
whisper-term --record

# Specify model and language
whisper-term --record --model small --language spanish

# Short flags for power users
whisper-term -r -m base -l english
```

#### **Direct Mode Flow**
```
$ whisper-term --record --model base
🎙️  Whisper Term - Direct Mode
==============================

🔄 Loading model 'base'...
✅ Model loaded successfully

🎤 Recording... Press ENTER to stop
🔴 ████████░░ 80% (00:05s)

[User presses ENTER]

⏹️  Recording stopped (5.2s)
💾 Audio saved immediately: data/recordings/2025-07/2025-07-08/20250708_210530.wav
🔄 Processing transcription...
✅ Transcription: "Hello, this is a test recording."

📋 Copied to clipboard!
💾 Text saved: data/recordings/2025-07/2025-07-08/20250708_210530.txt

✅ Done!
```

### Technical Implementation

#### **Enhanced CLI Arguments**
```python
# New arguments for direct mode
parser.add_argument(
    '--record', '-r',
    action='store_true',
    help='Start recording immediately (bypass interactive mode)'
)

parser.add_argument(
    '--clipboard', '-c',
    action='store_true',
    default=True,
    help='Copy transcription to clipboard (default: True)'
)

# Enhanced existing arguments
parser.add_argument(
    '--model', '-m',
    default='base',
    choices=['tiny', 'base', 'small', 'medium', 'large', 'turbo'],
    help='Whisper model to use'
)

parser.add_argument(
    '--language', '-l',
    default='english',
    help='Language for transcription'
)
```

#### **DirectModeHandler Class**
```python
class DirectModeHandler:
    def __init__(self, model_name: str, language: str):
        self.model_name = model_name
        self.language = language
        self.clipboard_manager = ClipboardManager()
        
    def run_direct_recording(self):
        # Initialize components with CLI parameters
        # Start recording immediately
        # Save audio file immediately when recording stops
        # Process transcription
        # Copy to clipboard
        # Save text file
        # Display results
```

#### **ClipboardManager Class**
```python
import pyperclip

class ClipboardManager:
    def copy_to_clipboard(self, text: str) -> bool:
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"⚠️  Failed to copy to clipboard: {e}")
            return False
```

### Component Integration

#### **Main Entry Point**
```python
def main():
    args = parser.parse_args()
    
    # Direct mode
    if args.record:
        direct_handler = DirectModeHandler(
            model_name=args.model,
            language=args.language
        )
        direct_handler.run_direct_recording()
        return
    
    # Interactive mode (existing)
    app = WhisperTermApp()
    app.run()
```

#### **Reuse Existing Components**
- **AudioRecorder**: No changes needed
- **TranscriptionEngine**: Accept model/language parameters
- **FileManager**: No changes needed  
- **SessionManager**: No changes needed

## Technical Details

### **New Dependencies**
- `pyperclip>=1.8.0` - Cross-platform clipboard operations

### **Modified Components**
- `src/whisper_term/main.py` - Enhanced CLI argument parsing
- `src/whisper_term/app.py` - Accept model/language parameters
- `pyproject.toml` - Add pyperclip dependency

### **New Components**
- `src/whisper_term/direct_mode.py` - DirectModeHandler class
- `src/whisper_term/clipboard.py` - ClipboardManager class

### **Configuration Changes**
- TranscriptionEngine accepts model/language in constructor
- WhisperTermApp accepts model/language parameters
- CLI arguments override hardcoded defaults

## Benefits

### **User Experience**
- **Faster workflow**: Single command for quick transcription
- **Clipboard integration**: Instant access to transcribed text
- **Power user friendly**: Short flags and scriptable interface
- **Automation ready**: Can be integrated into other tools
- **Data reliability**: Audio saved immediately to prevent data loss

### **Technical**
- **Backward compatible**: Existing interactive mode unchanged
- **Minimal changes**: Reuses existing architecture
- **Cross-platform**: pyperclip works on Windows, macOS, Linux
- **Maintainable**: Clean separation between direct and interactive modes

## Risks & Mitigations

### **Clipboard Dependency Risk**
- **Risk**: pyperclip may fail on some systems or configurations
- **Mitigation**: Graceful fallback with warning message, transcription still works

### **Model Parameter Risk**
- **Risk**: Invalid model names or languages cause crashes
- **Mitigation**: Validate arguments, provide clear error messages

### **Complexity Risk**
- **Risk**: Adding CLI mode increases complexity
- **Mitigation**: Keep implementation minimal, reuse existing components

### **User Experience Risk**
- **Risk**: Users might not discover new direct mode
- **Mitigation**: Update help text and documentation clearly

### **Platform Compatibility Risk**
- **Risk**: Clipboard behavior varies across platforms
- **Mitigation**: Test on multiple platforms, handle exceptions gracefully

### **Data Loss Risk**
- **Risk**: Application crash during transcription loses recording
- **Mitigation**: Save audio file immediately after recording stops, before transcription begins
