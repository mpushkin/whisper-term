"""Session management for recording sessions."""

from datetime import datetime
from pathlib import Path
from typing import Optional
import numpy as np

from .models import RecordingSession
from .file_manager import FileManager


class SessionManager:
    """Manages recording sessions and their metadata."""
    
    def __init__(self, file_manager: FileManager):
        """
        Initialize the session manager.
        
        Args:
            file_manager: FileManager instance for file operations
        """
        self.file_manager = file_manager
        self.current_session: Optional[RecordingSession] = None
    
    def create_session(self, audio_data: np.ndarray, transcription: str, 
                      sample_rate: int = 16000) -> Optional[RecordingSession]:
        """
        Create a new recording session.
        
        Args:
            audio_data: Recorded audio data
            transcription: Transcribed text
            sample_rate: Audio sample rate
            
        Returns:
            RecordingSession object or None if failed
        """
        try:
            # Generate timestamp
            timestamp = datetime.now()
            
            # Get file paths
            audio_path, text_path = self.file_manager.get_session_paths(timestamp)
            
            # Calculate duration
            duration = len(audio_data) / sample_rate if audio_data is not None else 0.0
            
            # Create session object
            session = RecordingSession(
                timestamp=timestamp,
                audio_path=audio_path,
                text_path=text_path,
                transcription=transcription,
                duration=duration
            )
            
            # Save audio and text files
            audio_saved = self.file_manager.save_audio(audio_data, audio_path, sample_rate)
            text_saved = self.file_manager.save_text(transcription, text_path)
            
            if audio_saved and text_saved:
                self.current_session = session
                print(f"📁 Session created: {session.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                return session
            else:
                print("❌ Failed to save session files")
                return None
                
        except Exception as e:
            print(f"❌ Error creating session: {e}")
            return None
    
    def get_current_session(self) -> Optional[RecordingSession]:
        """Get the current recording session."""
        return self.current_session
    
    def get_session_info(self, session: RecordingSession) -> dict:
        """
        Get formatted information about a session.
        
        Args:
            session: RecordingSession object
            
        Returns:
            Dictionary with session information
        """
        return {
            "timestamp": session.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": f"{session.duration:.2f}s",
            "audio_file": session.audio_path.name,
            "text_file": session.text_path.name,
            "transcription_length": len(session.transcription),
            "transcription_preview": session.transcription[:100] + "..." if len(session.transcription) > 100 else session.transcription,
            "audio_exists": session.audio_path.exists(),
            "text_exists": session.text_path.exists(),
        }
    
    def print_session_summary(self, session: RecordingSession) -> None:
        """
        Print a summary of the recording session.
        
        Args:
            session: RecordingSession object
        """
        print("\n" + "="*50)
        print("📋 RECORDING SESSION SUMMARY")
        print("="*50)
        
        info = self.get_session_info(session)
        
        print(f"⏰ Timestamp: {info['timestamp']}")
        print(f"⏱️  Duration: {info['duration']}")
        print(f"📁 Audio file: {info['audio_file']}")
        print(f"📝 Text file: {info['text_file']}")
        print(f"📊 Transcription: {info['transcription_length']} characters")
        
        if session.transcription:
            print(f"\n💬 Transcription:")
            print(f"   {info['transcription_preview']}")
        else:
            print("\n⚠️  No transcription available")
        
        print(f"\n📂 Files saved in: {session.audio_path.parent}")
        print("="*50)
    
    def load_session(self, audio_path) -> Optional[RecordingSession]:
        """
        Load a session from existing files.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            RecordingSession object or None if failed
        """
        try:
            audio_path = Path(audio_path)
            text_path = audio_path.with_suffix('.txt')
            
            if not audio_path.exists():
                print(f"❌ Audio file not found: {audio_path}")
                return None
            
            # Load transcription
            transcription = self.file_manager.load_text(text_path) or ""
            
            # Get timestamp from filename
            timestamp_str = audio_path.stem  # YYYYMMDD_HHMMSS
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            except ValueError:
                # Fallback to file modification time
                timestamp = datetime.fromtimestamp(audio_path.stat().st_mtime)
            
            # Calculate duration (would need to load audio file for accurate duration)
            # For now, use a placeholder
            duration = 0.0
            
            session = RecordingSession(
                timestamp=timestamp,
                audio_path=audio_path,
                text_path=text_path,
                transcription=transcription,
                duration=duration
            )
            
            return session
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return None
    
    def get_recent_sessions(self, limit: int = 5) -> list:
        """
        Get recent recording sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session information dictionaries
        """
        sessions_data = self.file_manager.get_recent_sessions(limit)
        sessions = []
        
        for session_data in sessions_data:
            if session_data["exists"]:
                session = self.load_session(session_data["audio_path"])
                if session:
                    sessions.append(self.get_session_info(session))
        
        return sessions