# 🎤🤖 Alpha Voice Assistant

An advanced AI-powered voice assistant built with **DeepSeek AI**, **Speech Recognition**, and **Text-to-Speech** capabilities. Features real-time voice interaction, intelligent error handling, and a modern web interface.

## ✨ Features

- 🎤 **Multiple Input Methods**: Text, audio file upload, live microphone recording with start/stop controls
- 🧠 **AI-Powered Responses**: Using DeepSeek-V3 via OpenRouter API with intelligent fallback
- 🔊 **Text-to-Speech**: Adjustable speech speed and voice output using pyttsx3
- ⚙️ **Customizable Settings**: AI creativity level, response length, and voice speed controls
- 🎯 **Quick Actions**: Pre-defined conversation starters and common interactions
- 📱 **Modern UI**: Clean, responsive Gradio interface with custom CSS styling
- 🔄 **Smart Fallback**: Automatic demo mode when API is unavailable
- 🛡️ **Error Handling**: Robust error handling with user-friendly messages
- 🎙️ **Background Recording**: Non-blocking audio recording with threading
- 📡 **API Validation**: Automatic API key testing and status reporting

## 🛠️ Tech Stack

### Frontend & UI
- **[Gradio](https://gradio.app/)** - Modern web interface framework
- **Custom CSS** - Enhanced styling with gradients and animations
- **HTML/Markdown** - Rich text formatting and layout

### AI & Language Models
- **[OpenRouter API](https://openrouter.ai/)** - AI model routing and access
- **[DeepSeek-V3](https://deepseek.com/)** - Advanced language model (deepseek-chat-v3-0324:free)
- **JSON** - Data serialization for API communication

### Audio Processing
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** - Speech-to-text conversion
- **[Google Speech Recognition API](https://cloud.google.com/speech-to-text)** - Cloud-based transcription
- **[pyttsx3](https://pypi.org/project/pyttsx3/)** - Text-to-speech synthesis
- **[PyAudio](https://pypi.org/project/PyAudio/)** - Real-time audio I/O

### Backend & Core
- **[Python 3.11+](https://python.org/)** - Core programming language
- **[Requests](https://requests.readthedocs.io/)** - HTTP client for API calls
- **[Threading](https://docs.python.org/3/library/threading.html)** - Concurrent audio processing
- **[OS/Environment Variables](https://docs.python.org/3/library/os.html)** - Configuration management
- **[Warnings](https://docs.python.org/3/library/warnings.html)** - Error suppression and handling
- **[Time](https://docs.python.org/3/library/time.html)** - Timing and delays
- **[Random](https://docs.python.org/3/library/random.html)** - Demo response generation

### Development & Deployment
- **[Git](https://git-scm.com/)** - Version control
- **[GitHub](https://github.com/)** - Repository hosting
- **[pip](https://pip.pypa.io/)** - Package management
- **[requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files)** - Dependency specification

### Architecture Features
- **Event-driven UI** - Gradio component interactions
- **State management** - Chat history and session persistence
- **Error boundaries** - Graceful degradation and fallback modes
- **Responsive design** - Adaptive layout for different screen sizes
- **Background processing** - Non-blocking audio operations
- **API abstraction** - Clean separation of AI service logic

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Microphone access (for voice input)
- Internet connection (for AI responses)
- OpenRouter API key (optional - has demo mode)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BSRohit20/alpha-voice-bot.git
   cd alpha-voice-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/keys)
   - Update the `API_KEY` variable in `voice_bot.py` or set environment variable:
     ```bash
     # Windows PowerShell
     $env:OPENROUTER_API_KEY="your_api_key_here"
     
     # Windows CMD
     set OPENROUTER_API_KEY=your_api_key_here
     
     # Linux/Mac
     export OPENROUTER_API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   python voice_bot.py
   ```

5. **Open in browser** - The app will automatically open at `http://localhost:7861`

## 🌐 Deployment

### Local Development (Full Features)

1. **Clone the repository**
   ```bash
   git clone https://github.com/BSRohit20/alpha-voice-bot.git
   cd alpha-voice-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/keys)
   - Set environment variable:
     ```bash
     # Windows
     set OPENROUTER_API_KEY=your_api_key_here
     
     # Linux/Mac
     export OPENROUTER_API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   python voice_bot.py
   ```

### Cloud Deployment

> **Note**: For cloud deployment (Hugging Face Spaces), some microphone features may be limited due to platform constraints.

## 🎛️ Usage Guide

### 💬 Text Chat
- Type your message in the large text area
- Click "📤 Send" button or press Enter to get AI responses
- Use the "🗑️ Clear Chat" button to reset conversation history

### 🎤 Voice Input Options

#### Quick Voice (Instant)
- Click "⚡ Quick Voice" for immediate 5-second voice capture
- Best for short commands or questions
- Automatically processes and responds

#### Controlled Recording
- Click "🎤 Start Recording" to begin voice capture
- Speak your message (no time limit)
- Click "⏹️ Stop Recording" when finished
- Perfect for longer conversations or detailed questions

#### Audio File Upload
- Click "🎙️ Upload Audio File" area
- Upload WAV, MP3, or M4A files
- Supports various audio formats and quality levels

### ⚙️ Settings & Controls

#### AI Creativity Level (🧠)
- **0.0-0.3**: Focused, factual responses
- **0.4-0.7**: Balanced creativity and accuracy
- **0.8-1.0**: Creative, diverse responses

#### Speech Speed (🔊)
- **0.5x**: Slow, clear speech
- **1.0x**: Normal speed (default)
- **2.0x**: Fast speech

#### Response Length (📝)
- **100-500 tokens**: Short, concise answers
- **500-1024 tokens**: Detailed responses (default)
- **1024-2000 tokens**: Comprehensive, in-depth answers

### 🎯 Quick Actions
- **👋 Say Hello**: Start a friendly conversation
- **😄 Tell Joke**: Get a random joke from the AI
- **❓ Get Help**: Learn about the bot's capabilities
- **ℹ️ Bot Info**: Get information about the assistant

## 🏗️ Project Architecture

### 📁 File Structure
```
alpha-voice-bot/
├── voice_bot.py           # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore           # Git ignore rules
└── assets/              # Additional resources (if any)
```

### 🔧 Core Components

#### 1. Audio Processing Pipeline
```python
Microphone → SpeechRecognition → Google API → Text
Audio File → SpeechRecognition → Google API → Text
Text → pyttsx3 → Audio Output
```

#### 2. AI Processing Flow
```python
User Input → Message History → OpenRouter API → DeepSeek Model → Response
API Failure → Fallback → Demo Mode → Offline Responses
```

#### 3. UI Component Hierarchy
```python
Gradio Blocks
├── Header (Gradient Design)
├── Main Row
│   ├── Chat Column
│   │   ├── Chatbot Interface
│   │   ├── Text Input
│   │   ├── Send/Clear Buttons
│   │   └── Audio Controls
│   └── Control Column
│       ├── Settings Panel
│       └── Quick Actions
└── Event Handlers
```

## 🛠️ Technical Implementation

### 🔌 API Integration
- **OpenRouter Endpoint**: `https://openrouter.ai/api/v1/chat/completions`
- **Model**: `deepseek/deepseek-chat-v3-0324:free`
- **Authentication**: Bearer token via API key
- **Error Handling**: Automatic fallback to demo mode

### 🎵 Audio Processing
- **Input Formats**: WAV, MP3, M4A, FLAC
- **Speech Recognition**: Google Web Speech API
- **Voice Synthesis**: System TTS engines via pyttsx3
- **Threading**: Background processing for non-blocking UI

### 🎨 UI Technologies
- **Framework**: Gradio 4.x
- **Styling**: Custom CSS with gradient themes
- **Theme**: Soft theme with custom overrides
- **Responsive**: Adaptive layout for different screen sizes

### 💾 State Management
- **Chat History**: Gradio State component
- **Session Persistence**: In-memory during runtime
- **Recording State**: Global variables with thread safety
- **Configuration**: Runtime parameter adjustment

## 🔧 Configuration Options

### Environment Variables
```bash
OPENROUTER_API_KEY=your_api_key_here    # Required for AI features
GRADIO_SERVER_PORT=7861                 # Custom port (optional)
GRADIO_ANALYTICS_ENABLED=False          # Disable analytics
```

### Runtime Configuration
```python
# In voice_bot.py
API_KEY = "your_key_here"               # Direct API key setting
MODEL = "deepseek/deepseek-chat-v3-0324:free"  # AI model selection
```

### Server Configuration
```python
demo.launch(
    server_name="127.0.0.1",           # Local access only
    server_port=7861,                  # Custom port
    inbrowser=True,                    # Auto-open browser
    share=False                        # Disable public sharing
)
```

## 🔧 Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required for AI responses)

### Customization

You can modify these settings in `voice_bot.py`:
- Default AI model
- UI colors and styling
- Voice recognition parameters
- Response templates

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues:
1. Check that your API key is properly set
2. Ensure all dependencies are installed
3. Try the offline demo mode first
4. Open an issue on GitHub with error details

## 🙏 Acknowledgments

- **DeepSeek AI** for the language model
- **OpenRouter** for API access
- **Gradio** for the web interface
- **Google** for speech recognition services

---

**🎉 Enjoy chatting with your AI voice assistant!**
