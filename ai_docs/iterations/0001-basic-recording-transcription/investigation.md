# Investigation – Basic Recording and Transcription

## Current Status
No existing implementation. Starting from scratch for Whisper Term project.

## Pain Points / Opportunities
- Need a simple, working proof-of-concept for the core functionality
- Users want to quickly test speech-to-text transcription without complex setup
- Foundation needed for future real-time streaming features
- Basic file organization and session management required

## Research & Benchmarks
Based on `ai_docs/investigations/local-whisper-model.md`:
- OpenAI Whisper library provides robust local speech recognition
- SoundDevice is the recommended audio recording library for 2025
- Base model provides good balance of speed and accuracy for initial implementation
- Non-streaming approach simplifies implementation significantly

## Proposed Direction
Create a minimal viable product with:
1. Simple terminal interface with start/stop recording
2. Hardcoded settings (base model, English language)
3. Record-then-transcribe workflow (no streaming)
4. Basic file organization in `data/` folder
5. Session-based storage with timestamps

## Decision
**PROCEED** with basic implementation to establish core functionality.
Link to `design.md` for detailed solution.
