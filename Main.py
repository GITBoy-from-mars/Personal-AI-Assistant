from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os



env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = '''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r"Data\ChatLog.json", "r", encoding='utf-8')
    if len(File.read()) < 5:
        with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
            file.write('')

        with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r"Data\ChatLog.json", "r", encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['parts']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'), "r", encoding='utf-8')
    Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8')
        File.write(result)
        File.close()

def InitialExecution():
        SetMicrophoneStatus("False")
        ShowTextToScreen("")
        ShowDefaultChatIfNoChats()
        ChatLogIntegration()
        ShowChatsOnGUI()

InitialExecution()

def MainExecution():
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
        ShowTextToScreen(f"{Username} : {Query}")
        SetAssistantStatus("Thinking...")
        Decision = FirstLayerDMM(Query)

        print("")
        print(f"Decision : {Decision}")
        print("")

        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])

        Merged_query = " and ".join(
            [".".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
            )
        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        for queries in Decision:
            if TaskExecution == False:
                if any(queries.startswith(func) for func in Functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True

        if ImageExecution == True:

            with open(r"Frontend\Files\ImageGeneratojon.data", "w") as file:
                file.write(f"{ImageGenerationQuery},True")

            try:
                p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=False)
                subprocesses.append(p1)

            except Exception as e:
                print(f"Error starting ImageGeneration.py: {e}")

        if G and R:

            SetAssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
        else:
            for Queries in Decision:
                if "general" in Queries:
                    SetAssistantStatus("Thinking...")
                    QueryFinal = Queries.replace("general ", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True
                elif "realtime" in Queries:
                    SetAssistantStatus("Searching...")
                    QueryFinal = Queries.replace("realtime ", "")
                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    return True

                elif "exit" in Queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    SetAssistantStatus("Answering...")
                    os._exit(1)

def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()

        else:
            AIStatus = GetAssistantStatus()

            if "Available..." in AIStatus:
                sleep(0.1)

            else:
                SetAssistantStatus("Available...")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    # Start the second thread for GUI
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()






# import pygame
# import random
# import asyncio
# import edge_tts
# import os
# import time # Import time for sleep
# from dotenv import dotenv_values
# from groq import Groq
# from json import load, dump
# import datetime
# from googlesearch import search as pywhatkit_search # Renamed to avoid conflict with local search_google
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import mtranslate as mt
# from AppOpener import close, open as appopen
# from webbrowser import open as webopen
# from bs4 import BeautifulSoup
# from rich import print
# import subprocess
# import requests
# import keyboard
# import threading # For running backend logic in a separate thread

# # Assume these are imported from Backend.Model, Backend.RealtimeSearchEngine, Backend.Chatbot, etc.
# # For this combined file, I'm including them directly or providing placeholders.
# # If you have these as separate files, ensure they are correctly imported.
# # from Backend.Model import FirstLayerDMM # Assuming this is your DMM
# # from Backend.RealtimeSearchEngine import RealtimeSearchEngine
# # from Backend.Automation import Automation # Automation functions are now integrated directly
# # from Backend.SpeechToText import SpeechRecognition # This is now handled by Selenium
# # from Backend.TextToSpeech import TextToSpeech # This is now handled by TTS function directly
# # from Frontend.GUI import GraphicalUserInterface, SetAssistantStatus, ShowTextToScreen, TempDirectoryPath, SetMicrophoneStatus, AnswerModifier, QueryModifier, GetMicrophoneStatus, GetAssistantStatus

# # --- Environment Variables and API Keys ---
# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username", "User") # Default value if not found
# Assistantname = env_vars.get("Assistantname", "Assistant") # Default value if not found
# GroqAPIKey = env_vars.get("GroqAPIKey")
# AssistantVoice = env_vars.get("AssistantVoice", "en-US-JennyNeural") # Default voice
# InputLanguage = env_vars.get("InputLanguage", "en-US") # Default language

# # Initialize the Groq client with the provided API key.
# client = Groq(api_key=GroqAPIKey)

# # --- Global Variables and Initial Setup ---
# # Define a system message that provides context to the AI chatbot about its role and behavior.
# System = f"Hello, I am {Username}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."

# # Predefined chatbot conversation system message and an initial user message.
# # This is the initial state of the chatbot's system messages.
# SystemChatBot = [
#     {"role": "system", "content": System},
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello, how can I help you?"}
# ]

# # Initialize an empty list to store chat messages.
# messages = [] # This will be updated from ChatLog.json
# # Attempt to load the chat log from a JSON file, or create an empty one if it doesn't exist.
# try:
#     with open(r"Data\ChatLog.json", "r") as f:
#         messages = load(f)  # Load existing messages from the chat log.
# except FileNotFoundError:
#     # If the file doesn't exist, create an empty JSON file to store chat logs.
#     os.makedirs(r"Data", exist_ok=True) # Ensure Data directory exists
#     with open(r"Data\ChatLog.json", "w") as f:
#         dump([], f)

# # Define a list of recognized function keywords for task categorization.
# Functions = [ # Renamed from 'funcs' to 'Functions' for clarity and consistency with user's snippet
#     "exit", "general", "realtime", "open", "close", "play",
#     "generate image", "system", "content", "google search",
#     "youtube search", "reminder"
# ]

# # Define CSS classes for parsing specific elements in HTML content. (Used in GoogleSearch if parsing HTML directly)
# classes = ["zCubwf", "hgKKEc", "LTKGO sV7Pjc", "ZmlLDw", "gsrt vk_bx FZmW5b VWpOhf", "pciqee", "tw-Data-text tw-text-small tw-ta",
#            "lZrdc", "DSuKdd LTKGO", "vizybc", "webanswers webanswers webanswer table", "dDoNo ikb4qb gsri", "sXLaOe",
#            "LnnKFe", "VQf4g", "qv3Dpe", "kno-rdesc", "SPZzOb"]

# # Define a user-agent for making web requests.
# useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# # Predefined professional responses for user interactions.
# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
# ]

# # --- Paths for Frontend/Backend Communication ---
# current_dir = os.getcwd()
# TempDirPath = rf"{current_dir}\Frontend\Files"
# GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# # Ensure directories exist
# os.makedirs(TempDirPath, exist_ok=True)
# os.makedirs(GraphicsDirPath, exist_ok=True)
# os.makedirs(r"Data", exist_ok=True) # Ensure Data directory exists for chatlog/speech

# # Generate the file path for the HTML file for speech recognition.
# VoiceHtmlLink = f'file:///{current_dir}/Data/Voice.html'

# # Define the HTML code for the speech recognition interface.
# HtmlCode = f"""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Speech Recognition</title>
#     <style>
#         body {{ font-family: Arial, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; background-color: #f0f0f0; }}
#         .container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
#         button {{ padding: 10px 20px; margin: 10px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
#         #start {{ background-color: #4CAF50; color: white; }}
#         #end {{ background-color: #f44336; color: white; }}
#         #output {{ margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; min-height: 50px; width: 300px; text-align: left; }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>Speech Recognition</h1>
#         <button id="start">Start Listening</button>
#         <button id="end">Stop Listening</button>
#         <div id="output"></div>
#         <input type="hidden" id="recognitionStatus" value="idle">
#         <input type="hidden" id="finalTranscript" value="">
#     </div>

#     <script>
#         const outputDiv = document.getElementById('output');
#         const startButton = document.getElementById('start');
#         const endButton = document.getElementById('end');
#         const recognitionStatusInput = document.getElementById('recognitionStatus');
#         const finalTranscriptInput = document.getElementById('finalTranscript');

#         let recognition;
#         let finalTranscript = '';

#         if ('webkitSpeechRecognition' in window) {{
#             recognition = new webkitSpeechRecognition();
#             recognition.continuous = false; // Set to false for single utterance recognition
#             recognition.interimResults = true;
#             recognition.lang = '{InputLanguage}';

#             recognition.onstart = function() {{
#                 outputDiv.textContent = 'Listening...';
#                 startButton.disabled = true;
#                 endButton.disabled = false;
#                 recognitionStatusInput.value = 'listening';
#                 finalTranscriptInput.value = ''; // Clear previous
#                 finalTranscript = '';
#             }};

#             recognition.onresult = function(event) {{
#                 let interimTranscript = '';
#                 for (let i = event.resultIndex; i < event.results.length; ++i) {{
#                     if (event.results[i].isFinal) {{
#                         finalTranscript += event.results[i][0].transcript;
#                     }} else {{
#                         interimTranscript += event.results[i][0].transcript;
#                     }}
#                 }}
#                 outputDiv.textContent = finalTranscript + interimTranscript;
#             }};

#             recognition.onerror = function(event) {{
#                 console.error('Speech recognition error:', event.error);
#                 outputDiv.textContent = 'Error: ' + event.error;
#                 recognitionStatusInput.value = 'error';
#                 startButton.disabled = false;
#                 endButton.disabled = true;
#             }};

#             recognition.onend = function() {{
#                 outputDiv.textContent = finalTranscript || 'No speech recognized.';
#                 finalTranscriptInput.value = finalTranscript; // Store final transcript
#                 recognitionStatusInput.value = 'finished';
#                 startButton.disabled = false;
#                 endButton.disabled = true;
#             }};

#             startButton.onclick = function() {{
#                 recognition.start();
#             }};

#             endButton.onclick = function() {{
#                 recognition.stop();
#             }};

#         }} else {{
#             outputDiv.textContent = 'Speech recognition not supported in this browser.';
#             startButton.disabled = true;
#             endButton.disabled = true;
#         }}
#     </script>
# </body>
# </html>
# """

# # Write the modified HTML code to a file.
# with open(r"Data\Voice.html", "w") as f:
#     f.write(HtmlCode)

# # Global variable for the Selenium driver
# driver = None

# # Default chat message for empty chat log
# DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
# {Assistantname} : Welcome {Username}. I am doing well. How may I help you?'''


