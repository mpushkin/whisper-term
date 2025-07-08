"""Audio recording functionality using sounddevice."""

import sounddevice as sd
import numpy as np
from typing import Optional
import threading
import queue


class AudioRecorder:
    """Handles audio recording using sounddevice."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        """
        Initialize the audio recorder.
        
        Args:
            sample_rate: Sample rate in Hz (16000 is optimal for Whisper)
            channels: Number of audio channels (1 for mono)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.audio_queue = queue.Queue()
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback function for audio recording."""
        if status:
            print(f"Audio callback status: {status}")
        
        if self.recording:
            self.audio_queue.put(indata.copy())
    
    def start_recording(self) -> None:
        """Start audio recording."""
        if self.recording:
            print("Already recording!")
            return
            
        self.recording = True
        self.audio_data = []
        
        # Clear any existing data in the queue
        while not self.audio_queue.empty():
            self.audio_queue.get()
        
        print("🔴 Recording started... Press SPACE to stop")
        
        # Start the audio stream
        self.stream = sd.InputStream(
            callback=self._audio_callback,
            channels=self.channels,
            samplerate=self.sample_rate,
            dtype=np.float32
        )
        self.stream.start()
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop audio recording and return the recorded data.
        
        Returns:
            Recorded audio data as numpy array, or None if no recording
        """
        if not self.recording:
            print("Not currently recording!")
            return None
        
        self.recording = False
        
        # Stop the audio stream
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        
        # Collect all audio data from the queue
        while not self.audio_queue.empty():
            self.audio_data.append(self.audio_queue.get())
        
        if not self.audio_data:
            print("No audio data recorded!")
            return None
        
        # Concatenate all audio chunks
        audio_array = np.concatenate(self.audio_data, axis=0)
        
        # Convert to mono if stereo
        if len(audio_array.shape) > 1 and audio_array.shape[1] > 1:
            audio_array = np.mean(audio_array, axis=1)
        
        # Flatten to 1D array
        audio_array = audio_array.flatten()
        
        duration = len(audio_array) / self.sample_rate
        print(f"⏹️  Recording stopped. Duration: {duration:.2f} seconds")
        
        return audio_array
    
    def get_duration(self, audio_data: np.ndarray) -> float:
        """Get the duration of audio data in seconds."""
        if audio_data is None:
            return 0.0
        return len(audio_data) / self.sample_rate
    
    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self.recording