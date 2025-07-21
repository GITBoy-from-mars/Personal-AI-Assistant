# VisionMinds AI Assistant

🌟 **Project Overview**  
Welcome to **VisionMinds AI Assistant**, a sophisticated desktop voice assistant designed to streamline your daily digital interactions. This project combines a robust Python backend with a responsive PyQt5 graphical user interface, powered by cutting-edge AI models for natural language understanding and task automation. Say goodbye to manual clicks and hello to intuitive voice commands!

---

## ✨ Features

- **Voice-Activated Control**: Interact with your computer using natural language commands.
- **Intelligent Decision-Making (DMM)**: A powerful First Layer Decision-Making Model (built with Gemini AI) accurately categorizes your queries into general, real-time, or specific task commands.
- **Conversational AI**: Engage in natural conversations and get answers to a wide range of questions using advanced Google Gemini.
- **Real-time Information Retrieval**: Get up-to-date news, facts, and information by leveraging real-time Google searches.
- **System Automation**: Control system functions like volume (mute, unmute, up, down) with simple voice commands.
- **Application & Webpage Management**: Open and close applications or browse specific websites effortlessly.
- **YouTube Integration**: Play videos or search for content directly on YouTube.
- **Content Generation**: Request the AI to write various types of content (letters, code, essays, poems) and open them in Notepad.
- **Image Generation (Placeholder)**: Future capability to generate images based on your prompts.
- **Dynamic UI**: A responsive PyQt5 GUI with real-time status updates and visual feedback (e.g., listening animations).
- **Cross-Platform Compatibility**: Designed to run on Windows, with potential for broader compatibility where Python and Chromium are supported.

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+ 👉 [Download Python](https://www.python.org/)
- Google Chrome Browser 👉 [Download Chrome](https://www.google.com/chrome/)
- Git (optional, for cloning) 👉 [Download Git](https://git-scm.com/)

---

### Installation

#### 1. Clone the Repository (if applicable):

```bash
git clone https://github.com/GITBoy-from-mars/Personal-AI-Assistant
cd VisionMinds-AI-Assistant
```


---

#### 2. Create a Virtual Environment (Recommended):

```bash
python -m venv .venv
```

---

#### 3. Activate the Virtual Environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

---

#### 4. Install Dependencies:

```bash
pip install pygame python-dotenv selenium mtranslate AppOpener beautifulsoup4 rich keyboard edge-tts webdriver-manager google-generativeai
```

---

#### 5. Set up Environment Variables:

Create a file named `.env` in the root directory and add your keys:

```dotenv
Username="YourName"
Assistantname="Jarvis" # Or any name you prefer
GroqAPIKey="YOUR_GROQ_API_KEY" # if you are Using Groq
AssistantVoice="en-US-JennyNeural" # e.g., "en-US-GuyNeural", "en-US-AriaNeural"
InputLanguage="en-US" # e.g., "en-GB", "hi-IN"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
# HuggingFaceAPIKey="YOUR_HUGGING_FACE_API_KEY" # If implementing image generation
```

---

#### 6. Prepare Graphics Files:

Ensure the following image files are available in the `Frontend/Graphics` directory:

- `Jarvis.gif` *(animated GIF for assistant's visual feedback)*
- `Mic_on.png`
- `Mic_off.png`
- `Home.png`
- `Chats.png`
- `Minimize2.png`
- `Maximize.png`
- `Restore.png`
- `Close.png`

> 🖼️ You can use placeholder images or create simple ones if not available.

---

### ✅ Running the Application

Run the main application using:

```bash
python Main.py
```

The PyQt5 GUI window should appear, and the assistant will be ready to receive commands.

---

## 💡 Usage

- **Activate Microphone**: Click the mic icon on the home screen to toggle listening.
- **Give Commands**: Speak clearly into your mic when it says "Listening..."
- **Navigate**: Use the "Home" and "Chat" buttons in the top bar to switch screens.
- **Interact with AI**: Ask questions, open apps, generate content, control the system, and more!

---

## 🤝 Contributing

Contributions are welcome!



## 🙏 Acknowledgements

- **Google Gemini API** – for the intelligent Decision-Making Model.
- **PyQt5** – GUI framework.
- **Selenium WebDriver & WebDriver-Manager** – for browser automation.
- **Edge-TTS** – for text-to-speech conversion.
- **AppOpener & PyWhatKit** – for system and web automation.
- **python-dotenv** – for environment variable management.

