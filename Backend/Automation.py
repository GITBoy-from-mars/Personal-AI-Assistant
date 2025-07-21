# # Import required libraries
# from AppOpener import close, open as appopen  # Import functions to open and close apps.
# from webbrowser import open as webopen  # Import web browser functionality.
# from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
# from dotenv import dotenv_values  # Import dotenv to manage environment variables.
# from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
# from rich import print  # Import rich for styled console output.
# from groq import Groq  # Import Groq for AI chat functionalities.
# import webbrowser  # Import webbrowser for opening URLs.
# import subprocess  # Import subprocess for interacting with the system.
# import requests  # Import requests for making HTTP requests.
# import keyboard  # Import keyboard for keyboard-related actions.
# import asyncio  # Import asyncio for asynchronous programming.
# import os  # Import os for operating system functionalities.

# # Load environment variables from the .env file.
# env_vars = dotenv_values(".env")
# GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# # Define CSS classes for parsing specific elements in HTML content.
# classes = ["zCubwf", "hgKKEc", "LTKGO sV7Pjc", "ZmlLDw", "gsrt vk_bx FZmW5b VWpOhf", "pciqee", "tw-Data-text tw-text-small tw-ta",
#            "lZrdc", "DSuKdd LTKGO", "vizybc", "webanswers webanswers webanswer table", "dDoNo ikb4qb gsri", "sXLaOe",
#            "LnnKFe", "VQf4g", "qv3Dpe", "kno-rdesc", "SPZzOb"]

# # Define a user-agent for making web requests.
# useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# # Initialize the Groq client with the API key.
# client = Groq(api_key=GroqAPIKey)

# # Predefined professional responses for user interactions.
# professional_responses = [
#     "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
#     "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
# ]

# # List to store chatbot messages.
# messages = []

# # System message to provide context to the chatbot.
# SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# # Function to perform a Google search.
# def GoogleSearch(Topic):
#     search(Topic)  # Use pywhatkit's search function to perform a Google search.
#     return True  # Indicate success.

# # Function to generate content using AI and save it to a file.
# def Content(Topic):
#     # Nested function to open a file in Notepad.
#     def OpenNotepad(File):
#         default_text_editor = 'notepad.exe'  # Default text editor.
#         subprocess.Popen([default_text_editor, File])  # Open the file in Notepad.

#     # Nested function to generate content using the AI chatbot.
#     def ContentWriterAI(prompt):
#         messages.append({"role": "user", "content": f"{prompt}"})  # Add the user's prompt to messages.

#         completion = client.chat.completions.create(
#             model="mixtral-8x7b-32768",  # Specify the AI model.
#             messages=SystemChatBot + messages,  # Include system instructions and chat history.
#             max_tokens=2048,  # Limit the maximum tokens in the response.
#             temperature=0.7,  # Adjust response randomness.
#             top_p=1,  # Use nucleus sampling for response diversity.
#             stream=True,  # Enable streaming response.
#             stop=None
#         )

#         Answer = ""  # Initialize an empty string for the response.
#         # Process streamed response chunks.
#         for chunk in completion:
#             if chunk.choices[0].delta.content:  # Check for content in the current chunk.
#                 Answer += chunk.choices[0].delta.content  # Append the content to the answer.

#         Answer = Answer.replace("</s2>", "")  # Remove unwanted tokens from the response.
#         messages.append({'role': 'assistant', 'content': Answer})  # Add the AI's response to messages.
#         return Answer

#     Topic: str = Topic.replace("Content ", "")  # Remove "Content " from the topic.
#     ContentByAI = ContentWriterAI(Topic)  # Generate content using AI.

#     # Save the generated content to a text file.
#     with open(r"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding='utf-8') as file:
#         file.write(ContentByAI)  # Write the content to the file.
#         file.close()
#     OpenNotepad(f"Data\{Topic.lower().replace(' ', '')}.txt")  # Open the file in Notepad.
#     return True  # Indicate success.
# content("Application for Leave")
# # Function to search for a topic on Youtube.
# def YouTubeSearch(Topic):
#     Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
#     webbrowser.open(Url4Search)  # Open the search URL in a web browser.
#     return True  # Indicate success.