# # --- Helper Functions (for file I/O and text manipulation) ---

# def AnswerModifier(Answer):
#     """Removes empty lines from a given text."""
#     lines = Answer.split('\n')
#     non_empty_lines = [line for line in lines if line.strip()]
#     modified_answer = '\n'.join(non_empty_lines)
#     return modified_answer

# def QueryModifier(Query):
#     """Modifies a query to ensure proper punctuation (adds ? or .)."""
#     new_query = Query.lower().strip()
#     query_words = new_query.split()
#     question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

#     if any(word + " " in new_query for word in question_words):
#         if query_words and query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "?"
#         else:
#             new_query += "?"
#     else:
#         if query_words and query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "."
#         else:
#             new_query += "."
#     return new_query.capitalize()

# def SetMicrophoneStatus(command):
#     """Sets the microphone status in a file."""
#     with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
#         file.write(command)

# def GetMicrophoneStatus():
#     """Gets the microphone status from a file."""
#     try:
#         with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
#             status = file.read().strip()
#         return status
#     except FileNotFoundError:
#         SetMicrophoneStatus("False") # Initialize if file doesn't exist
#         return "False"

# def SetAssistantStatus(status):
#     """Sets the assistant's status in a file."""
#     with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
#         file.write(status)

# def GetAssistantStatus():
#     """Gets the assistant's status from a file."""
#     try:
#         with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
#             status = file.read().strip()
#         return status
#     except FileNotFoundError:
#         SetAssistantStatus("Idle") # Initialize if file doesn't exist
#         return "Idle"

# def MicButtonInitialed():
#     """Sets microphone status to False (likely off/inactive)."""
#     SetMicrophoneStatus("False")

# def MicButtonClosed():
#     """Sets microphone status to True (likely on/active)."""
#     SetMicrophoneStatus("True")

# def GraphicsDirectoryPath(filename):
#     """Returns the full path to a graphic file."""
#     return rf'{GraphicsDirPath}\{filename}'

# def TempDirectoryPath(filename):
#     """Returns the full path to a temporary file."""
#     return rf'{TempDirPath}\{filename}'

# def ShowTextToScreen(text):
#     """Writes text to a Responses.data file for GUI display."""
#     with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
#         file.write(text)

