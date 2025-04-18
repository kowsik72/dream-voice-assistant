from groq import Groq
import datetime
import requests
import json
from dotenv import dotenv_values
# In Backend/RealtimeSearchEngine.py
from selenium import webdriver

env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")
api_key = env_vars.get("googleapikey")

# Validate API Key
if not api_key:
    raise ValueError("❌ Google API key is missing! Please check your .env file.")

client = Groq(api_key=GroqAPIKey)

# System Prompt for the AI
System = f"""Hello, I am {Username}. You are an advanced AI chatbot named {Assistantname} with real-time up-to-date information.
*** Provide answers professionally with proper grammar. ***
*** Just answer the question concisely. ***
"""

# Function to get real-time date & time
def get_realtime_info():
    now = datetime.datetime.now()
    return f"Day: {now.strftime('%A')}, Date: {now.strftime('%d %B %Y')}, Time: {now.strftime('%H:%M:%S')}"

# Function to load chat history
def load_chat_history():
    try:
        with open("Data/ChatLog.json", "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Return empty chat history if file is corrupted or missing

# Function to save chat history
def save_chat_history(messages):
    with open("Data/ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)

# Function to clean and format the answer
def answer_modifier(Answer):
    return " ".join(line for line in Answer.split() if line.strip())

# Function to fetch Google Search results using SerpAPI
def google_search(query):
    url = f"https://serpapi.com/search?q={query}&api_key={api_key}&num=5"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "organic_results" not in data:
            return "⚠️ No valid search results found."

        answer = f"The search results for '{query}' are:\n[start]\n"
        for i, result in enumerate(data["organic_results"], start=1):
            title = result.get("title", "No Title")
            description = result.get("snippet", "No Description")
            link = result.get("link", "No URL")
            answer += f"🔹 **{title}**\n{description}\n🔗 {link}\n\n"
        
        return answer + "[end]"
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error fetching Google results: {e}"

# Function to perform a real-time AI-powered search
def RealtimeSearchEngine(prompt):
    messages = load_chat_history()
    
    # Fetch search results
    search_results = google_search(prompt)
    messages.append({"role": "user", "content": search_results})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": System + "\n" + get_realtime_info()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True
    )

    # Process AI-generated response
    answer = "".join(chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content).strip()
    answer = answer.replace("</s>", "")

    # Update chat log
    messages.append({"role": "assistant", "content": answer})
    save_chat_history(messages)

    return answer_modifier(answer)

# Run the search engine in a loop
if __name__ == "__main__":
    while True:
        user_input = input("Enter your query: ")
        print(RealtimeSearchEngine(user_input))
