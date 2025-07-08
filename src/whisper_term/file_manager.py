"""File management for audio recordings and transcriptions."""

import os
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional
import numpy as np
from scipy.io import wavfile


class FileManager:
    """Handles file operations for recordings and transcriptions."""
    
    def __init__(self, base_data_dir: str = "data"):
        """
        Initialize the file manager.
        
        Args:
            base_data_dir: Base directory for data storage
        """
        self.base_data_dir = Path(base_data_dir)
        self.recordings_dir = self.base_data_dir / "recordings"
        self.models_dir = self.base_data_dir / "models"
        
        # Create directories if they don't exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.recordings_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def get_session_paths(self, timestamp: datetime) -> Tuple[Path, Path]:
        """
        Get the file paths for a recording session.
        
        Args:
            timestamp: Timestamp for the session
            
        Returns:
            Tuple of (audio_path, text_path)
        """
        # Create date-based folder structure: YYYY-MM/YYYY-MM-DD/
        year_month = timestamp.strftime("%Y-%m")
        date = timestamp.strftime("%Y-%m-%d")
        
        session_dir = self.recordings_dir / year_month / date
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamp-based filenames: YYYYMMDD_HHMMSS
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        audio_path = session_dir / f"{timestamp_str}.wav"
        text_path = session_dir / f"{timestamp_str}.txt"
        
        return audio_path, text_path
    
    def save_audio(self, audio_data: np.ndarray, audio_path: Path, 
                   sample_rate: int = 16000) -> bool:
        """
        Save audio data to a WAV file.
        
        Args:
            audio_data: Audio data as numpy array
            audio_path: Path to save the audio file
            sample_rate: Sample rate of the audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Normalize audio data to prevent clipping
            if audio_data.dtype == np.float32 or audio_data.dtype == np.float64:
                # Convert float audio to int16 for WAV format
                audio_data = np.clip(audio_data, -1.0, 1.0)
                audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save as WAV file
            wavfile.write(str(audio_path), sample_rate, audio_data)
            
            print(f"💾 Audio saved: {audio_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
            return False
    
    def save_text(self, text: str, text_path: Path) -> bool:
        """
        Save transcription text to a file.
        
        Args:
            text: Transcription text
            text_path: Path to save the text file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure the directory exists
            text_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save as UTF-8 text file
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"📝 Text saved: {text_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving text: {e}")
            return False
    
    def load_text(self, text_path: Path) -> Optional[str]:
        """
        Load transcription text from a file.
        
        Args:
            text_path: Path to the text file
            
        Returns:
            Text content or None if error
        """
        try:
            if not text_path.exists():
                return None
            
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            print(f"❌ Error loading text: {e}")
            return None
    
    def get_recent_sessions(self, limit: int = 10) -> list:
        """
        Get a list of recent recording sessions.
        
        Args:
            limit: Maximum number of sessions to return
            
        Returns:
            List of session directories, most recent first
        """
        sessions = []
        
        try:
            # Walk through the recordings directory
            for year_month_dir in self.recordings_dir.iterdir():
                if not year_month_dir.is_dir():
                    continue
                    
                for date_dir in year_month_dir.iterdir():
                    if not date_dir.is_dir():
                        continue
                    
                    # Find all WAV files in this date directory
                    wav_files = list(date_dir.glob("*.wav"))
                    
                    for wav_file in wav_files:
                        # Get corresponding text file
                        text_file = wav_file.with_suffix(".txt")
                        
                        sessions.append({
                            "date": date_dir.name,
                            "audio_path": wav_file,
                            "text_path": text_file,
                            "timestamp": wav_file.stem,
                            "exists": wav_file.exists() and text_file.exists()
                        })
            
            # Sort by timestamp (most recent first)
            sessions.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return sessions[:limit]
            
        except Exception as e:
            print(f"❌ Error getting recent sessions: {e}")
            return []
    
    def get_storage_info(self) -> dict:
        """
        Get information about storage usage.
        
        Returns:
            Dictionary with storage statistics
        """
        try:
            total_size = 0
            total_files = 0
            
            # Calculate total size of recordings
            for root, dirs, files in os.walk(self.recordings_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        total_size += file_path.stat().st_size
                        total_files += 1
            
            return {
                "total_size_bytes": total_size,
                "total_size_mb": total_size / (1024 * 1024),
                "total_files": total_files,
                "recordings_dir": str(self.recordings_dir),
                "models_dir": str(self.models_dir)
            }
            
        except Exception as e:
            print(f"❌ Error getting storage info: {e}")
            return {
                "total_size_bytes": 0,
                "total_size_mb": 0,
                "total_files": 0,
                "recordings_dir": str(self.recordings_dir),
                "models_dir": str(self.models_dir),
                "error": str(e)
            }