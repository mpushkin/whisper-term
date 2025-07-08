"""Direct CLI mode handler for immediate recording."""

import sys
from datetime import datetime
from typing import Optional

from .audio_recorder import AudioRecorder
from .transcription_engine import TranscriptionEngine
from .file_manager import FileManager
from .session_manager import SessionManager
from .clipboard import ClipboardManager


class DirectModeHandler:
    """Handles direct CLI mode without interactive interface."""
    
    def __init__(self, model_name: str = "base", language: str = "english", 
                 clipboard_enabled: bool = True):
        """
        Initialize direct mode handler.
        
        Args:
            model_name: Whisper model to use
            language: Language for transcription
            clipboard_enabled: Whether to copy to clipboard
        """
        self.model_name = model_name
        self.language = language
        self.clipboard_enabled = clipboard_enabled
        self.clipboard_manager = ClipboardManager() if clipboard_enabled else None
        
        # Initialize components
        self.audio_recorder = AudioRecorder(sample_rate=16000, channels=1)
        self.transcription_engine = TranscriptionEngine(
            model_name=model_name, 
            language=language
        )
        self.file_manager = FileManager()
        self.session_manager = SessionManager(self.file_manager)
    
    def run_direct_recording(self) -> bool:
        """
        Execute direct recording mode.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print("🎙️  Whisper Term - Direct Mode")
            print("=" * 30)
            
            # Load model
            print(f"\n🔄 Loading model '{self.model_name}'...")
            # Model loading happens during first transcription
            
            # Start recording
            print("\n🎤 Recording... Press ENTER to stop")
            print("   Press Ctrl+C to cancel")
            
            self.audio_recorder.start_recording()
            
            # Wait for user to stop recording
            try:
                input()  # Wait for ENTER
            except KeyboardInterrupt:
                print("\n\n⚠️  Recording cancelled by user")
                self.audio_recorder.stop_recording()
                return False
            
            # Stop recording and get audio data
            audio_data = self.audio_recorder.stop_recording()
            
            if audio_data is None:
                print("❌ No audio data recorded")
                return False
            
            # Save audio file immediately for reliability
            timestamp = datetime.now()
            audio_path, text_path = self.file_manager.get_session_paths(timestamp)
            
            print(f"💾 Saving audio file...")
            audio_saved = self.file_manager.save_audio(
                audio_data, 
                audio_path, 
                self.audio_recorder.sample_rate
            )
            
            if not audio_saved:
                print("❌ Failed to save audio file")
                return False
            
            # Process transcription
            print("🔄 Processing transcription...")
            result = self.transcription_engine.transcribe(audio_data)
            transcription = result.get("text", "")
            
            if not transcription:
                print("⚠️  No speech detected or transcription failed")
                transcription = ""
            
            # Display result
            if transcription:
                print(f"\n✅ Transcription: \"{transcription}\"")
            else:
                print("\n⚠️  No transcription generated")
            
            # Copy to clipboard
            if self.clipboard_enabled and transcription:
                if self.clipboard_manager and self.clipboard_manager.copy_to_clipboard(transcription):
                    print("📋 Copied to clipboard!")
                else:
                    print("⚠️  Failed to copy to clipboard")
            
            # Save text file
            text_saved = self.file_manager.save_text(transcription, text_path)
            if not text_saved:
                print("⚠️  Failed to save text file")
            
            # Create session record
            session = self.session_manager.create_session(
                audio_data=audio_data,
                transcription=transcription,
                sample_rate=self.audio_recorder.sample_rate
            )
            
            if session:
                duration = self.audio_recorder.get_duration(audio_data)
                print(f"\n📊 Session completed:")
                print(f"   Duration: {duration:.2f}s")
                print(f"   Audio: {audio_path}")
                print(f"   Text: {text_path}")
            
            print("\n✅ Done!")
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error during direct recording: {e}")
            return False
    
    def get_status(self) -> dict:
        """Get current status of direct mode handler."""
        return {
            "model_name": self.model_name,
            "language": self.language,
            "clipboard_enabled": self.clipboard_enabled,
            "clipboard_available": self.clipboard_manager.is_available() if self.clipboard_manager else False
        }