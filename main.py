"""Main entry point for Whisper Term (alternative to using package)."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from whisper_term.main import main

if __name__ == "__main__":
    main()