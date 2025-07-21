from google.generativeai import GenerativeModel, configure  # Gemini API
import google.generativeai as genai
from json import load, dump
import datetime
from dotenv import dotenv_values
import os, sys
# Load environment variables

# base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# env_path = os.path.join(base_path, '.env')

# # Now load the .env variables correctly
# env_vars = dotenv_values(env_path)

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GeminiAPIKey = env_vars.get("GeminiAPIKey")  # Changed to Gemini API key

# Configure Gemini client
configure(api_key=GeminiAPIKey)
model = GenerativeModel('gemini-1.5-pro-latest')  # Use latest Gemini model

# Initialize messages list
messages = []

# System instruction template
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} with real-time knowledge.
*** Important Instructions ***
- Do not tell time unless explicitly asked
- Be concise; answer only the question asked
- Reply ONLY in English (ignore other languages)
- Never mention your training data or add extra notes
"""

# Load chat history
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    """Generate current date/time string"""
    now = datetime.datetime.now()
    return (
        f"Current Date: {now.strftime('%A, %B %d, %Y')}\n"
        f"Current Time: {now.strftime('%H:%M:%S')}"
    )

def AnswerModifier(Answer):
    """Clean up response formatting"""
    return '\n'.join(line.strip() for line in Answer.split('\n') if line.strip())

def ChatBot(Query):
    try:
        # Load existing chat history
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # Combine system instructions with real-time info
        full_system = f"{System}\n\n{RealtimeInformation()}"
        
        # Start new chat session with history
        chat = model.start_chat(history=messages)
        
        # Generate response with combined instructions
        response = chat.send_message(
            f"{full_system}\n\nUser Query: {Query}",
            stream=True
        )
        
        # Stream and accumulate response
        Answer = ""
        for chunk in response:
            Answer += chunk.text
        
        # Update and save history
        messages.extend([
            {"role": "user", "parts": [Query]},
            {"role": "model", "parts": [Answer]}
        ])
        
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        
        return AnswerModifier(Answer)
    
    except Exception as e:
        print(f"Error: {e}")
        # Reset chat log on error
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))