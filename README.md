# Whisper Term

A terminal app for whisper speech to text model.

## Features

- Interactive speech-to-text transcription using OpenAI Whisper
- Local processing with automatic model management
- Organized session storage with date-based folders
- Simple terminal interface with keyboard controls

## Installation

### Prerequisites

- Python 3.8-3.11 (recommended: 3.10.x for best compatibility)
- uv package manager (see installation instructions below)

### Installing uv

uv is a fast Python package manager written in Rust. Install it using:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative methods:**
```bash
# With pip
pip install uv

# With Homebrew (macOS)
brew install uv
```

### Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd whisper-term
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Run the application:
```bash
uv run whisper-term
```

### Using uv for Development

uv provides modern Python project management with automatic virtual environment handling:

```bash
# Add new dependencies
uv add package-name

# Remove dependencies
uv remove package-name

# Run scripts in project environment
uv run python main.py

# Install the project in development mode
uv sync
```

## Usage

1. Launch the application:
```bash
uv run whisper-term
```

2. Press **ENTER** to start recording
3. Speak into your microphone
4. Press **ENTER** again to stop recording
5. Wait for transcription to complete
6. Find your audio and text files in the `data/recordings/` folder

## File Organization

The application automatically organizes your recordings:

```
data/
├── models/              # Whisper model cache
│   └── base.pt         # Downloaded base model
└── recordings/         # Session recordings
    └── 2025-07/
        └── 2025-07-08/
            ├── 20250708_143022.wav
            └── 20250708_143022.txt
```

## Development

This project uses uv for dependency management and virtual environment handling. Key benefits:

- **Fast**: 10-100x faster than pip for package installation
- **Modern**: Uses pyproject.toml and uv.lock for deterministic builds
- **Automatic**: Handles virtual environments automatically
- **Comprehensive**: Replaces pip, pip-tools, pipx, poetry, and more