# def ReadChatLogJson():
#     """Reads the chat log from ChatLog.json."""
#     try:
#         with open(r"Data\ChatLog.json", "r", encoding='utf-8') as f:
#             chatlog_data = load(f)
#         return chatlog_data
#     except FileNotFoundError:
#         return [] # Return empty list if file not found

# def ChatLogIntegration():
#     """Formats chat log data and writes to Database.data for GUI."""
#     json_data = ReadChatLogJson()
#     formatted_chatlog = ""
#     for entry in json_data:
#         if entry["role"] == "user":
#             formatted_chatlog += f"User: {entry['content']}\n"
#         elif entry["role"] == "assistant":
#             formatted_chatlog += f"Assistant: {entry['content']}\n"
#     formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
#     formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

#     with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
#         file.write(AnswerModifier(formatted_chatlog))

# def ShowChatsOnGUI():
#     """Reads formatted chat data and writes to Responses.data for GUI."""
#     try:
#         with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
#             data = file.read()
#         if len(str(data)) > 0:
#             lines = data.split('\n')
#             result = '\n'.join(lines)
#             with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
#                 file.write(result)
#     except FileNotFoundError:
#         pass # File might not exist yet

# def ShowDefaultChatIfNoChats():
#     """Initializes chat log with default message if empty."""
#     try:
#         with open(r"Data\ChatLog.json", "r", encoding='utf-8') as f:
#             chat_content = f.read()
#         if len(chat_content.strip()) < 5: # Check if content is very small (likely empty [])
#             with open(TempDirectoryPath('Database.data'), "w", encoding='utf-8') as file:
#                 file.write('')
#             with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
#                 file.write(DefaultMessage.replace("{Username}", Username).replace("{Assistantname}", Assistantname))
#             # Also ensure ChatLog.json is properly initialized with default messages
#             with open(r"Data\ChatLog.json", "w", encoding='utf-8') as f:
#                 dump([
#                     {"role": "user", "content": f"Hello {Assistantname}, How are you?"},
#                     {"role": "assistant", "content": f"Welcome {Username}. I am doing well. How may I help you?"}
#                 ], f, indent=4)
#     except FileNotFoundError:
#         # Create file and add default chat if not found
#         os.makedirs(r"Data", exist_ok=True)
#         with open(r"Data\ChatLog.json", "w", encoding='utf-8') as f:
#             dump([], f) # Create empty file first
#         ShowDefaultChatIfNoChats() # Recurse to add default messages

# # --- Function Definitions (Core Logic) ---

# # Function to get real-time date and time information.
# def RealtimeInformation():
#     current_date_time = datetime.datetime.now()
#     day = current_date_time.strftime("%A")
#     date = current_date_time.strftime("%d")
#     month = current_date_time.strftime("%B")
#     year = current_date_time.strftime("%Y")
#     hour = current_date_time.strftime("%H")
#     minute = current_date_time.strftime("%M")
#     second = current_date_time.strftime("%S")

#     data = f"Please use this real-time information if needed,\n"
#     data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
#     data += f"Time: {hour} hours :{minute} minutes :{second} seconds."
#     return data

# # Asynchronous function to convert text to an audio file
# async def TextToAudioFile(text) -> None:
#     file_path = r"Data\speech.mp3"
#     if os.path.exists(file_path):
#         try:
#             os.remove(file_path)
#         except OSError as e:
#             print(f"Error removing old speech file: {e}")

#     communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
#     await communicate.save(file_path)

# # Function to manage Text-to-Speech (TTS) functionality
# def TTS(Text):
#     try:
#         asyncio.run(TextToAudioFile(Text))
#         pygame.mixer.init()
#         pygame.mixer.music.load(r"Data\speech.mp3")
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
#         return True
#     except Exception as e:
#         print(f"Error in TTS: {e}")
#         return False
#     finally:
#         try:
#             if pygame.mixer.get_init(): # Check if mixer is initialized before quitting
#                 pygame.mixer.music.stop()
#                 pygame.mixer.quit()
#         except Exception as e:
#             print(f"Error in TTS cleanup: {e}")

# # Function to perform a Google search.
# def GoogleSearch(Topic):
#     # Using pywhatkit's search function for simplicity.
#     try:
#         pywhatkit_search(Topic)
#         return f"Performed Google search for: {Topic}"
#     except Exception as e:
#         return f"Failed to perform Google search: {e}"

# # Function to translate text into English using the mtranslate library.
# def UniversalTranslator(Text):
#     english_translation = mt.translate(Text, "en", "auto")
#     return english_translation.capitalize()

# # Function to generate content using AI and save it to a file.
# def Content(Topic):
#     def OpenNotepad(File):
#         default_text_editor = 'notepad.exe'
#         try:
#             subprocess.Popen([default_text_editor, File])
#             return True
#         except Exception as e:
#             print(f"Error opening Notepad: {e}")
#             return False

#     def ContentWriterAI(prompt):
#         local_messages = messages[:]
#         local_messages.append({"role": "user", "content": f"{prompt}"})
#         completion = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages=SystemChatBot + local_messages,
#             max_tokens=2048,
#             temperature=0.7,
#             top_p=1,
#             stream=True,
#             stop=None
#         )
#         Answer = ""
#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content
#         Answer = Answer.replace("</s2>", "")
#         return Answer

#     Topic = Topic.replace("content ", "").strip()
#     ContentByAI = ContentWriterAI(Topic)
#     file_name = f"Data\\{Topic.lower().replace(' ', '_')}.txt"
#     try:
#         with open(file_name, "w", encoding='utf-8') as file:
#             file.write(ContentByAI)
#         OpenNotepad(file_name)
#         return f"Generated content on '{Topic}' and opened in Notepad."
#     except Exception as e:
#         return f"Failed to generate/save content: {e}"

# # Function to search for a topic on Youtube.
# def YouTubeSearch(Topic):
#     try:
#         Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
#         webopen(Url4Search)
#         return f"Opened YouTube search for: {Topic}"
#     except Exception as e:
#         return f"Failed to open YouTube search: {e}"

# # Function to play a video on Youtube.
# def PlayYoutube(query):
#     try:
#         playonyt(query)
#         return f"Playing YouTube video for: {query}"
#     except Exception as e:
#         return f"Failed to play YouTube video: {e}"

