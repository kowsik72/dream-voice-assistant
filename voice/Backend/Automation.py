from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


client = Groq(api_key=GroqAPIKey)

# Define CSS classes for parsing specific elements in HTML content
classes = [
    "zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf",
    "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO",
    "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt",
    "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"
]

# Define a user-agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"


professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]


messages = [
]


SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, you're a content writer. You have to erite content like letter."}]

def GoogleSearch(Topic):
    search(Topic)
    return True


def Content(Topic): 
    # Nested function to open a file in Notepad
    def OpenNotepad(File): 
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad

    # Nested function to generate content using the AI chatbot
    def ContentWriterAI(prompt): 
        messages.append({"role": "user", "content": f"{prompt}"})  # Add user's prompt

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Specify the AI model
            messages=SystemChatBot + messages,  # Include system instructions & chat history
            max_tokens=2048,  # Limit response length
            temperature=0.7,  # Adjust response randomness
            top_p=1,  # Use nucleus sampling for response diversity
            stream=True,  # Enable streaming response
            stop=None  # Allow model to determine stopping conditions
        )

        Answer = ""
        for chunk in completion:  # Stream and concatenate the response
            if chunk.choices and chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer=Answer.replace("</s>","")
        messages.append({"role":"assistant","content": Answer})
        return Answer
    
        Topic = Topic.replace("Content ", "").strip()  # Remove "Content" prefix and strip spaces
    ContentByAI = ContentWriterAI(Topic)  # Generate content using AI

    file_name = rf"Data\{Topic.lower().replace(' ', '_')}.txt"  # Format filename
    
    # Save the generated content to a text file
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(ContentByAI)  # Write content to file

    OpenNotepad(file_name)  # Open the file in Notepad
    
    return True  # Indicate success




def YouTubeSearch(Topic):
    url = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(url)
    return True


def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app_name):
    try:
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        print(f" Successfully opened {app_name}.")
    except Exception as e:
        print(f" {app_name} is not installed locally. Searching online...")
        search_google(app_name)

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    print(f"🔗 Searching for {query} on Google: {url}")




from AppOpener import close  # Assuming `close` is a function from the AppOpener package
def CloseApp(app):
    restricted_apps = ["chrome", "brave"]
    if any(browser in app.lower() for browser in restricted_apps):
        print(f"⚠️ Not closing {app} to prevent unexpected behavior.")
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        print(f"✅ Successfully closed {app}.")
        return True
    except Exception as e:
        print(f"⚠️ Failed to close {app}. Error: {e}")
        return False



def System(command):
    # Nested function to mute the system volume
    def mute():
        keyboard.press_and_release("volume mute")

    # Nested function to unmute the system volume
    def unmute():
        keyboard.press_and_release("volume mute")  # Same as mute (toggle)

    # Nested function to increase the system volume
    def volume_up():
        keyboard.press_and_release("volume up")

    # Nested function to decrease the system volume
    def volume_down():
        keyboard.press_and_release("volume down")

    # Execute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True

import asyncio

async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks

    for command in commands:
        if command.startswith("open"):  # Handle "open" commands
            if "open it" in command or "open file" in command:
                continue  # Ignore these specific commands

            func = asyncio.to_thread(OpenApp, command.removeprefix("open ").strip())
            funcs.append(func)  # Schedule app opening

        elif command.startswith("close"):  # Handle "close" commands
            func = asyncio.to_thread(CloseApp, command.removeprefix("close ").strip())
            funcs.append(func)  # Schedule app closing

        elif command.startswith("content"):  # Handle "content" commands
            func = asyncio.to_thread(Content, command.removeprefix("content ").strip())
            funcs.append(func)  # Schedule content creation

        elif command.startswith("google search"):  # Handle Google search commands
            func = asyncio.to_thread(GoogleSearch, command.removeprefix("google search ").strip())
            funcs.append(func)  # Schedule Google search

        elif command.startswith("youtube search"):  # Handle YouTube search commands
            func = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ").strip())
            funcs.append(func)  # Schedule YouTube search

        elif command.startswith("system"):  # Handle system commands
            func = asyncio.to_thread(System, command.removeprefix("system ").strip())
            funcs.append(func)  # Schedule system command

        else:
            print(f"⚠️ No function found for: {command}")  # Print an error for unrecognized commands

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently

    for result in results:
        # Process the results
        if isinstance(result, str):
            yield result
        else:
            yield result
import asyncio

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass  # This iterates over the generator without doing anything
    
    return True  # Indicate successful execution



