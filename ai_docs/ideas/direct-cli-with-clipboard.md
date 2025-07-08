# Idea: Direct CLI Usage with Clipboard Integration

## Context

Currently, Whisper Term always starts in interactive mode, requiring users to navigate through menus or press keys to start recording. For power users and automation scenarios, it would be more efficient to have a direct CLI mode where specifying model parameters immediately starts recording, and the transcribed result is automatically copied to the clipboard for easy pasting.

## Proposal

Implement a **direct CLI mode** that bypasses the interactive interface when model parameters are provided, automatically starts recording, and copies the transcription result to the clipboard upon completion.

### Enhanced CLI Arguments

#### **Current CLI Interface**
```bash
whisper-term                    # Interactive mode
whisper-term --model base       # Interactive mode with base model
whisper-term --language spanish # Interactive mode with Spanish
```

#### **Proposed Direct CLI Interface**
```bash
# Direct recording with automatic clipboard copy
whisper-term --record --model base
whisper-term --record --model small --language spanish
whisper-term --record --duration 30s
whisper-term --record --model turbo --output-format json

# Quick one-liner for power users
whisper-term -r -m base         # Short flags
whisper-term -r -m small -l es  # Language codes
whisper-term -r --timeout 60s   # Auto-stop after 60s

# Batch processing with clipboard
whisper-term --file audio.wav --model base --clipboard
whisper-term --file *.wav --model small --clipboard --format json
```

### User Experience Flow

#### **Direct Recording Mode**
```bash
$ whisper-term --record --model base
🎙️  Whisper Term - Direct Recording Mode
=========================================

🔄 Loading model 'base'...
✅ Model loaded successfully

🎤 Recording started automatically...
   Press ENTER to stop recording
   Press Ctrl+C to cancel

🔴 Recording... (00:05s)
Audio Level: ████████░░ 80%

[User presses ENTER]

⏹️  Recording stopped (5.2s)
🔄 Processing transcription...
✅ Transcription completed

📝 Result: "Hello, this is a test recording for the whisper application."

📋 Copied to clipboard!
💾 Saved to: data/recordings/2025-07/2025-07-08/20250708_210530.txt
🎵 Audio saved: data/recordings/2025-07/2025-07-08/20250708_210530.wav

✅ Done!
```

#### **Batch File Processing**
```bash
$ whisper-term --file meeting.wav --model small --clipboard
🎙️  Whisper Term - File Processing Mode
========================================

🔄 Loading model 'small'...
✅ Model loaded successfully

🎵 Processing: meeting.wav
⏱️  Duration: 2m 34s
🔄 Transcribing...

████████████████████████████████████████ 100%

✅ Transcription completed

📝 Result: "Good morning everyone, welcome to today's meeting..."

📋 Copied to clipboard!
💾 Saved to: data/recordings/2025-07/2025-07-08/meeting.txt

✅ Done!
```

#### **Timeout Mode**
```bash
$ whisper-term --record --model turbo --timeout 30s
🎙️  Whisper Term - Timed Recording Mode
========================================

🔄 Loading model 'turbo'...
✅ Model loaded successfully

🎤 Recording started (30s timeout)...
   Press ENTER to stop early
   Press Ctrl+C to cancel

🔴 Recording... (00:15s) [⏰ 15s remaining]
Audio Level: ██████████ 100%

⏰ Timeout reached - stopping recording
⏹️  Recording stopped (30.0s)
🔄 Processing transcription...
✅ Transcription completed

📝 Result: "This is a longer recording that was automatically stopped after thirty seconds..."

📋 Copied to clipboard!
💾 Saved to: data/recordings/2025-07/2025-07-08/20250708_210630.txt

✅ Done!
```

### Technical Implementation

#### **Enhanced CLI Arguments**
```python
parser.add_argument(
    '--record', '-r',
    action='store_true',
    help='Start recording immediately (direct mode)'
)

parser.add_argument(
    '--clipboard', '-c',
    action='store_true',
    default=True,  # Default to True in direct mode
    help='Copy transcription to clipboard'
)

parser.add_argument(
    '--timeout', '-t',
    type=str,
    metavar='DURATION',
    help='Auto-stop recording after duration (e.g., 30s, 2m, 1h)'
)

parser.add_argument(
    '--file', '-f',
    type=str,
    metavar='PATH',
    help='Process audio file instead of recording'
)

parser.add_argument(
    '--output-format',
    choices=['text', 'json', 'srt', 'vtt'],
    default='text',
    help='Output format for transcription'
)

parser.add_argument(
    '--quiet', '-q',
    action='store_true',
    help='Minimal output (just the transcription)'
)
```