# # Function to play a video on Youtube.
# def PlayYoutube(query):
#     playonyt(query)  # Use pywhatkit's playonyt function to play the video.
#     return True  # Indicate success.

# # Function to open an application or a relevant webpage.
# def OpenApp(app, sess=requests.session()):
#     try:
#         appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app.
#         return True  # Indicate success.

#     except:
#         # Nested function to extract links from HTML content.
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
#             links = soup.find_all('a', {'jsname': 'UWkNB'})  # Find relevant links.
#             return [link.get('href') for link in links]  # Return the links.

#         # Nested function to perform a Google search and retrieve HTML.
#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL.
#             headers = {"User-Agent": useragent}  # Use the predefined user-agent.
#             response = sess.get(url, headers=headers)  # Perform the GET request.

#             if response.status_code == 200:
#                 return response.text  # Return the HTML content.
#             else:
#                 print("Failed to retrieve search results.")  # Print an error message.
#             return None

#         html = search_google(app)  # Perform the Google search.

#         if html:
#             link = extract_links(html)[0]  # Extract the first link from the search results.
#             webopen(link)  # Open the link in a web browser.

#         return True  # Indicate success.

# # Function to close an application.
# def CloseApp(app):
#     if "chrome" in app:
#         pass  # Skip if the app is Chrome.
#     else:
#         try:
#             close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
#             return True  # Indicate success.
#         except:
#             return False  # Indicate failure.

# # Function to execute system level commands.
# def System(command):
#     # Nested function to mute the system volume.
#     def mute():
#         keyboard.press_and_release("volume mute")  # Simulate the mute key press.

#     # Nested function to unmute the system volume.
#     def unmute():
#         keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

#     # Nested function to increase the system volume.
#     def volume_up():
#         keyboard.press_and_release("volume up")  # Simulate the volume up key press.
    
#     def volume_down():
#         keyboard.press_and_release("volume down")  # Simulate the volume up key press.
    
#     if command == "mute":
#         mute()
#     elif command == "unmute":
#         unmute()
#     if command == "volume up":
#         volume_up()
#     elif command == "volume down":
#         volume_down()
    
#     return True  # Indicate success.

# async def TranslateAndExecute(commnds: list[str]):
#     funcs = [] # List to store asynchronous tasks.

#     for command in commands:

#         if command.startswith("open "): # Handle "open" commands.

#             if "open it" in command: # Ignore "open it" commands.
#                 pass

#             if "open file" == command: # Ignore "open file" commands.
#                 pass
#             else:
#                 fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app opening.
#                 funcs.append(fun)

#         elif command.startswith("general "): # Placeholder for general commands.
#             pass

#         elif command.startswith("realtime "): # Placeholder for real-time commands.
#             pass

#         elif command.startswith("close "): # Handle "close" commands.
#             fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) # Schedule app closing.
#             funcs.append(fun)

#         elif command.startswith("play "): # Handle "play" commands.
#             fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play ")) # Schedule YouTube playback.
#             funcs.append(fun)

#         elif command.startswith("content "): # Handle "content" commands.
#             fun = asyncio.to_thread(Content, command.removeprefix("content ")) # Schedule content creation.
#             funcs.append(fun)

#         elif command.startswith("google search "): # Handle Google search commands.
#             fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ")) # Schedule Google search.
#             funcs.append(fun)

#         elif command.startswith("youtube search "): # Handle Youtube search commands.
#             fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # Schedule YouTube search.
#             funcs.append(fun)

#         elif command.startswith("system "): # Handle system commands.
#             fun = asyncio.to_thread(System, command.removeprefix("system ")) # Schedule system command.
#             funcs.append(fun)

#         else:
#             print(f"No Function Found. For {command}!") # Print an error for uncategorized commands.

#     results = await asyncio.gather(*funcs) # Execute all tasks concurrently.

