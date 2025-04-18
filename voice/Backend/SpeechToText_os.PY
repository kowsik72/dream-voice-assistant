import os
import speech_recognition as sr
import mtranslate as mt
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

# Function to modify and format queries
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += ","
    return new_query.capitalize()

# Function to translate text to English if needed
def UniversalTranslator(Text):
    return mt.translate(Text, "te", "auto").capitalize()

# Function to perform speech recognition
def SpeechRecognition():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized Text: {text}")

        if "en" in InputLanguage.lower():
            return QueryModifier(text)
        else:
            SetAssistantStatus("Translating...")
            return QueryModifier(UniversalTranslator(text))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Function to set the assistant's status (optional feature)
def SetAssistantStatus(Status):
    with open('assistant_status.txt', "w", encoding='utf-8') as file:
        file.write(Status)

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()  # Perform speech recognition
        if Text:
            print(f"Processed Text: {Text}")
