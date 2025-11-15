import speech_recognition as sr
import pyttsx3
from queue import Queue

message_queue = Queue()

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

USB_MIC_INDEX = None   # Automatically detected later


def detect_microphone_index():
    """Find the index of the USB microphone (card 3)."""
    global USB_MIC_INDEX
    p = sr.Microphone.list_microphone_names()

    print("\nAvailable Audio Devices:")
    for i, name in enumerate(p):
        print(f"{i}: {name}")

    # Automatically detect a USB mic
    for i, name in enumerate(p):
        if "USB" in name or "Array" in name or "Microphone" in name:
            USB_MIC_INDEX = i
            print(f"\nSelected USB microphone index: {USB_MIC_INDEX}")
            return

    # fallback
    USB_MIC_INDEX = 0
    print("\n⚠️ No USB mic detected. Using default mic.")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen(timeout=4):
    """Listen using the selected microphone."""
    r = sr.Recognizer()

    with sr.Microphone(device_index=USB_MIC_INDEX) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=timeout)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except:
        print("❌ Could not understand audio")
        return None


def hotword_listener(hotword="hey pi"):
    """Always running background listener."""
    while True:
        print("Waiting for hotword...")
        query = listen(timeout=3)

        if query and hotword.lower() in query.lower():
            speak("Yes?")
            message_queue.put("Bot: Hotword detected")

            command = listen(timeout=6)
            if command:
                message_queue.put("You: " + command)
                return command
            else:
                speak("I didn't catch that.")
                message_queue.put("Bot: No command heard")
