"""Main application class for Whisper Term."""

import sys
import threading
import time
from typing import Optional

from .audio_recorder import AudioRecorder
from .transcription_engine import TranscriptionEngine
from .file_manager import FileManager
from .session_manager import SessionManager


class WhisperTermApp:
    """Main application class for Whisper Term."""
    
    def __init__(self):
        """Initialize the application."""
        print("🎙️  Whisper Term - Speech-to-Text Terminal App")
        print("="*50)
        
        # Initialize components
        self.audio_recorder = AudioRecorder(sample_rate=16000, channels=1)
        self.transcription_engine = TranscriptionEngine(model_name="base", language="english")
        self.file_manager = FileManager()
        self.session_manager = SessionManager(self.file_manager)
        
        # Application state
        self.running = True
        self.recording = False
        
        print("✅ Application initialized successfully")
        print("💡 Press Ctrl+C to exit the application")
        print("="*50)
    
    def display_instructions(self) -> None:
        """Display usage instructions."""
        print("\n📋 INSTRUCTIONS:")
        print("• Press ENTER to start/stop recording")
        print("• Type 'q' or 'quit' to exit")
        print("• Speak clearly into your microphone")
        print("• Wait for transcription to complete after stopping")
        print()
    
    def start_recording(self) -> None:
        """Start audio recording."""
        if self.recording:
            print("⚠️  Already recording!")
            return
        
        self.recording = True
        self.audio_recorder.start_recording()
    
    def stop_recording(self) -> None:
        """Stop recording and process transcription."""
        if not self.recording:
            print("⚠️  Not currently recording!")
            return
        
        self.recording = False
        
        # Stop recording and get audio data
        audio_data = self.audio_recorder.stop_recording()
        
        if audio_data is None:
            print("❌ No audio data recorded")
            return
        
        # Process transcription
        result = self.transcription_engine.transcribe(audio_data)
        transcription = result.get("text", "")
        
        if transcription:
            print(f"\n💬 Transcription:")
            print(f"   {transcription}")
        else:
            print("⚠️  No speech detected or transcription failed")
        
        # Create session and save files
        session = self.session_manager.create_session(
            audio_data=audio_data,
            transcription=transcription,
            sample_rate=self.audio_recorder.sample_rate
        )
        
        if session:
            self.session_manager.print_session_summary(session)
        
        print("\n" + "="*50)
    
    def handle_user_input(self) -> None:
        """Handle user input in a separate thread."""
        while self.running:
            try:
                user_input = input().strip().lower()
                
                if user_input in ['q', 'quit', 'exit']:
                    self.shutdown()
                    break
                elif user_input == '' or user_input == 'r':  # Empty input (ENTER) or 'r' for record
                    if self.recording:
                        self.stop_recording()
                    else:
                        self.start_recording()
                elif user_input == 'h' or user_input == 'help':
                    self.display_instructions()
                else:
                    print("💡 Press ENTER to start/stop recording, 'q' to quit, 'h' for help")
                    
            except EOFError:
                # Handle Ctrl+D
                self.shutdown()
                break
            except KeyboardInterrupt:
                # Handle Ctrl+C
                self.shutdown()
                break
    
    def run(self) -> None:
        """Run the main application loop."""
        try:
            self.display_instructions()
            
            print("🎤 Ready! Press ENTER to start recording...")
            
            # Start input handler in a separate thread
            input_thread = threading.Thread(target=self.handle_user_input, daemon=True)
            input_thread.start()
            
            # Main loop
            while self.running:
                time.sleep(0.1)  # Small delay to prevent high CPU usage
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Received interrupt signal...")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ Application error: {e}")
            self.shutdown()
    
    def shutdown(self) -> None:
        """Shutdown the application gracefully."""
        print("\n🔄 Shutting down...")
        
        # Stop recording if active
        if self.recording:
            print("⏹️  Stopping active recording...")
            self.stop_recording()
        
        # No cleanup needed for input() method
        
        # Display final statistics
        storage_info = self.file_manager.get_storage_info()
        print(f"\n📊 Session Statistics:")
        print(f"   Total recordings: {storage_info['total_files']}")
        print(f"   Storage used: {storage_info['total_size_mb']:.1f} MB")
        print(f"   Data location: {storage_info['recordings_dir']}")
        
        print("\n👋 Thank you for using Whisper Term!")
        self.running = False
        sys.exit(0)
    
    def show_recent_sessions(self, limit: int = 5) -> None:
        """
        Show recent recording sessions.
        
        Args:
            limit: Number of recent sessions to show
        """
        print(f"\n📋 Recent Sessions (last {limit}):")
        print("-" * 40)
        
        sessions = self.session_manager.get_recent_sessions(limit)
        
        if not sessions:
            print("   No recent sessions found")
        else:
            for i, session in enumerate(sessions, 1):
                print(f"{i}. {session['timestamp']}")
                print(f"   Duration: {session['duration']}")
                print(f"   Preview: {session['transcription_preview']}")
                print()
    
    def get_model_info(self) -> dict:
        """Get information about the current model."""
        return self.transcription_engine.get_model_info()
    
    def get_app_status(self) -> dict:
        """Get current application status."""
        return {
            "running": self.running,
            "recording": self.recording,
            "model_info": self.get_model_info(),
            "storage_info": self.file_manager.get_storage_info()
        }