# # Function to open an application or a relevant webpage.
# def OpenApp(app):
#     try:
#         if app.startswith("http://") or app.startswith("https://"):
#             webopen(app)
#             return f"Opened webpage: {app}"
#         else:
#             appopen(app, match_closest=True, output=True, throw_error=True)
#             return f"Opened application: {app}"
#     except Exception as e:
#         return f"Failed to open app/webpage '{app}': {e}"

# # Function to close an application.
# def CloseApp(app):
#     if "chrome" in app.lower():
#         return "Cannot reliably close Chrome via AppOpener. Please close manually."
#     else:
#         try:
#             close(app, match_closest=True, output=True, throw_error=True)
#             return f"Closed application: {app}"
#         except Exception as e:
#             return f"Failed to close app '{app}': {e}"

# # Function to execute system level commands.
# def System(command):
#     command = command.lower().strip()
#     if "mute" in command:
#         keyboard.press_and_release("volume mute")
#         return "System muted."
#     elif "unmute" in command:
#         keyboard.press_and_release("volume mute") # Mute key toggles mute/unmute
#         return "System unmuted."
#     elif "volume up" in command:
#         keyboard.press_and_release("volume up")
#         return "Volume increased."
#     elif "volume down" in command:
#         keyboard.press_and_release("volume down")
#         return "Volume decreased."
#     else:
#         return f"Unknown system command: {command}"


# # Main chatbot function to handle user queries.
# def ChatBot(Query):
#     global messages, SystemChatBot

#     try:
#         with open(r"Data\ChatLog.json", "r") as f:
#             messages = load(f)

#         messages.append({"role": "user", "content": f"{Query}"})

#         groq_messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages

#         completion = client.chat.completions.create(
#             model="llama3-70b-8192",
#             messages=groq_messages,
#             max_tokens=1024,
#             temperature=0.7,
#             top_p=1,
#             stream=True,
#             stop=None,
#         )

#         Answer = ""
#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content

#         Answer = Answer.replace("</s2>", "").strip()
#         messages.append({"role": "assistant", "content": Answer})

#         with open(r"Data\ChatLog.json", "w") as f:
#             dump(messages, f, indent=4)

#         return AnswerModifier(Answer=Answer)

#     except Exception as e:
#         print(f"Error in ChatBot: {e}")
#         # Reset chat log on error to prevent corrupted state
#         with open(r"Data\ChatLog.json", "w") as f:
#             dump([], f, indent=4)
#         # Attempt to retry or provide a default error message
#         return "I encountered an error while processing your request. Please try again."

# # Function to handle real-time search and response generation.
# def RealtimeSearchEngine(prompt):
#     global SystemChatBot, messages

#     try:
#         with open(r"Data\ChatLog.json", "r") as f:
#             messages = load(f)
#         messages.append({"role": "user", "content": f"{prompt}"})

#         # Perform Google Search and add results to context
#         google_search_result = GoogleSearch(prompt) # This already opens browser
#         # If you want to use the search result text in the LLM, you need to fetch it.
#         # For now, GoogleSearch just opens a browser.
#         # If you need to pass content to the LLM, you'd use a library that returns text.
#         # For simplicity, assuming the LLM can infer from the prompt that it needs real-time data.
#         # If GoogleSearch actually returns text, use it here:
#         # SystemChatBot.append({"role": "system", "content": f"Google Search Result: {google_search_result}"})

#         groq_messages = SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages

#         completion = client.chat.completions.create(
#             model="llama3-70b-8192",
#             messages=groq_messages,
#             temperature=0.7,
#             max_tokens=2048,
#             top_p=1,
#             stream=True,
#             stop=None
#         )

#         Answer = ""
#         for chunk in completion:
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content

#         Answer = Answer.strip().replace("</s2>", "")
#         messages.append({'role': 'assistant', 'content': Answer})

#         with open(r"Data\ChatLog.json", "w") as f:
#             dump(messages, f, indent=4)

#         # SystemChatBot.pop() # Remove the temporary system message if added
#         return AnswerModifier(Answer=Answer)

#     except Exception as e:
#         print(f"Error in RealtimeSearchEngine: {e}")
#         return "I encountered an error while searching for real-time information. Please try again."


# # First Layer Decision-Making Model (DMM) using Gemini API
# import google.generativeai as genai # Ensure you have this installed: pip install -q google-generativeai

# # Replace with your actual Gemini API key if not set in environment
# # genai.configure(api_key="YOUR_GEMINI_API_KEY") # Only if not using environment variable or Canvas provided key

# dmm_preamble = """
# You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
# You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'.
# *** Do not answer any query, just decide what kind of query is given to you. ***
# -> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
# -> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
# -> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
# -> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
# -> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
# -> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
# -> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
# -> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
# -> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
# -> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
# -> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
# *** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
# *** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
# *** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
# """

# DMM_ChatHistory = [
#     {"role": "user", "parts": [{"text": "how are you?"}]},
#     {"role": "model", "parts": [{"text": "general how are you?"}]},
#     {"role": "user", "parts": [{"text": "do you like pizza?"}]},
#     {"role": "model", "parts": [{"text": "general do you like pizza?"}]},
#     {"role": "user", "parts": [{"text": "open chrome and tell me about mahatma gandhi."}]},
#     {"role": "model", "parts": [{"text": "open chrome, general tell me about mahatma gandhi."}]},
#     {"role": "user", "parts": [{"text": "open chrome and firefox"}]},
#     {"role": "model", "parts": [{"text": "open chrome, open firefox"}]},
#     {"role": "user", "parts": [{"text": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"}]},
#     {"role": "model", "parts": [{"text": "general what is today's date, reminder 11:00pm 5th aug dancing performance"}]},
#     {"role": "user", "parts": [{"text": "chat with me."}]},
#     {"role": "model", "parts": [{"text": "general chat with me."}]}
# ]

# dmm_model = genai.GenerativeModel('gemini-pro')

# def FirstLayerDMM(prompt: str = "test"):
#     try:
#         # Prepare the full chat history including the preamble for gemini-pro.
#         full_dmm_chat_history = [{"role": "user", "parts": [{"text": dmm_preamble}]}] + DMM_ChatHistory

