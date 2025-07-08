"""Transcription engine using OpenAI Whisper."""

import whisper
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any


class TranscriptionEngine:
    """Handles speech-to-text transcription using OpenAI Whisper."""
    
    def __init__(self, model_name: str = "base", language: str = "english"):
        """
        Initialize the transcription engine.
        
        Args:
            model_name: Whisper model to use (tiny, base, small, medium, large)
            language: Language for transcription (english, auto, etc.)
        """
        self.model_name = model_name
        self.language = language
        self.model = None
        self.model_cache_dir = Path("data/models")
        
    def _load_model(self) -> None:
        """Load the Whisper model if not already loaded."""
        if self.model is None:
            print(f"Loading Whisper model '{self.model_name}'...")
            
            # Create cache directory if it doesn't exist
            self.model_cache_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # Load model with custom cache directory
                self.model = whisper.load_model(
                    name=self.model_name,
                    download_root=str(self.model_cache_dir)
                )
                print(f"✅ Model '{self.model_name}' loaded successfully")
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                raise
    
    def transcribe(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Dictionary containing transcription results
        """
        if audio_data is None or len(audio_data) == 0:
            return {"text": "", "language": self.language}
        
        # Load model if not already loaded
        self._load_model()
        
        print("🔄 Processing transcription...")
        
        try:
            # Transcribe with specified language
            options = {
                "language": self.language if self.language != "auto" else None,
                "task": "transcribe",
                "fp16": False,  # Use fp32 for better compatibility
            }
            
            result = self.model.transcribe(audio_data, **options)
            
            # Extract text and clean it up
            text = result["text"].strip()
            
            if text:
                print(f"✅ Transcription completed: {len(text)} characters")
            else:
                print("⚠️  No speech detected in audio")
            
            return {
                "text": text,
                "language": result.get("language", self.language),
                "segments": result.get("segments", []),
            }
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return {
                "text": "",
                "language": self.language,
                "error": str(e)
            }
    
    def transcribe_from_file(self, audio_file: Path) -> Dict[str, Any]:
        """
        Transcribe audio from a file.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Dictionary containing transcription results
        """
        if not audio_file.exists():
            return {"text": "", "language": self.language, "error": "File not found"}
        
        # Load model if not already loaded
        self._load_model()
        
        print(f"🔄 Transcribing file: {audio_file.name}")
        
        try:
            options = {
                "language": self.language if self.language != "auto" else None,
                "task": "transcribe",
                "fp16": False,
            }
            
            result = self.model.transcribe(str(audio_file), **options)
            
            text = result["text"].strip()
            
            if text:
                print(f"✅ File transcription completed: {len(text)} characters")
            else:
                print("⚠️  No speech detected in file")
            
            return {
                "text": text,
                "language": result.get("language", self.language),
                "segments": result.get("segments", []),
            }
            
        except Exception as e:
            print(f"❌ File transcription error: {e}")
            return {
                "text": "",
                "language": self.language,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        if self.model is None:
            return {"model_name": self.model_name, "loaded": False}
        
        return {
            "model_name": self.model_name,
            "language": self.language,
            "loaded": True,
            "cache_dir": str(self.model_cache_dir)
        }