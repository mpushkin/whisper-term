"""Clipboard operations for cross-platform text copying."""

import sys
from typing import Optional


class ClipboardManager:
    """Handles clipboard operations across platforms."""
    
    def __init__(self):
        """Initialize clipboard manager."""
        self._pyperclip = None
        self._load_pyperclip()
    
    def _load_pyperclip(self) -> None:
        """Load pyperclip library with fallback handling."""
        try:
            import pyperclip
            self._pyperclip = pyperclip
        except ImportError:
            print("⚠️  pyperclip not available - clipboard functionality disabled")
            self._pyperclip = None
        except Exception as e:
            print(f"⚠️  Failed to load clipboard support: {e}")
            self._pyperclip = None
    
    def copy_to_clipboard(self, text: str) -> bool:
        """
        Copy text to clipboard.
        
        Args:
            text: Text to copy to clipboard
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
        
        if self._pyperclip is None:
            print("⚠️  Clipboard not available - text not copied")
            return False
        
        try:
            self._pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"⚠️  Failed to copy to clipboard: {e}")
            return False
    
    def get_from_clipboard(self) -> Optional[str]:
        """
        Get text from clipboard.
        
        Returns:
            Text from clipboard or None if failed
        """
        if self._pyperclip is None:
            return None
        
        try:
            return self._pyperclip.paste()
        except Exception as e:
            print(f"⚠️  Failed to read from clipboard: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if clipboard functionality is available."""
        return self._pyperclip is not None