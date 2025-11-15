import speech_recognition as sr
import pyttsx3
from queue import Queue

message_queue = Queue()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=4):
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=timeout)

    try:
        return r.recognize_google(audio)
    except:
        return None

def hotword_listener(hotword="hey pi"):
    while True:
        print("Listening for hotword...")
        query = listen(timeout=3)

        if query and hotword.lower() in query.lower():
            speak("Yes?")
            message_queue.put("Bot: Hotword detected")

            command = listen(timeout=5)
            return command
