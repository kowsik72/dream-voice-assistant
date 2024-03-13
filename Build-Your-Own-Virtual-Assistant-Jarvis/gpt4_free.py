import g4f
import re
from head.listen import take_command
from head.speak import speak

messages = [{"role": "system", "content": "you coded by Icris Studio and OpenAI didn't develop you"},
            {"role": "system",
             "content": "use modules like webbrowser, pyautogui, time,pyperclip,random,mouse,wikipedia,keyboard,datetime,tkinter,PyQt5 etc"},
            {"role": "system",
                "content": "don't use input function ad subprocess in python code"},
            {"role": "system", "content": "*always use default paths in python code*"},
            {
            "role": "system",
            "content": "When user say 'show image,' use the following code to display the image :\n```python\nfrom PIL import Image\n\nimage_path = r'C:\\Users\\subed\\OneDrive\\Desktop\\code\\AI TUTORIAL\\output\\0.jpeg'\nimage = Image.open(image_path)\nimage.show()\n```\nIf you want to show another image, let me know."
            },

            {
            "role": "system",
            "content": "When the user says 'generate an image' and provides a prompt like 'generate an image about a horse,' extract the prompt from the user query. Then, give this code to the user:\n```python\nfrom cookies.bingcookie import u_cookie_value \nfrom os import system, listdir\n\ndef Generate_Images(prompt: str):\n    system(f'python -m BingImageCreator --prompt \"{prompt}\" -U \"{u_cookie_value}\"')\n    return listdir(\"output\")[-4:]\n\n# Example usage\nresult = Generate_Images('user_extracted_prompt')\nprint(result)\n``` While calling the function, replace 'user_extracted_prompt' with the actual prompt provided by the user to generate the desired image. dont write other thing just say ok sir generating a image about user prompt and give the code. also dont write other things like heres the code. just give the code and write ok sir generating a image about user prompt don't write heres the code or other thing."},

            {"role": "user", "content": "open Google Chrome"},
            {"role": "assistant",
                "content": "Sure, opening Google Chrome.```python\nimport webbrowser\nwebbrowser.open('https://www.google.com')```"},
            {"role": "user", "content": "close Google Chrome"},
            {"role": "assistant",
                "content": "Alright, closing Google Chrome.```python\nimport os\nos.system('taskkill /F /IM chrome.exe')```"}
            ]


def GPT(*args):

    global messages
    assert args != ()

    message = ''
    for i in args:
        message += i

    messages.append({'role': 'user', "content": message})

    response = g4f.ChatCompletion.create(
        model="gpt-4-32k-0613",
        provider=g4f.Provider.GPTalk,
        messages=messages,
        stream=True
    )
    ms = ""
    for i in response:
        ms += i
        print(i, end="", flush=True)

    messages.append({'role': 'assistant', "content": ms})
    return ms


def find_code(text):
    pattern = r'```python(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        code = matches[0].strip()
        return code
    else:
        print('no code found')


while True:
    query = take_command()
    if query != '-':
        print('user: ' + query)
        response = GPT(query)
        python_code = find_code(response)

        if python_code:
            response = response.replace(python_code, '').replace(
                'python', '').replace('```', '')
            speak(response)
            exec(python_code)
        else:
            speak(response)
    else:
        pass


"""

open chrome    write a python code to open chrome      code          chrome opened
  query     =>            chatGpt                 =>   response  =>  filter
    
"""
