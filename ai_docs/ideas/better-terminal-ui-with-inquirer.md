# Idea: Better Terminal UI with Inquirer

## Context

The current Whisper Term application uses a simple `input()` method for user interaction, which works but is basic and not very discoverable. Users need to remember commands like 'q' for quit, 'h' for help, etc. A more sophisticated terminal UI would improve user experience and make the application more intuitive.

## Proposal

Replace the current text-based input system with **python-inquirer**, which provides rich interactive terminal UI components including menus, checkboxes, and navigation. This would transform Whisper Term from a command-driven interface to a menu-driven interface.

### Enhanced Terminal UI Flow

#### **Main Menu**
```
🎙️  Whisper Term - Speech-to-Text Terminal App
==================================================

? What would you like to do?
❯ 🎤 Start Recording Session
  📁 Browse Recent Sessions
  ⚙️  Model Management
  📊 View Statistics
  ❓ Help
  🚪 Exit
```

#### **Recording Session Flow**
```
🎤 Recording Session
====================

? Recording controls:
❯ ▶️  Start Recording
  ⏹️  Stop Recording (disabled until recording)
  📄 View Current Session
  🔙 Back to Main Menu

Status: Ready to record
Model: turbo (English)
Output: data/recordings/2025-07/2025-07-08/
```

#### **Model Management Menu**
```
⚙️  Model Management
=====================

? Select an option:
❯ 📥 Download New Model
  🔄 Change Current Model
  🗑️  Delete Unused Models
  📋 View Model Information
  🔙 Back to Main Menu

Current Model: turbo (774MB)
Available Models: tiny, base, small, medium, large, turbo
```

#### **Model Selection Interface**
```
🔄 Change Current Model
=======================

? Select Whisper model: (Use arrow keys)
❯ ● turbo     (774MB) - Latest, optimized for English [CURRENT]
  ○ base      (142MB) - Good balance of speed and accuracy
  ○ small     (461MB) - Better accuracy, slower
  ○ medium    (1.5GB) - High accuracy
  ○ large     (2.9GB) - Highest accuracy, slowest
  ○ tiny      (39MB)  - Fastest, lowest accuracy

? Select language:
❯ ● english   [CURRENT]
  ○ auto      (Auto-detect)
  ○ spanish
  ○ french
  ○ german
  ○ chinese
  ○ japanese
```

#### **Recent Sessions Browser**
```
📁 Browse Recent Sessions
=========================

? Select session to view: (Use arrow keys, Enter to select)
❯ 📅 2025-07-08 20:53:00 (5.2s) - "Hello, this is a test recording..."
  📅 2025-07-08 20:45:12 (3.8s) - "Testing the whisper application..."
  📅 2025-07-08 20:32:45 (12.1s) - "This is a longer recording to test..."
  📅 2025-07-08 19:15:33 (2.3s) - "Quick test message..."
  📅 2025-07-07 18:22:11 (7.9s) - "Yesterday's recording session..."

? What would you like to do with this session?
❯ 👀 View Full Transcription
  🎵 Play Audio File
  📝 Re-transcribe with Different Model
  🗑️  Delete Session
  🔙 Back to Sessions List
```

#### **Statistics Dashboard**
```
📊 Statistics Dashboard
=======================

📈 Usage Statistics:
   Total Sessions: 15
   Total Duration: 2m 34s
   Average Session: 10.3s
   
💾 Storage Information:
   Audio Files: 45.2 MB
   Text Files: 0.8 MB
   Total Storage: 46.0 MB
   
🧠 Model Information:
   Current Model: turbo (774MB)
   Models Downloaded: 3
   Models Storage: 1.4 GB
   
📊 Recent Activity:
   Today: 5 sessions
   This week: 12 sessions
   This month: 15 sessions

? Options:
❯ 🔄 Refresh Statistics
  🗑️  Clean Up Old Sessions
  📤 Export Statistics
  🔙 Back to Main Menu
```

#### **Live Recording Interface**
```
🎤 Recording in Progress
========================

🔴 RECORDING... (00:12s)

Audio Level: ████████░░ 80%
Model: turbo (English)
Output: 20250708_205300.wav

? Controls:
❯ ⏹️  Stop Recording
  ⏸️  Pause Recording
  🔇 Toggle Mute Monitor
  📊 Audio Settings

Press Enter to select, Esc to force stop
```

#### **Real-time Transcription View**
```
🎤 Live Transcription
=====================

🔴 RECORDING... (00:08s)

📝 Transcription (Live):
   "Hello, this is a test of the whisper
   application. I'm speaking into the
   microphone to see how well it..."

🎵 Audio Level: ████████░░ 80%
⚙️  Model: turbo (English)
📁 Output: 20250708_205300.wav

? Controls:
❯ ⏹️  Stop & Save
  ⏸️  Pause
  🔄 Restart
  ⚙️  Settings
```

### Technical Implementation

#### **Core Components**
- **MenuManager**: Handles menu navigation and state
- **SessionBrowser**: Interactive session browsing and management
- **ModelManager**: Model selection and management interface
- **LiveRecordingUI**: Real-time recording interface with progress
- **StatisticsUI**: Dashboard for usage and storage statistics

#### **Inquirer Integration**
```python
import inquirer
from inquirer import themes

class WhisperTermUI:
    def __init__(self):
        self.theme = themes.GreenPassion
        
    def main_menu(self):
        choices = [
            "🎤 Start Recording Session",
            "📁 Browse Recent Sessions", 
            "⚙️  Model Management",
            "📊 View Statistics",
            "❓ Help",
            "🚪 Exit"
        ]
        
        question = inquirer.List(
            'action',
            message="What would you like to do?",
            choices=choices,
            carousel=True
        )
        
        return inquirer.prompt([question], theme=self.theme)
```

## Impact

### **User Experience Benefits**
- **Discoverable**: All options visible in menus, no need to remember commands
- **Intuitive**: Arrow key navigation feels natural for terminal users
- **Visual**: Rich formatting with emojis and status indicators
- **Guided**: Clear workflows for complex operations like model management

### **Feature Expansion**
- **Session Management**: Easy browsing and management of past recordings
- **Model Management**: User-friendly interface for downloading and switching models
- **Statistics**: Visual dashboard for usage tracking
- **Settings**: Configuration management through menus

### **Development Benefits**
- **Maintainable**: Clear separation between UI and business logic
- **Extensible**: Easy to add new menu options and workflows
- **Testable**: UI components can be tested independently
- **Professional**: Modern terminal applications use rich UIs

## Next Steps

1. **Proof of Concept**: Create basic menu navigation with inquirer
2. **Main Menu**: Implement core menu structure and navigation
3. **Recording Interface**: Design interactive recording session flow
4. **Model Management**: Build model selection and management UI
5. **Session Browser**: Create session browsing and management interface
6. **Statistics Dashboard**: Implement usage and storage statistics view
7. **Integration**: Connect rich UI to existing business logic
8. **Testing**: Ensure all menu flows work correctly across platforms