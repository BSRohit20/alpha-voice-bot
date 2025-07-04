import gradio as gr
import requests
import json
import pyttsx3
import threading
import warnings
import os
import time

# Try to import speech recognition and handle missing pyaudio gracefully
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ Speech recognition not available - microphone features will be disabled")

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'

# 🔐 OpenRouter API Key and model  
# ⚠️ IMPORTANT: Set your OpenRouter API key as environment variable
# Get your key from: https://openrouter.ai/keys
API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY_HERE")
MODEL = "deepseek/deepseek-chat-v3-0324:free"

def query_openrouter(messages, temperature=0.7, max_tokens=1024):
    """Query the OpenRouter API with the given messages"""
    # Check if API key is set
    if API_KEY == "YOUR_OPENROUTER_API_KEY_HERE" or not API_KEY:
        return demo_response(messages[-1]["content"])
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:7872",
        "X-Title": "Alpha Voice Bot"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    try:
        print(f"🔄 Sending request to OpenRouter...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, 
            data=json.dumps(data),
            timeout=30  # Add timeout
        )
        response.raise_for_status()
        result = response.json()
        print(f"✅ Got response from OpenRouter")
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "⚠️ Connection error: Unable to connect to OpenRouter. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "⚠️ Timeout error: Request took too long. Please try again."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return "⚠️ Authentication error: Invalid API key. Please check your OpenRouter API key."
        elif response.status_code == 429:
            return "⚠️ Rate limit exceeded: Too many requests. Please wait and try again."
        else:
            return f"⚠️ HTTP error {response.status_code}: {str(e)}"
    except Exception as e:
        return f"⚠️ OpenRouter error: {str(e)}"

def demo_response(user_input):
    """Provide demo responses when API key is not configured"""
    import random
    
    user_lower = user_input.lower().strip()
    
    # Math operations
    if "2+2" in user_lower or "2 + 2" in user_lower:
        return "2 + 2 = 4. That's basic math! 😊"
    
    # Simple questions and responses
    responses = {
        "hello": "Hello! I'm your Alpha Voice Bot. How can I help you today?",
        "hi": "Hi there! Nice to meet you. What would you like to talk about?",
        "how are you": "I'm doing great! Thanks for asking. How are you doing?",
        "what is your name": "I'm Alpha Voice Bot, your AI assistant. What's your name?",
        "goodbye": "Goodbye! Have a wonderful day!",
        "bye": "See you later! Take care!",
        "help": "I can help you with conversations, questions, math problems, and more! Try asking me anything.",
        "test": "Test successful! Voice recognition and chat are working perfectly!",
        "thank you": "You're very welcome! Happy to help.",
        "thanks": "No problem! Glad I could assist.",
        "who are you": "I'm Alpha Voice Bot, an AI assistant that can chat with you via text or voice.",
        "what can you do": "I can have conversations, answer questions, solve problems, tell jokes, and help with various tasks!",
        "joke": "Why don't scientists trust atoms? Because they make up everything! 😄",
        "tell me a joke": "What do you call a bear with no teeth? A gummy bear! 🐻",
        "weather": "I don't have access to current weather data, but I hope it's nice where you are!",
        "time": "I don't have access to the current time, but I hope you're having a good day!",
        "how old are you": "I'm a digital AI, so I don't age like humans do. But I'm here to help!",
        "where are you from": "I exist in the digital realm, but I'm happy to chat with you from anywhere!",
    }
    
    # Check for keyword matches
    for key, response in responses.items():
        if key in user_lower:
            return response
    
    # Handle questions
    if "?" in user_input:
        question_responses = [
            f"That's an interesting question about '{user_input}'. While I can give basic responses, I'd love to provide more detailed answers with a proper AI connection!",
            f"You asked: '{user_input}' - I can try to help with simple responses, but for detailed assistance, I'd need a full AI connection.",
            f"Great question! I can provide basic responses to '{user_input}', but for comprehensive answers, an AI API would be helpful.",
        ]
        return random.choice(question_responses)
    
    # Default responses
    friendly_replies = [
        f"You said: '{user_input}'. I heard you clearly! I can provide basic responses and conversation.",
        f"I understand you mentioned: '{user_input}'. I'm working in basic mode but can still chat with you!",
        f"Thanks for saying: '{user_input}'. I can respond to simple conversations and questions!",
        f"You shared: '{user_input}'. I'm here to chat, even in basic mode!",
        f"I got your message: '{user_input}'. While I can give simple responses, I'm still happy to talk with you!",
    ]
    
    return random.choice(friendly_replies)

