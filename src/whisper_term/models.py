"""Data models for Whisper Term."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class RecordingSession:
    """Represents a recording session with metadata."""
    
    timestamp: datetime
    audio_path: Path
    text_path: Path
    transcription: str
    duration: float
    
    def __post_init__(self):
        """Ensure paths are Path objects."""
        if not isinstance(self.audio_path, Path):
            self.audio_path = Path(self.audio_path)
        if not isinstance(self.text_path, Path):
            self.text_path = Path(self.text_path)