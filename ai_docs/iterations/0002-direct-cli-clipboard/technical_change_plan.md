# Technical Change Plan – Direct CLI with Clipboard

## Summary
Implement minimal direct CLI mode with `--record` flag that bypasses interactive mode, starts recording immediately, and copies transcription to clipboard. See `design.md` for architecture details.

## Code Changes (by module / file)
| Path | Change Type | Description |
|------|-------------|-------------|
| src/whisper_term/clipboard.py | new | ClipboardManager class using pyperclip |
| src/whisper_term/direct_mode.py | new | DirectModeHandler class for CLI mode |
| src/whisper_term/main.py | modify | Add CLI arguments and direct mode routing |
| src/whisper_term/app.py | modify | Accept model/language parameters |
| src/whisper_term/transcription_engine.py | modify | Accept model/language in constructor |
| pyproject.toml | modify | Add pyperclip dependency |
| README.md | modify | Update with direct CLI usage examples |

## Data & Schema Changes
No database or schema changes. File organization remains the same.

## API / Interface Changes
**New CLI Arguments:**
- `--record, -r` - Start recording immediately (boolean flag)
- `--clipboard, -c` - Copy to clipboard (boolean, default True)
- Enhanced `--model, -m` - Model selection with validation
- Enhanced `--language, -l` - Language selection

**Public Functions:**
- `DirectModeHandler.run_direct_recording()` - Main direct mode flow
- `ClipboardManager.copy_to_clipboard()` - Cross-platform clipboard copy

## Dependencies & Configuration
**New Dependencies:**
```
pyperclip>=1.8.0  # Cross-platform clipboard operations
```

**Configuration Changes:**
- TranscriptionEngine constructor accepts model_name and language
- WhisperTermApp constructor accepts model_name and language
- CLI arguments override hardcoded defaults

## Detailed Steps
1. **Add pyperclip dependency**
   - Update pyproject.toml with pyperclip>=1.8.0
   - Run uv sync to install

2. **Implement ClipboardManager**
   - Create src/whisper_term/clipboard.py
   - Implement copy_to_clipboard with error handling
   - Add graceful fallback for clipboard failures

3. **Implement DirectModeHandler**
   - Create src/whisper_term/direct_mode.py
   - Implement run_direct_recording method
   - Save audio file immediately after recording stops
   - Integrate with existing AudioRecorder, TranscriptionEngine, FileManager

4. **Enhance CLI Arguments**
   - Modify src/whisper_term/main.py argument parser
   - Add --record, --clipboard flags
   - Enhance --model, --language with validation

5. **Update Component Constructors**
   - Modify TranscriptionEngine to accept model_name, language
   - Modify WhisperTermApp to accept model_name, language
   - Ensure backward compatibility

6. **Route Direct Mode**
   - Update main() function to check --record flag
   - Route to DirectModeHandler if --record is present
   - Otherwise use existing interactive mode

7. **Update Documentation**
   - Add direct mode examples to README.md
   - Update help text with new CLI options

## Testing Strategy
**Unit Tests:**
- `test_clipboard.py` - Test clipboard operations with mocking
- `test_direct_mode.py` - Test DirectModeHandler flow
- `test_main.py` - Test CLI argument parsing and routing

**Integration Tests:**
- End-to-end direct mode recording and clipboard copy
- Model parameter validation
- Error handling for clipboard failures
- Audio file saving reliability (immediate save after recording)

**Manual Verification:**
- Test on macOS, Linux, Windows (if available)
- Verify clipboard functionality across platforms
- Test with different model sizes and languages
- Ensure interactive mode still works

## Rollback / Migration Plan
**Rollback Strategy:**
- Remove pyperclip dependency from pyproject.toml
- Revert changes to main.py, app.py, transcription_engine.py
- Delete clipboard.py and direct_mode.py
- No data migration needed

**Migration Notes:**
- No breaking changes to existing functionality
- Existing users continue to use interactive mode
- New CLI flags are optional and backward compatible

## Risks & Mitigations (technical only)

### **Clipboard Library Risk**
- **Risk**: pyperclip may fail on headless systems or without display
- **Mitigation**: Wrap in try-catch, continue with warning if clipboard fails

### **Model Parameter Risk**
- **Risk**: Invalid model names cause whisper to crash
- **Mitigation**: Validate model names against known choices, provide clear error messages

### **Constructor Changes Risk**
- **Risk**: Changing component constructors might break existing code
- **Mitigation**: Use default parameters to maintain backward compatibility

### **Platform Compatibility Risk**
- **Risk**: Clipboard behavior varies across platforms
- **Mitigation**: Test on multiple platforms, handle platform-specific exceptions

### **Threading Risk**
- **Risk**: Clipboard operations might interfere with audio recording
- **Mitigation**: Perform clipboard operations after recording/transcription complete

### **Import Risk**
- **Risk**: pyperclip import might fail on some systems
- **Mitigation**: Import pyperclip only when needed, provide fallback behavior

### **Data Loss Risk**
- **Risk**: Application crash during transcription loses audio data
- **Mitigation**: Save audio file immediately after recording stops, before transcription processing begins