#         chat_session = dmm_model.start_chat(
#             history=full_dmm_chat_history
#         )

#         stream = chat_session.send_message(
#             prompt,
#             stream=True,
#             generation_config={
#                 "temperature": 0.7,
#             }
#         )

#         response = ""
#         for chunk in stream:
#             if chunk.text:
#                 response += chunk.text

#         response = response.replace("\n", "").strip()
#         response = response.split(",")
#         response = [i.strip() for i in response]

#         temp = []
#         for task in response:
#             for func_keyword in Functions:
#                 if task.startswith(func_keyword):
#                     temp.append(task)

#         response = temp

#         # Recursive call if DMM returns 'general (query)' without a more specific classification
#         if "general (query)" in response and len(response) == 1:
#             print("DMM returned 'general (query)'. Recategorizing...")
#             return FirstLayerDMM(prompt=prompt) # Recursive call

#         return response
#     except Exception as e:
#         print(f"Error in FirstLayerDMM: {e}")
#         # Fallback to general if DMM fails
#         return [f"general {prompt}"]


# # Function to get speech input from the HTML page via Selenium
# def SpeechRecognition():
#     global driver

#     if driver is None:
#         print("Selenium WebDriver not initialized. Cannot perform speech recognition.")
#         return ""

#     try:
#         # Ensure we are on the correct page
#         if driver.current_url != VoiceHtmlLink:
#             driver.get(VoiceHtmlLink)
#             time.sleep(1) # Give page time to load

#         # Click the "Start Listening" button
#         try:
#             start_button = driver.find_element(By.ID, "start")
#             if start_button.is_enabled():
#                 start_button.click()
#                 print("Clicked Start Listening button in browser.")
#                 SetAssistantStatus("Listening...")
#             else:
#                 print("Start button not enabled, recognition might be active or page not ready.")
#         except Exception as e:
#             print(f"Error clicking start button: {e}")
#             # If button not found or clickable, it might be already listening.

#         # Wait for speech recognition to finish and transcript to be available
#         timeout = 20 # seconds for speech input
#         poll_interval = 0.2 # seconds
#         start_time = time.time()
#         transcript = ""

#         while time.time() - start_time < timeout:
#             try:
#                 # Read the recognition status and final transcript from hidden input fields
#                 recognition_status = driver.find_element(By.ID, "recognitionStatus").get_attribute("value")
#                 current_output_text = driver.find_element(By.ID, "output").text.strip()

#                 if recognition_status == 'finished':
#                     transcript = driver.find_element(By.ID, "finalTranscript").get_attribute("value")
#                     print(f"Recognized (final): {transcript}")
#                     break
#                 elif recognition_status == 'listening':
#                     SetAssistantStatus(f"Listening... {current_output_text[:50]}...")
#                 elif recognition_status == 'error':
#                     print("Speech recognition error detected in browser.")
#                     break # Exit on error
#                 time.sleep(poll_interval)
#             except Exception as e:
#                 print(f"Error polling speech recognition status: {e}")
#                 time.sleep(poll_interval)

#         # After getting transcript or timeout, click the "Stop Listening" button to reset the JS state
#         try:
#             end_button = driver.find_element(By.ID, "end")
#             if end_button.is_enabled():
#                 end_button.click()
#                 print("Clicked Stop Listening button in browser.")
#                 time.sleep(0.5) # Give time for JS to reset
#         except Exception as e:
#             print(f"Error clicking end button during cleanup: {e}")

#         # Clear the output div and hidden fields in HTML after getting the transcript
#         driver.execute_script("""
#             document.getElementById('output').textContent = '';
#             document.getElementById('recognitionStatus').value = 'idle';
#             document.getElementById('finalTranscript').value = '';
#         """)

#         return transcript

#     except Exception as e:
#         print(f"Overall error in SpeechRecognition: {e}")
#         return ""


# # --- Main Execution Flow ---
# subprocesses = [] # To keep track of any launched subprocesses

# def MainExecution():
#     global driver, subprocesses

#     # Ensure Selenium driver is initialized and Voice.html is open
#     if driver is None:
#         print("Initializing Selenium WebDriver...")
#         chrome_options = Options()
#         chrome_options.add_argument(f"--user-agent={useragent}")
#         chrome_options.add_argument("--use-fake-ui-for-media-stream")
#         chrome_options.add_argument("--use-fake-device-for-media-stream")
#         chrome_options.add_argument("--headless=new") # Run Chrome in headless mode
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#         driver.get(VoiceHtmlLink)
#         time.sleep(2) # Give time for page to load

#     SetAssistantStatus("Listening...")
#     Query = SpeechRecognition()
#     if not Query:
#         print("No speech recognized or error during recognition. Retrying...")
#         SetAssistantStatus("Available...")
#         return # Skip processing if no query

#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")
#     Decision = FirstLayerDMM(QueryModifier(Query))

#     print("\n")
#     print(f"Decision : {Decision}")
#     print("\n")

#     # Flag to check if any specific task was executed
#     task_executed = False

#     # Handle tasks based on DMM decision
#     for command in Decision:
#         if command.startswith("exit"):
#             print("Exit command received. Terminating application.")
#             SetAssistantStatus("Goodbye!")
#             asyncio.run(TTS("Goodbye!"))
#             # Clean up driver and subprocesses before exiting
#             if driver:
#                 driver.quit()
#             for p in subprocesses:
#                 if p.poll() is None: # If subprocess is still running
#                     p.terminate()
#             os._exit(0) # Force exit all threads

#         elif command.startswith("generate image "):
#             ImageGenerationQuery = command.removeprefix("generate image ").strip()
#             with open(r"Frontend\Files\ImageGeneration.data", "w", encoding='utf-8') as file:
#                 file.write(f"{ImageGenerationQuery},True")
#             try:
#                 p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'],
#                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                         stdin=subprocess.PIPE, shell=False)
#                 subprocesses.append(p1)
#                 print(f"Started ImageGeneration.py for: {ImageGenerationQuery}")
#                 SetAssistantStatus("Generating Image...")
#                 task_executed = True
#             except Exception as e:
#                 print(f"Error starting ImageGeneration.py: {e}")
#                 SetAssistantStatus("Image generation failed.")
#                 task_executed = True # Consider it handled, even if failed

