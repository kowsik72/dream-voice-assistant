# import os
# import pygame

# def speak(text):
#     voice = "en-US-ChristopherNeural"

#     command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "audio/output.mp3"'

#     os.system(command)

#     pygame.init()
#     pygame.mixer.init()

#     try:
#         pygame.mixer.music.load("audio/output.mp3")

#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)

#     except Exception as e:
#         print(e)

#     finally:
#         pygame.mixer.music.stop()
#         pygame.mixer.quit()
        


import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()