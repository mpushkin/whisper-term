"""Main entry point for Whisper Term."""

import sys
import argparse
from pathlib import Path

from .app import WhisperTermApp


def main():
    """Main entry point for the application."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Whisper Term - Speech-to-Text Terminal App",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  whisper-term              # Start the interactive app
  whisper-term --help       # Show this help message

Controls:
  Space                     # Start/stop recording
  Ctrl+C                    # Exit application

For more information, visit: https://github.com/user/whisper-term
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Whisper Term 0.1.0'
    )
    
    parser.add_argument(
        '--model',
        default='base',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model to use (default: base)'
    )
    
    parser.add_argument(
        '--language',
        default='english',
        help='Language for transcription (default: english)'
    )
    
    parser.add_argument(
        '--data-dir',
        default='data',
        help='Directory for data storage (default: data)'
    )
    
    parser.add_argument(
        '--recent',
        type=int,
        metavar='N',
        help='Show N recent sessions and exit'
    )
    
    args = parser.parse_args()
    
    # Handle --recent option
    if args.recent:
        try:
            from .file_manager import FileManager
            from .session_manager import SessionManager
            
            file_manager = FileManager(args.data_dir)
            session_manager = SessionManager(file_manager)
            
            print(f"📋 Recent Sessions (last {args.recent}):")
            print("-" * 40)
            
            sessions = session_manager.get_recent_sessions(args.recent)
            
            if not sessions:
                print("   No recent sessions found")
            else:
                for i, session in enumerate(sessions, 1):
                    print(f"{i}. {session['timestamp']}")
                    print(f"   Duration: {session['duration']}")
                    print(f"   Preview: {session['transcription_preview']}")
                    print()
            
            return
            
        except Exception as e:
            print(f"❌ Error showing recent sessions: {e}")
            sys.exit(1)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    if sys.version_info >= (3, 12):
        print("⚠️  Warning: Python 3.12+ may have compatibility issues with Whisper")
        print("   Recommended: Python 3.8-3.11")
    
    # Create data directory if it doesn't exist
    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Initialize and run the application
        app = WhisperTermApp()
        
        # Override default settings if provided
        if args.model != 'base':
            app.transcription_engine.model_name = args.model
        
        if args.language != 'english':
            app.transcription_engine.language = args.language
        
        if args.data_dir != 'data':
            app.file_manager.base_data_dir = Path(args.data_dir)
            app.file_manager.recordings_dir = app.file_manager.base_data_dir / "recordings"
            app.file_manager.models_dir = app.file_manager.base_data_dir / "models"
            app.file_manager._ensure_directories()
        
        # Run the application
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()