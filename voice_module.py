import speech_recognition as sr
import pyttsx3
import time
from knowledge_module import wiki_search, gemini_query
from gui_module import message_queue

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(timeout=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=timeout)
    try:
        return recognizer.recognize_google(audio)
    except:
        return None

def start_hotword_listener(hotword="hey pi"):
    while True:
        print("Listening for hotword...")
        query = listen(timeout=3)
        if query and hotword.lower() in query.lower():
            message_queue.put("Bot: Hotword detected. Listening for command...")
            speak("Yes?")
            command = listen(timeout=5)
            if command:
                message_queue.put(f"You: {command}")
                # Decide source: Wikipedia or Gemini
                if "Wikipedia" in command or "search" in command:
                    cmd_clean = command.replace("Wikipedia", "").replace("search", "")
                    result = wiki_search(cmd_clean)
                else:
                    result = gemini_query(command)
                message_queue.put(f"Bot: {result}")
                speak(result)