def speak_text(text, speed=1.0):
    """Convert text to speech using pyttsx3 with adjustable speed"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', int(200 * speed))  # Adjust speech rate
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech synthesis error: {e}")

def transcribe_audio(file_path):
    """Transcribe audio file to text using Google Speech Recognition"""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return "Speech recognition not available in this deployment"
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

def record_microphone():
    """Record audio from microphone with stop control"""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return "Microphone recording not available in this deployment"
    
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Recording... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Record with a reasonable timeout
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=10)
        print("🔄 Processing speech...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    except sr.WaitTimeoutError:
        return "No speech detected - please try again"

# Global variables for recording
recording_active = False
recorded_audio = None
recording_thread = None

def record_audio_thread():
    """Background thread for recording audio"""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return
    
    global recorded_audio, recording_active
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Background recording started...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while recording_active:
                try:
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=None)
                    recorded_audio = audio
                    break
                except sr.WaitTimeoutError:
                    if not recording_active:
                        break
                    continue
    except Exception as e:
        print(f"Recording thread error: {e}")

def record_microphone_simple():
    """Simple microphone recording that starts immediately"""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return "Microphone recording not available in this deployment"
    
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
        print("🔄 Processing speech...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    except sr.WaitTimeoutError:
        return "No speech detected"
    except Exception as e:
        return f"Recording error: {e}"

def start_recording():
    """Start recording audio in background"""
    global recording_active, recorded_audio, recording_thread
    recording_active = True
    recorded_audio = None
    
    # Start recording in background thread
    recording_thread = threading.Thread(target=record_audio_thread, daemon=True)
    recording_thread.start()
    
    return "🎤 Recording... Speak now!", gr.update(visible=False), gr.update(visible=True)

def stop_recording_and_process(chat_history, temperature, voice_speed, max_tokens):
    """Stop recording and process the audio"""
    global recording_active, recorded_audio
    recording_active = False
    
    # Wait a moment for recording to stop
    time.sleep(0.5)
    
    try:
        if recorded_audio is not None:
            recognizer = sr.Recognizer()
            text = recognizer.recognize_google(recorded_audio)
            print(f"🔄 Recognized: {text}")
            
            if text and text.strip():
                result = handle_input(text, chat_history, temperature, voice_speed, max_tokens)
                return result[0], result[1], "🎤 Ready to record", gr.update(visible=True), gr.update(visible=False)
            else:
                chat_history.append(("🎤 Voice Recording", "⚠️ No speech detected"))
                return chat_history, "", "🎤 Ready to record", gr.update(visible=True), gr.update(visible=False)
        else:
            chat_history.append(("🎤 Voice Recording", "⚠️ No audio recorded"))
            return chat_history, "", "🎤 Ready to record", gr.update(visible=True), gr.update(visible=False)
            
    except sr.UnknownValueError:
        chat_history.append(("🎤 Voice Recording", "⚠️ Could not understand audio"))
        return chat_history, "", "🎤 Ready to record", gr.update(visible=True), gr.update(visible=False)
    except Exception as e:
        chat_history.append(("🎤 Recording failed", f"⚠️ Error: {e}"))
        return chat_history, "", "🎤 Ready to record", gr.update(visible=True), gr.update(visible=False)

def handle_input(user_input, chat_history, temperature, voice_speed, max_tokens):
    """Handle text input and generate response with enhanced parameters"""
    if not user_input:
        return chat_history, ""

    # Build conversation history
    messages = [{"role": "system", "content": "You are Alpha Voice Assistant, a helpful and intelligent AI. Keep responses conversational and engaging. You can help with questions, tasks, creative writing, problem-solving, and casual conversation."}]
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": user_input})

    # Get AI response with custom parameters
    reply = query_openrouter(messages, temperature, max_tokens)
    
    # If the reply indicates a connection error, fallback to demo mode
    if "Connection error" in reply or "Timeout error" in reply or "HTTP error" in reply:
        reply = "⚠️ " + reply + "\n\n🔄 Switching to offline mode...\n\n" + demo_response(user_input)
    
    chat_history.append((user_input, reply))
    
    # Speak the response in a separate thread with custom speed
    threading.Thread(target=speak_text, args=(reply, voice_speed), daemon=True).start()
    
    return chat_history, ""

def handle_audio(audio_file, chat_history, temperature, voice_speed, max_tokens):
    """Handle audio input and generate response"""
    if audio_file is None:
        return chat_history, ""
    
    try:
        text = transcribe_audio(audio_file)
        if text and text not in ["Could not understand audio", "Listening timeout"]:
            return handle_input(text, chat_history, temperature, voice_speed, max_tokens)
        else:
            chat_history.append(("🎙️ Audio input", f"⚠️ {text}"))
            return chat_history, ""
    except Exception as e:
        chat_history.append(("🎙️ Audio input failed", f"⚠️ Error: {e}"))
        return chat_history, ""

def handle_microphone(chat_history, temperature, voice_speed, max_tokens):
    """Handle live microphone input"""
    try:
        text = record_microphone_simple()
        if text and text not in ["Could not understand audio", "No speech detected"]:
            return handle_input(text, chat_history, temperature, voice_speed, max_tokens)
        else:
            chat_history.append(("🎙️ Microphone input", f"⚠️ {text}"))
            return chat_history, ""
    except Exception as e:
        chat_history.append(("🎙️ Microphone failed", f"⚠️ Error: {e}"))
        return chat_history, ""

def quick_response(message, chat_history, temperature, voice_speed, max_tokens):
    """Handle quick action buttons"""
    return handle_input(message, chat_history, temperature, voice_speed, max_tokens)

def clear_chat():
    """Clear the chat history"""
    return []

# 🎨 Enhanced Web App UI
def create_interface():
    with gr.Blocks(
        css="""
        .gradio-container {
            max-width: 1400px !important; 
            margin: auto;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            text-align: center; 
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            margin-bottom: 20px;
            color: white;
        }
        .chat-container {
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .control-panel {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .feature-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-card {
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 5px;
        }
        .mic-button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }
        .send-button {
            background: linear-gradient(45deg, #4834d4, #686de0) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }
        .stop-button {
            background: linear-gradient(45deg, #e74c3c, #c0392b) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
        }
        .recording-status {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 8px;
            text-align: center;
            font-weight: bold;
        }
        /* Equal column layout */
        .equal-columns {
            display: flex !important;
            gap: 20px !important;
        }
        .equal-columns > div {
            flex: 1 !important;
        }
        /* Larger text input styling */
        .large-textbox textarea {
            min-height: 120px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        """,
        title="🎤 Alpha Voice Assistant - AI Powered Voice Bot",
        theme=gr.themes.Soft()
    ) as demo:
        
        gr.Markdown("""
        <div class="header">
            <h1 style="font-size: 3em; margin-bottom: 10px;">🎤🤖 Alpha Voice Assistant</h1>
            <p style="font-size: 1.3em; opacity: 0.9;">Advanced AI-Powered Voice Recognition & Response System</p>
            <p style="font-size: 1em; opacity: 0.8;">Built with DeepSeek AI • Speech Recognition • Text-to-Speech</p>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 💬 Conversation Interface")
                    chatbot = gr.Chatbot(
                        label="",
                        height=500,
                        bubble_full_width=False,
                        show_label=False,
                        avatar_images=("🧑‍💻", "🤖")
                    )
                
                chat_state = gr.State([])
                
                # Larger text input area
                text_input = gr.Textbox(
                    placeholder="💭 Type your message here or use voice input...",
                    show_label=False,
                    container=False,
                    lines=4,
                    max_lines=6,
                    elem_classes="large-textbox"
                )
                
                with gr.Row():
                    send_btn = gr.Button("📤 Send", scale=1, elem_classes="send-button", size="lg")
                    clear_btn = gr.Button("🗑️ Clear Chat", scale=1, variant="secondary")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        audio_input = gr.Audio(
                            type="filepath",
                            label="🎙️ Upload Audio File (WAV, MP3, M4A)",
                            show_label=True
                        )
                    with gr.Column(scale=1):
                        # Recording status
                        recording_status = gr.Textbox(
                            value="🎤 Ready to record",
                            show_label=False,
                            interactive=False,
                            container=False
                        )
                        
                        # Recording control buttons
                        with gr.Row():
                            start_rec_btn = gr.Button("🎤 Start Recording", scale=1, elem_classes="mic-button", size="sm")
                            stop_rec_btn = gr.Button("⏹️ Stop Recording", scale=1, variant="stop", size="sm", visible=False)
                        
                        # Legacy mic button (for quick recording)
                        mic_btn = gr.Button("⚡ Quick Voice", scale=1, variant="secondary", size="sm")
            
            with gr.Column(scale=1):
                gr.Markdown("### ⚙️ Control Panel")
                
                with gr.Group(elem_classes="control-panel"):
                    temperature = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.7,
                        step=0.1,
                        label="🧠 AI Creativity Level",
                        info="0 = Focused, 1 = Creative"
                    )
                    
                    voice_speed = gr.Slider(
                        minimum=0.5,
                        maximum=2.0,
                        value=1.0,
                        step=0.1,
                        label="🔊 Speech Speed",
                        info="Adjust text-to-speech speed"
                    )
                    
                    max_tokens = gr.Slider(
                        minimum=100,
                        maximum=2000,
                        value=1024,
                        step=100,
                        label="📝 Response Length",
                        info="Maximum words in AI response"
                    )
                
                gr.Markdown("### 🎯 Quick Actions")
                with gr.Row():
                    hello_btn = gr.Button("👋 Say Hello", size="sm")
                    joke_btn = gr.Button("😄 Tell Joke", size="sm")
                with gr.Row():
                    help_btn = gr.Button("❓ Get Help", size="sm")
                    info_btn = gr.Button("ℹ️ Bot Info", size="sm")
                


        # Event handlers
        text_input.submit(
            fn=handle_input,
            inputs=[text_input, chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        send_btn.click(
            fn=handle_input,
            inputs=[text_input, chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        audio_input.change(
            fn=handle_audio,
            inputs=[audio_input, chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        # Recording control buttons
        start_rec_btn.click(
            fn=start_recording,
            outputs=[recording_status, start_rec_btn, stop_rec_btn]
        )
        
        stop_rec_btn.click(
            fn=stop_recording_and_process,
            inputs=[chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input, recording_status, start_rec_btn, stop_rec_btn]
        )
        
        # Quick voice button (original functionality)
        mic_btn.click(
            fn=handle_microphone,
            inputs=[chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        # Quick action buttons
        hello_btn.click(
            fn=quick_response,
            inputs=[gr.State("Hello! How are you today?"), chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        joke_btn.click(
            fn=quick_response,
            inputs=[gr.State("Tell me a funny joke please!"), chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        help_btn.click(
            fn=quick_response,
            inputs=[gr.State("What can you help me with? Show me your capabilities."), chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        info_btn.click(
            fn=quick_response,
            inputs=[gr.State("Tell me about yourself and your features."), chat_state, temperature, voice_speed, max_tokens],
            outputs=[chatbot, text_input]
        )
        
        clear_btn.click(
            fn=clear_chat,
            outputs=[chatbot]
        ).then(
            fn=lambda: [],
            outputs=[chat_state]
        )

    return demo

if __name__ == "__main__":
    print("🚀 Starting Alpha Voice Bot...")
    print("🔧 System Check:")
    print("   1. ✅ Python packages loaded")
    print("   2. ✅ Speech recognition ready")
    print("   3. ✅ Text-to-speech ready")
    
    # Test internet connection
    try:
        response = requests.get("https://httpbin.org/status/200", timeout=5)
        print("   4. ✅ Internet connection working")
    except:
        print("   4. ⚠️ Internet connection issues detected")
    
    # Test OpenRouter API key
    if API_KEY and API_KEY != "YOUR_OPENROUTER_API_KEY_HERE":
        print("   5. ✅ API key configured")
    else:
        print("   5. ⚠️ API key not configured - using demo mode")
    
    print("\n📋 Instructions:")
    print("   • Allow microphone access when prompted")
    print("   • Use Start/Stop recording for longer voice input")
    print("   • Use Quick Voice for short voice input")
    print("   • Bot will fallback to offline mode if connection fails")
    
    demo = create_interface()
    demo.launch(
        share=False,  # Disable share to avoid HuggingFace warnings
        inbrowser=False,  # Don't open browser in production
        show_error=True,
        server_name="0.0.0.0",  # Allow external connections
        server_port=int(os.getenv("PORT", 7860)),  # Use Railway's PORT or default
        quiet=False,  # Show URL and output
        favicon_path=None  # Disable favicon to reduce 404 errors
    )