#         elif command.startswith("open "):
#             app_or_url = command.removeprefix("open ").strip()
#             asyncio.run(asyncio.to_thread(OpenApp, app_or_url))
#             task_executed = True
#         elif command.startswith("close "):
#             app_name = command.removeprefix("close ").strip()
#             asyncio.run(asyncio.to_thread(CloseApp, app_name))
#             task_executed = True
#         elif command.startswith("play "):
#             song_or_video = command.removeprefix("play ").strip()
#             asyncio.run(asyncio.to_thread(PlayYoutube, song_or_video))
#             task_executed = True
#         elif command.startswith("system "):
#             system_command = command.removeprefix("system ").strip()
#             asyncio.run(asyncio.to_thread(System, system_command))
#             task_executed = True
#         elif command.startswith("content "):
#             content_topic = command.removeprefix("content ").strip()
#             asyncio.run(asyncio.to_thread(Content, content_topic))
#             task_executed = True
#         elif command.startswith("google search "):
#             search_topic = command.removeprefix("google search ").strip()
#             asyncio.run(asyncio.to_thread(GoogleSearch, search_topic))
#             task_executed = True
#         elif command.startswith("youtube search "):
#             youtube_topic = command.removeprefix("youtube search ").strip()
#             asyncio.run(asyncio.to_thread(YouTubeSearch, youtube_topic))
#             task_executed = True
#         elif command.startswith("reminder "):
#             reminder_details = command.removeprefix("reminder ").strip()
#             print(f"Reminder requested: {reminder_details} (Functionality not fully implemented)")
#             SetAssistantStatus("Reminder set (placeholder).")
#             task_executed = True

#     # Handle general and realtime queries if no specific task was executed
#     if not task_executed:
#         # Check if any "general" or "realtime" queries are present
#         G_queries = [i.removeprefix("general ").strip() for i in Decision if i.startswith("general")]
#         R_queries = [i.removeprefix("realtime ").strip() for i in Decision if i.startswith("realtime")]

#         if R_queries: # Prioritize realtime if present
#             SetAssistantStatus("Searching...")
#             full_search_query = " ".join(R_queries + G_queries) # Combine all for search
#             Answer = asyncio.run(asyncio.to_thread(RealtimeSearchEngine, QueryModifier(full_search_query)))
#             ShowTextToScreen(f"{Assistantname} : {Answer}")
#             SetAssistantStatus("Answering...")
#             asyncio.run(TTS(Answer))
#         elif G_queries: # Only general queries
#             SetAssistantStatus("Thinking...")
#             merged_general_query = " ".join(G_queries)
#             Answer = asyncio.run(asyncio.to_thread(ChatBot, QueryModifier(merged_general_query)))
#             ShowTextToScreen(f"{Assistantname} : {Answer}")
#             SetAssistantStatus("Answering...")
#             asyncio.run(TTS(Answer))
#         else:
#             # Fallback if DMM didn't classify anything specific or general/realtime
#             print("DMM did not produce a recognized command or general/realtime query.")
#             SetAssistantStatus("I'm not sure how to respond to that.")
#             asyncio.run(TTS("I'm not sure how to respond to that."))


#     SetAssistantStatus("Available...") # Reset status after processing

# # Initial setup function
# def InitialExecution():
#     global driver
#     SetMicrophoneStatus("False")
#     ShowTextToScreen("")
#     ShowDefaultChatIfNoChats() # Ensure chat log and default messages are set up
#     ChatLogIntegration()
#     ShowChatsOnGUI()

#     # Initialize Selenium WebDriver here
#     print("Initializing Selenium WebDriver for Voice.html...")
#     chrome_options = Options()
#     chrome_options.add_argument(f"--user-agent={useragent}")
#     chrome_options.add_argument("--use-fake-ui-for-media-stream")
#     chrome_options.add_argument("--use-fake-device-for-media-stream")
#     chrome_options.add_argument("--headless=new")
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.get(VoiceHtmlLink)
#     time.sleep(2) # Give time for page to load

# # Threads for backend logic
# def FirstThread():
#     while True:
#         current_status = GetMicrophoneStatus()
#         if current_status == "True":
#             MainExecution()
#         else:
#             ai_status = GetAssistantStatus()
#             # Only set "Available..." if not already in a processing state
#             if "Available..." not in ai_status and "Listening..." not in ai_status and \
#                "Thinking..." not in ai_status and "Answering..." not in ai_status and \
#                "Generating Image..." not in ai_status:
#                 SetAssistantStatus("Available...")
#             time.sleep(0.5) # Poll less frequently when mic is off

# def SecondThread():
#     # This thread can monitor ImageGeneration.data for completion
#     while True:
#         try:
#             with open(r"Frontend\Files\ImageGeneration.data", "r", encoding='utf-8') as f:
#                 data = f.read()
#             if data.endswith(",False"): # If image generation is complete
#                 prompt, status = data.split(',')
#                 if status == "False":
#                     # Image generation finished, reset status in file
#                     with open(r"Frontend\Files\ImageGeneration.data", "w", encoding='utf-8') as f_write:
#                         f_write.write(f"{prompt},Idle") # Set to Idle or empty
#                     SetAssistantStatus("Image generation complete.")
#                     print(f"Image generation for '{prompt}' finished.")
#         except FileNotFoundError:
#             pass
#         except Exception as e:
#             print(f"Error in SecondThread (ImageGeneration monitor): {e}")
#         time.sleep(1) # Check every 1 second

# # --- GUI related imports and function call ---
# # These would typically be in Frontend/GUI.py
# # For this combined response, I'm including the necessary parts for the GUI to run.
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QTextEdit, QFrame, QSizePolicy
# from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QMovie, QIcon
# from PyQt5.QtCore import Qt, QSize, QTimer, QRect, QPoint, QThread, QObject, pyqtSignal, QPropertyAnimation, QEasingCurve, QCoreApplication

# class ChatSection(QWidget):
#     def __init__(self):
#         super(ChatSection, self).__init__()
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(-20, 40, 40, 100)
#         layout.setSpacing(-100)