#     for result in results: # Process the results.
#         if isinstance(result, str):
#             yield result
#         else:
#            yield result

# async def Automation(commands: list[str]):
    
#     async for result in TranslateAndExecute(commands): # Execute the commands and yield results.
#        pass
       
#     return True







# Import required libraries
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
import google.generativeai as genai  # Replaced Groq with Gemini
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os, sys


base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_path, '.env')

# Now load the .env variables correctly
env_vars = dotenv_values(env_path)

# Load environment variables from the .env file.
# env_vars = dotenv_values(".env")
GeminiAPIKey = env_vars.get("GeminiAPIKey")  # Changed to Gemini API key

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKKEc", "LTKGO sV7Pjc", "ZmlLDw", "gsrt vk_bx FZmW5b VWpOhf", "pciqee", "tw-Data-text tw-text-small tw-ta",
           "lZrdc", "DSuKdd LTKGO", "vizybc", "webanswers webanswers webanswer table", "dDoNo ikb4qb gsri", "sXLaOe",
           "LnnKFe", "VQf4g", "qv3Dpe", "kno-rdesc", "SPZzOb"]

# Define a user-agent for making web requests.
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Configure Gemini
genai.configure(api_key=GeminiAPIKey)  # Gemini configuration

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, if user is asking open application you can give gogle search link, poems etc."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)
    return True

# Function to generate content using AI and save it to a file.
def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        # Build conversation history for Gemini
        conversation = []
        for msg in SystemChatBot + messages:
            role = "user" if msg["role"] in ["system", "user"] else "model"
            conversation.append({"role": role, "parts": [msg["content"]]})
        
        # Add current prompt to conversation
        conversation.append({"role": "user", "parts": [prompt]})
        
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(conversation)
        
        Answer = response.text
        
        # Update messages list
        messages.append({"role": "user", "content": prompt})
        messages.append({'role': 'assistant', 'content': Answer})
        
        return Answer

    Topic = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    # Save the generated content to a text file.
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding='utf-8') as file:
        file.write(ContentByAI)
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

# Function to search for a topic on Youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# Function to play a video on Youtube.
def PlayYoutube(query):
    playonyt(query)
    return True

# Function to open an application or a relevant webpage.
# def OpenApp(app, sess=requests.session()):
#     try:
#         appopen(app, match_closest=True, output=True, throw_error=True)
#         return True

#     except:
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')
#             links = soup.find_all('a', {'jsname': 'UWkNB'})
#             return [link.get('href') for link in links]

#         def search_google(query):
#             url = f"https://www.google.com/search?q={query}"
#             headers = {"User-Agent": useragent}
#             response = sess.get(url, headers=headers)

#             if response.status_code == 200:
#                 return response.text
#             else:
#                 print("Failed to retrieve search results.")
#             return None

#         html = search_google(app)

#         if html:
#             link = extract_links(html)[0]
#             webopen(link)

#         return True
    



def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:
        # def extract_links(html):
        #     if html is None:
        #         return []
        #     soup = BeautifulSoup(html, 'html.parser')
        #     links = []
        #     for a in soup.find_all('a', href=True):
        #         href = a['href']
        #         if href.startswith("/url?q="):
        #             url = href.split("/url?q=")[1].split("&")[0]
        #             if "google.com" not in url and "webcache.googleusercontent.com" not in url:
        #                 links.append(url)
        #     return links
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith("/url?q="):
                    url = href.split("/url?q=")[1].split("&")[0]
                    # Skip only real Google internal links and cache
                    if "webcache.googleusercontent.com" in url or "/search?" in url:
                        continue
                    links.append(url)
            return links

        def search_google1(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None

        html = search_google1(app)

        if html:
            links = extract_links(html)
            if links:
                webopen(links[0])
            else:
                print(f"No valid link found for {app}")
        return True
    
# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# Function to execute system level commands.
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")
    
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    if command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True

async def TranslateAndExecute(commands: list[str]):  # Fixed typo in parameter name
    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command or "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Function Found. For {command}!")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
           yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
       pass
    return True