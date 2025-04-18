from groq import Groq
import datetime
from dotenv import dotenv_values
import json
import os

# Load Environment Variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# System Prompt for the Chatbot
System = f"""Hello, I am {Username}. You are an advanced AI chatbot named {Assistantname} with real-time up-to-date information.
*** Do not tell time unless asked. ***
*** Reply only in English, even if the question is in another language. ***
*** Just answer concisely, no unnecessary details. ***
"""

# Function to get real-time information
def RealtimeInformation():
    now = datetime.datetime.now()
    return f"Day: {now.strftime('%A')}, Date: {now.strftime('%d %B %Y')}, Time: {now.strftime('%H:%M:%S')}"

# Initialize System Messages
SystemChatBot = [{"role": "system", "content": System + "\n" + RealtimeInformation()}]

# Load chat history
chat_log_path = "Data/ChatLog.json"
if not os.path.exists(chat_log_path):
    with open(chat_log_path, "w") as f:
        json.dump([], f)

def load_chat_history():
    try:
        with open(chat_log_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Return empty chat history if file is corrupted or missing

def save_chat_history(messages):
    with open(chat_log_path, "w") as f:
        json.dump(messages, f, indent=4)

def AnswerModifier(Answer):
    return "\n".join(line for line in Answer.split("\n") if line.strip())

def ChatBot(Query):
    try:
        messages = load_chat_history()
        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        # Collect response
        Answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content)
        Answer = Answer.replace("</s>", "").strip()

        messages.append({"role": "assistant", "content": Answer})
        save_chat_history(messages)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return "I'm sorry, I encountered an issue. Please try again later."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