#         self.chat_text_edit = QTextEdit()
#         self.chat_text_edit.setReadOnly(True)
#         self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
#         self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
#         layout.addWidget(self.chat_text_edit)

#         self.setStyleSheet("background-color: black;")
#         layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
#         layout.setStretch(1, 1)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

#         text_color = QColor(Qt.blue)
#         self.user_format = QTextCharFormat()
#         self.user_format.setForeground(QColor(Qt.white))
#         self.assistant_format = QTextCharFormat()
#         self.assistant_format.setForeground(QColor(Qt.cyan))

#         self.gif_label = QLabel()
#         self.gif_label.setStyleSheet("border: none;")
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         max_gif_size_W = 400
#         max_gif_size_H = 270
#         movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
#         self.gif_label.setMovie(movie)
#         self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
#         movie.start()
#         layout.addWidget(self.gif_label)

#         self.label = QLabel("")
#         self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
#         self.label.setAlignment(Qt.AlignRight)
#         layout.addWidget(self.label)

#         layout.setSpacing(-20)

#         font = QFont()
#         font.setPointSize(13)
#         self.chat_text_edit.setFont(font)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.LoadMessages)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(500)

#         self.chat_text_edit.viewport().installEventFilter(self)

#         self.setStyleSheet(self.styleSheet() + """
#         QScrollBar:vertical {
#             border: none;
#             background: black;
#             width: 10px;
#             margin: 0px 0px 0px 0px;
#         }

#         QScrollBar::handle:vertical {
#             background: white;
#             min-height: 20px;
#             border-radius: 5px;
#         }

#         QScrollBar::add-line:vertical {
#             background: black;
#             subcontrol-position: bottom;
#             subcontrol-origin: margin;
#             border: none;
#             height: 0px;
#         }

#         QScrollBar::sub-line:vertical {
#             background: black;
#             subcontrol-position: top;
#             subcontrol-origin: margin;
#             border: none;
#             height: 0px;
#         }
#         """)

#     def LoadMessages(self):
#         try:
#             with open(r"Data\ChatLog.json", "r", encoding='utf-8') as f:
#                 current_messages = load(f)

#             formatted_current_text = self._format_messages_for_display(current_messages)
#             if self.chat_text_edit.toPlainText() != formatted_current_text:
#                 self.chat_text_edit.clear()
#                 cursor = self.chat_text_edit.textCursor()

#                 for msg in current_messages:
#                     role = msg.get("role")
#                     content = msg.get("content")
#                     if role == "user":
#                         cursor.insertText(f"You: {content}\n\n", self.user_format)
#                     elif role == "assistant":
#                         cursor.insertText(f"{Assistantname}: {content}\n\n", self.assistant_format)
#                 cursor.movePosition(QTextCursor.End)
#                 self.chat_text_edit.setTextCursor(cursor)

#         except FileNotFoundError:
#             os.makedirs(r"Data", exist_ok=True)
#             with open(r"Data\ChatLog.json", "w", encoding='utf-8') as f:
#                 dump([], f)
#         except Exception as e:
#             print(f"Error loading messages: {e}")

#     def _format_messages_for_display(self, messages_list):
#         formatted_text = ""
#         for msg in messages_list:
#             role = msg.get("role")
#             content = msg.get("content")
#             if role == "user":
#                 formatted_text += f"You: {content}\n\n"
#             elif role == "assistant":
#                 formatted_text += f"{Assistantname}: {content}\n\n"
#         return formatted_text

#     def SpeechRecogText(self):
#         status_text = GetAssistantStatus()
#         self.label.setText(status_text)

#     def addMessage(self, message, role):
#         cursor = self.chat_text_edit.textCursor()
#         format = QTextCharFormat()
#         block_format = QTextTextBlockFormat()
#         block_format.setTopMargin(10)
#         block_format.setLeftMargin(10)

#         if role == "user":
#             format.setForeground(QColor(Qt.white))
#             cursor.insertText(f"You: {message}\n\n", format)
#         elif role == "assistant":
#             format.setForeground(QColor(Qt.cyan))
#             cursor.insertText(f"{Assistantname}: {message}\n\n", format)

#         cursor.movePosition(QTextCursor.End)
#         self.chat_text_edit.setTextCursor(cursor)


# class HomeScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()

#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(0, 0, 0, 0)

#         gif_label = QLabel()
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         gif_label.setMovie(movie)
#         max_gif_size_H = int(screen_width / 16 * 9)
#         movie.setScaledSize(QSize(screen_width, max_gif_size_H))
#         gif_label.setAlignment(Qt.AlignCenter)
#         movie.start()
#         content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)

#         self.label = QLabel("")
#         self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
#         self.label.setAlignment(Qt.AlignCenter)
#         content_layout.addWidget(self.label, alignment=Qt.AlignCenter)

#         self.icon_label = QLabel()
#         pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
#         new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.icon_label.setPixmap(new_pixmap)
#         self.icon_label.setFixedSize(150,150)
#         self.icon_label.setAlignment(Qt.AlignCenter)
#         self.icon_label.mousePressEvent = self.toggle_icon
#         content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

#         self.toggled = GetMicrophoneStatus() == "True"
#         self.toggle_icon()

#         content_layout.setContentsMargins(0, 0, 0, 150)

#         self.setLayout(content_layout)
#         self.setStyleSheet("background-color: black;")
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)

#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(500)

#     def load_icon(self, path, width=60, height=60):
#         pixmap = QPixmap(path)
#         new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.icon_label.setPixmap(new_pixmap)

#     def toggle_icon(self, event=None):
#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
#             MicButtonInitialed()
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
#             MicButtonClosed()
#         self.toggled = not self.toggled

#     def SpeechRecogText(self):
#         status_text = GetAssistantStatus()
#         self.label.setText(status_text)


# class MessageScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()

#         layout = QVBoxLayout()
#         label = QLabel("")
#         layout.addWidget(label)

#         self.chat_section = ChatSection()
#         layout.addWidget(self.chat_section)

#         self.setLayout(layout)
#         self.setStyleSheet("background-color: black;")
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)


