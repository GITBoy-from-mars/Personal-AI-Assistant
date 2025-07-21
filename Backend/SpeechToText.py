from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

import os, sys
# Load environment variables

# base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
# env_path = os.path.join(base_path, '.env')

# # Now load the .env variables correctly
# env_vars = dotenv_values(env_path)



# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
# Get the input language setting from the environment variables.
InputLanguage = env_vars.get("InputLanguage")

# Define the HTML code for the speech recognition interface.
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with the input language from the environment variables.
HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file.
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the curr
current_dir = os.getcwd()
# Generate the file path for the HTML file.
Link = f'{current_dir}/Data/Voice.html'

# Set Chrome options for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.143.86 Safari/537.36"
chrome_options.add_argument(f"--user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
})
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-client-side-phishing-detection")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--disable-site-isolation-trials")
chrome_options.add_argument("--disable-features=NetworkService")
# chrome_options.add_argument("--disable-usb-keyboard-detect")
# chrome_options.add_argument("--disable-usb-detection")
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# # chrome_options.add_argument("--disable-logging")
# # chrome_options.add_argument("--log-level=3")
# # chrome_options.add_argument("--disable-dev-shm-usage")
# # chrome_options.add_argument("--no-sandbox")


# Initialize the Chrome WebDriver using the ChromeDriverManager.
Service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service, options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())

# Define the
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant's status by writing it to a file.
def SetAssistantStatus(Status):
    with open(f"{TempDirPath}/Status.data", "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting.
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "can you"]

    # Check if the query is a question and add a question mark if necessary.
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        # Add a period if the query is not a question.
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using the WebDriver.






















def SpeechRecognition():
    driver.get("file:///" + Link)
    time.sleep(1)  # Let page load

    # Click start
    driver.find_element(By.ID, "start").click()
    print("[INFO] Listening...")

    timeout = 15  # seconds to wait
    previous_text = ""
    start_time = time.time()

    while True:
        try:
            current_text = driver.find_element(By.ID, "output").text.strip()

            # If there's a new result, break
            if current_text and current_text != previous_text:
                print("[INFO] Speech detected.")
                driver.find_element(By.ID, "end").click()

                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(current_text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(current_text))

            previous_text = current_text

        except Exception as e:
            print(f"[WARN] Error reading speech output: {e}")

        # Timeout after 15 seconds
        if time.time() - start_time > timeout:
            print("[ERROR] Timeout: No speech detected.")
            driver.find_element(By.ID, "end").click()
            return ""

        time.sleep(1) 





# def SpeechRecognition():
#     # Open the HTML file in the browser.
#     driver.get("file:///" + Link)

#     # Start speech recognition by clicking the start button.
#     driver.find_element(by=By.ID, value="start").click()

#     while True:
#        try:
#             # Get the recognized text from the HTML output element.
#             Text = driver.find_element(by=By.ID, value="output").text

#             if Text:
#                 # Stop recognition by clicking the stop button.
#                 driver.find_element(by=By.ID, value="end").click()

#             if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
#                 return QueryModifier(Text)
#             else:
#                 # If the input language is not English, translate the text and return it.
#                 SetAssistantStatus("Translating...")
#                 return QueryModifier(UniversalTranslator(Text))

#        except Exception as e:
#            pass

# Main execution block.
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)