#### **Clipboard Integration**
```python
import pyperclip  # Cross-platform clipboard library

class ClipboardManager:
    """Handles clipboard operations across platforms."""
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard."""
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"⚠️  Failed to copy to clipboard: {e}")
            return False
    
    def get_from_clipboard(self) -> str:
        """Get text from clipboard."""
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"⚠️  Failed to read from clipboard: {e}")
            return ""
```

#### **Direct Mode Handler**
```python
class DirectModeHandler:
    """Handles direct CLI mode without interactive interface."""
    
    def __init__(self, args):
        self.args = args
        self.clipboard_manager = ClipboardManager()
        
    def run_direct_recording(self):
        """Execute direct recording mode."""
        print("🎙️  Whisper Term - Direct Recording Mode")
        print("=" * 40)
        
        # Initialize components
        recorder = AudioRecorder()
        engine = TranscriptionEngine(
            model_name=self.args.model,
            language=self.args.language
        )
        
        # Start recording
        print("\n🎤 Recording started automatically...")
        print("   Press ENTER to stop recording")
        print("   Press Ctrl+C to cancel")
        
        recorder.start_recording()
        
        # Wait for user input or timeout
        if self.args.timeout:
            self._wait_with_timeout()
        else:
            input()  # Wait for ENTER
        
        # Stop and process
        audio_data = recorder.stop_recording()
        result = engine.transcribe(audio_data)
        
        # Handle output
        self._handle_output(result['text'])
        
    def _handle_output(self, transcription: str):
        """Handle transcription output and clipboard."""
        if self.args.quiet:
            print(transcription)
        else:
            print(f"\n📝 Result: \"{transcription}\"")
        
        if self.args.clipboard:
            if self.clipboard_manager.copy_to_clipboard(transcription):
                if not self.args.quiet:
                    print("📋 Copied to clipboard!")
        
        if not self.args.quiet:
            print("✅ Done!")
```

#### **Output Formats**
```python
class OutputFormatter:
    """Format transcription output in different formats."""
    
    def format_text(self, result: dict) -> str:
        """Plain text format."""
        return result['text']
    
    def format_json(self, result: dict) -> str:
        """JSON format with metadata."""
        return json.dumps({
            'text': result['text'],
            'language': result['language'],
            'timestamp': datetime.now().isoformat(),
            'segments': result.get('segments', [])
        }, indent=2)
    
    def format_srt(self, result: dict) -> str:
        """SRT subtitle format."""
        srt_content = ""
        for i, segment in enumerate(result.get('segments', []), 1):
            start = self._format_time(segment['start'])
            end = self._format_time(segment['end'])
            text = segment['text'].strip()
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
        return srt_content
```

### Integration with Existing Code

#### **Main Entry Point Modification**
```python
def main():
    parser = argparse.ArgumentParser(...)
    args = parser.parse_args()
    
    # Direct mode handling
    if args.record or args.file:
        direct_handler = DirectModeHandler(args)
        if args.file:
            direct_handler.run_file_processing()
        else:
            direct_handler.run_direct_recording()
        return
    
    # Existing interactive mode
    app = WhisperTermApp()
    app.run()
```

## Impact

### **User Experience Benefits**
- **Faster workflow**: No menu navigation for quick transcriptions
- **Automation friendly**: Can be scripted and integrated into workflows
- **Clipboard integration**: Instant access to transcribed text
- **Batch processing**: Handle multiple files efficiently
- **Power user features**: Timeout, format options, quiet mode

### **Use Cases**
- **Quick voice notes**: `whisper-term -r -m base` for fast transcription
- **Meeting transcription**: `whisper-term -f meeting.wav -m small -c`
- **Automation scripts**: Integrate into other tools and workflows
- **Development**: Quick testing and debugging of speech recognition
- **Accessibility**: Voice-to-text for users with typing difficulties

### **Development Benefits**
- **Modular design**: Separate direct mode from interactive mode
- **Cross-platform**: Clipboard works on Windows, macOS, Linux
- **Extensible**: Easy to add new output formats and features
- **Backward compatible**: Existing interactive mode unchanged

## Next Steps

1. **Clipboard Library**: Add `pyperclip` dependency for cross-platform clipboard
2. **Timeout Handler**: Implement duration parsing and timeout mechanism
3. **Output Formats**: Create formatters for JSON, SRT, VTT
4. **File Processing**: Add batch file processing capability
5. **Direct Mode**: Implement DirectModeHandler class
6. **CLI Enhancement**: Extend argument parser with new options
7. **Integration**: Connect direct mode to existing business logic
8. **Testing**: Test across different platforms and use cases