# class CustomTopBar(QWidget):
#     def __init__(self, parent, stacked_widget: QStackedWidget):
#         super().__init__(parent)
#         self.stacked_widget = stacked_widget
#         self.initUI()
#         self.current_screen = None

#     def initUI(self):
#         self.setFixedHeight(50)
#         layout = QHBoxLayout(self)
#         layout.setAlignment(Qt.AlignRight)

#         title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
#         title_label.setStyleSheet("color: black; font-size: 18px; background-color:white; padding-left: 10px;")
#         layout.addWidget(title_label)
#         layout.addStretch(1) # Pushes elements to the right

#         home_button = QPushButton()
#         home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
#         home_button.setIcon(home_icon)
#         home_button.setText('Home')
#         home_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black; border-radius: 10px; padding: 0 15px;")
#         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
#         layout.addWidget(home_button)

#         message_button = QPushButton()
#         message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
#         message_button.setIcon(message_icon)
#         message_button.setText(" Chat")
#         message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color: black; border-radius: 10px; padding: 0 15px;")
#         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
#         layout.addWidget(message_button)

#         minimize_button = QPushButton()
#         minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
#         minimize_button.setIcon(minimize_icon)
#         minimize_button.setStyleSheet("background-color:white; border-radius: 10px;")
#         minimize_button.clicked.connect(self.minimizeWindow)
#         layout.addWidget(minimize_button)

#         self.maximize_button = QPushButton()
#         self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
#         self.restore_icon = QIcon(GraphicsDirectoryPath('Restore.png'))
#         self.maximize_button.setIcon(self.maximize_icon)
#         self.maximize_button.setFlat(False)
#         self.maximize_button.setStyleSheet("background-color:white; border-radius: 10px;")
#         self.maximize_button.clicked.connect(self.maximizeWindow)
#         layout.addWidget(self.maximize_button)

#         close_button = QPushButton()
#         close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
#         close_button.setIcon(close_icon)
#         close_button.setStyleSheet("background-color:white; border-radius: 10px;")
#         close_button.clicked.connect(self.closeWindow)
#         layout.addWidget(close_button)

#         # Horizontal line separator (this will be at the end of the QHBoxLayout, effectively below buttons)
#         line_frame = QFrame()
#         line_frame.setFixedHeight(1)
#         line_frame.setFrameShape(QFrame.HLine)
#         line_frame.setFrameShadow(QFrame.Sunken)
#         line_frame.setStyleSheet("border-color: black; background-color: black;")
#         # This line frame placement might need adjustment if you want it to span the full width below the buttons.
#         # For now, it will be placed as a widget in the QHBoxLayout.
#         # layout.addWidget(line_frame) # Removed as it might not be intended for QHBoxLayout directly

#         self.draggable = True
#         self.offset = None

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), Qt.white) # Background for the top bar itself
#         super().paintEvent(event)

#     def minimizeWindow(self):
#         self.parent().showMinimized()

#     def maximizeWindow(self):
#         if self.parent().isMaximized():
#             self.parent().showNormal()
#             self.maximize_button.setIcon(self.maximize_icon)
#         else:
#             self.parent().showMaximized()
#             self.maximize_button.setIcon(self.restore_icon)

#     def closeWindow(self):
#         self.parent().close()

#     def mousePressEvent(self, event):
#         if self.draggable:
#             self.offset = event.pos()

#     def mouseMoveEvent(self, event):
#         if self.draggable and self.offset:
#             new_pos = event.globalPos() - self.offset
#             self.parent().move(new_pos)

#     def mouseReleaseEvent(self, event):
#         self.offset = None # Reset offset when mouse is released


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground) # For transparent background

#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(0,0,0,0) # Remove margins for main layout
#         self.main_layout.setSpacing(0) # Remove spacing between widgets

#         # Stacked widget for different screens (Home, Chat)
#         self.stacked_widget = QStackedWidget(self)
#         self.home_screen = HomeScreen()
#         self.message_screen = MessageScreen()
#         self.stacked_widget.addWidget(self.home_screen)
#         self.stacked_widget.addWidget(self.message_screen)

#         # Custom top bar
#         self.top_bar = CustomTopBar(self, self.stacked_widget)
#         self.main_layout.addWidget(self.top_bar)
#         self.main_layout.addWidget(self.stacked_widget)

#         # Set initial size and style
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()
#         self.setGeometry(0, 0, screen_width, screen_height) # Full screen initially
#         self.setStyleSheet("background-color: black;") # Main window background

#         # Make the main window draggable by the top bar
#         self.top_bar.mousePressEvent = self.mousePressEvent_top_bar
#         self.top_bar.mouseMoveEvent = self.mouseMoveEvent_top_bar
#         self.top_bar.mouseReleaseEvent = self.mouseReleaseEvent_top_bar

#     # Implement mouse events for dragging the frameless window
#     def mousePressEvent_top_bar(self, event):
#         if event.button() == Qt.LeftButton:
#             self.old_pos = event.globalPos()

#     def mouseMoveEvent_top_bar(self, event):
#         if event.buttons() == Qt.LeftButton:
#             delta = QPoint(event.globalPos() - self.old_pos)
#             self.move(self.x() + delta.x(), self.y() + delta.y())
#             self.old_pos = event.globalPos()

#     def mouseReleaseEvent_top_bar(self, event):
#         if event.button() == Qt.LeftButton:
#             self.old_pos = None


# def GraphicalUserInterface():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


# # Main entry point for the application
# if __name__ == "__main__":
#     # Perform initial setup (creates directories, initializes files, starts Selenium)
#     InitialExecution()

#     # Start backend threads
#     thread1 = threading.Thread(target=FirstThread)
#     thread2 = threading.Thread(target=SecondThread)

#     thread1.daemon = True # Allow threads to exit when main program exits
#     thread2.daemon = True

#     thread1.start()
#     thread2.start()

#     # Start the GUI application in the main thread
#     GraphicalUserInterface()

#     # Clean up Selenium driver and any subprocesses when GUI closes
#     if driver:
#         driver.quit()
#     for p in subprocesses:
#         if p.poll() is None: # If subprocess is still running
#             p.terminate()