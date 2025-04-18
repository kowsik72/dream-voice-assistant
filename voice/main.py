from Backend.ImageGenration import GenerateImages
from Frontend.GUI import ( 
    GraphicalUserInterface, 
    TempDirectoryPath, 
    SetMicrophoneStatus, 
    SetAssistantStatus, 
    ShowTextToScreen, 
    AnswerModifier, 
    QueryModifier, 
    GetMicrophoneStatus, 
    GetAssistantStatus)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import text_to_speech  # Ensure this is a function, not a class
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os


# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# Default message template
DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

# Background processes list
subprocesses = []

# List of recognized commands
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Function to check and show default chat if no previous chats exist
def ShowDefaultChatIfNoChats():
    try:
        with open(r"Data\ChatLog.json", "r", encoding="utf-8") as file:
            if len(file.read()) < 5:  # If the chat log is empty or very short
                with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as db_file:
                    db_file.write("")
                with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as response_file:
                    response_file.write(DefaultMessage)
    except FileNotFoundError:
        # If the file doesn't exist, create it with default messages
        with open(r"Data\ChatLog.json", "w", encoding="utf-8") as file:
            file.write("[]")  # Write an empty JSON array
        with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as db_file:
            db_file.write("")
        with open(TempDirectoryPath("Responses.data"), "w", encoding="utf-8") as response_file:
            response_file.write(DefaultMessage)
import json

def ReadChatLogJson():
    """Reads and returns the chat log data from a JSON file."""
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
            chatlog_data = json.load(file)
        return chatlog_data
    except FileNotFoundError:
        return []  # If file doesn't exist, return an empty list

def ChatLogIntegration():
    """Formats chat log data and saves it to a temporary database file."""
    json_data = ReadChatLogJson()  # ✅ Fixed variable assignment
    formatted_chatlog = ""

    for entry in json_data: 
        if entry["role"] == "user":  # ✅ Fixed comparison operator
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"  # ✅ Fixed string concatenation

    # Replace generic role names with actual assistant & user names
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    # Save to the database file
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))  # ✅ Fixed function call


def ShowChatsOnGUI():
    """Reads chat data from the database and updates the GUI responses."""
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            Data = file.read()  # ✅ Fixed variable assignment

        if len(Data.strip()) > 0:  # ✅ Stripping extra spaces before checking length
            lines = Data.split('\n')
            result = '\n'.join(lines)

            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                file.write(result)  # ✅ Fixed file writing

    except FileNotFoundError:
        print("⚠️ Database file not found. Skipping GUI update.")

def InitialExecution():
    """Initializes the chat system and GUI components."""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()  # ✅ Ensures it only runs when the script is executed directly
import asyncio

def MainExecution():
    """Main function to process user queries and execute tasks."""
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")

    Decision = FirstLayerDMM(Query)

    print("\n")
    print(f"Decision: {Decision}")
    print("\n")

    # Extracting General and Realtime Queries
    Gany = [i for i in Decision if i.startswith("general")]
    Rany = [i for i in Decision if i.startswith("realtime")]

    # Creating Merged Query (Combining general & real-time queries)
    MergedQuery = " and ".join(
        ["".join(i.split()[1:]) for i in Decision if i.startswith(("general", "realtime"))]
    )

    # Handling Image Generation
    for queries in Decision:
        if queries.startswith("generate"):
            ImageGenerationQuery = queries
            ImageExecution = True
            break  # Exit loop after first valid query

    # Handling Automation Commands (Open, Close, Play, etc.)
    for queries in Decision:
        if any(queries.startswith(func) for func in Functions):
            print(f"🔄 Executing Automation: {queries}")
            asyncio.run(Automation([queries]))  
            TaskExecution = True

    # Handling Image Generation Execution
    if ImageExecution:
                print(f"🖼️ Generating Image: {ImageGenerationQuery}")
                with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
                    file.write(f"{ImageGenerationQuery}, True")
                try:
                    # Direct image generation call
                    GenerateImages(ImageGenerationQuery.replace("generate image ", "").strip())
                    ShowTextToScreen(f"{Assistantname}: Image generated successfully!")
                    SetAssistantStatus("Answering...")
                    text_to_speech("Your image is ready to view!")
                    
                    # Reset microphone status after completion
                    SetMicrophoneStatus("False")
                    return  # Exit early after image generation
                    
                except Exception as e:
                    print(f"⚠️ Image generation failed: {e}")
                    ShowTextToScreen(f"{Assistantname}: Failed to generate image")
                    text_to_speech("Sorry, I couldn't create that image")

    # Handling General and Realtime Queries
    if (Gany and Rany) or Rany:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        text_to_speech(Answer)

    elif Gany:
        SetAssistantStatus("Thinking...")
        QueryFinal = MergedQuery.replace("general", "").strip()
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        text_to_speech(Answer)

    elif "exit" in Decision:
        print("👋 Exiting...")
        SetAssistantStatus("Answering...")
        text_to_speech("Okay, Bye!")
        os._exit(1)

def FirstThread():
    """Continuously checks microphone status and executes commands."""
    while True:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":  # Fixed syntax for comparison
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    """Launches the Graphical User Interface."""
    GraphicalUserInterface()

if __name__ == "__main__":
    thread1 = threading.Thread(target=FirstThread, daemon=True)  # Corrected threading syntax
    thread1.start()

    SecondThread()  # GUI runs in the main thread