import pygame
import asyncio
import edge_tts
import os
import random
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

SPEECH_FILE_PATH = r"Data\speech.mp3"

async def text_to_audio_file(text):
    if os.path.exists(SPEECH_FILE_PATH):
        os.remove(SPEECH_FILE_PATH)
    
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(SPEECH_FILE_PATH)

def play_audio(func=lambda: True):
    pygame.mixer.init()
    pygame.mixer.music.load(SPEECH_FILE_PATH)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        if not func():
            break
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

def TTS(text, func=lambda: True):
    try:
        asyncio.run(text_to_audio_file(text))
        play_audio(func)
        return True
    except Exception as e:
        print(f"Error in TTS: {e}")
        return False

def text_to_speech(text, func=lambda: True):
    sentences = text.split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(text) > 250:
        TTS(" ".join(sentences[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(text, func)

if __name__ == "__main__":
    while True:
        text_to_speech(input("Enter the text: "))
