import pyaudio
import sounddevice as sd
import numpy as np
threshold=1.0
clap=False

def detect(indata,frames,time,status):
    global clap
    volume=np.linalg.norm(indata)*10
    if volume>threshold:
        print("claped")
        clap=True
def listen():
    with sd.InputStream(callback=detect):
        return sd.sleep(1000)
if __name__== "__main__":
    while True:
        listen()
        if clap==True:
            break
        else:
            pass