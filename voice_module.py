import speech_recognition as sr
import pyttsx3
import time
import queue
from knowledge_module import wiki_search, gemini_query
from gui_module import message_queue

# -----------------------------
#  TEXT-TO-SPEECH ENGINE
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)


def speak(text):
    message_queue.put(f"Bot: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass


# -----------------------------
#  OFFLINE SPEECH (VOSK) SETUP
# -----------------------------
USE_VOSK = False
try:
    from vosk import Model, KaldiRecognizer
    import json
    USE_VOSK = True
    model = Model("/home/pi/vosk-model-small-en-us-0.15")  # <- Change to your model folder
except:
    print("Vosk not available. Using Google STT only.")


# -----------------------------
#  LISTEN FUNCTION
# -----------------------------
def listen(timeout=5):
    recognizer = sr.Recognizer()

    # IMPORTANT: Raspberry Pi USB MIC is usually device_index=3
    mic = sr.Microphone(device_index=3)

    with mic as source:
        print("\n[LISTENING...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, phrase_time_limit=timeout)
        except Exception as e:
            print("Mic error:", e)
            return None

    # -----------------------------
    # Try Google STT
    # -----------------------------
    try:
        text = recognizer.recognize_google(audio)
        print("Recognized (Google):", text)
        return text
    except Exception as e:
        print("Google STT failed:", e)

    # -----------------------------
    # Try Offline VOSK
    # -----------------------------
    if USE_VOSK:
        try:
            recognizer_vosk = KaldiRecognizer(model, 16000)
            data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            if recognizer_vosk.AcceptWaveform(data):
                result = json.loads(recognizer_vosk.Result())
                print("Recognized (Vosk):", result.get("text", ""))
                return result.get("text", "")
            else:
                partial = json.loads(recognizer_vosk.PartialResult())
                return partial.get("partial", "")
        except Exception as e:
            print("Vosk failed:", e)

    return None


# -----------------------------
#  HOTWORD LISTENER
# -----------------------------
def start_hotword_listener(hotword="hey pi"):
    speak("Voice system activated.")

    while True:
        print("\n--- Waiting for hotword ---")
        query = listen(timeout=3)
        print("Heard:", query)

        if not query:
            continue

        # Hotword detected
        if hotword.lower() in query.lower():
            message_queue.put("Bot: Hotword detected. Listening for command...")
            speak("Yes?")

            command = listen(timeout=5)
            print("Command:", command)

            if not command:
                speak("I didn't hear any command.")
                continue

            message_queue.put(f"You: {command}")

            # -----------------------------
            # COMMAND PROCESSING
            # -----------------------------
            if "Wikipedia" in command or "search" in command:
                cmd_clean = command.replace("Wikipedia", "").replace("search", "")
                result = wiki_search(cmd_clean)
            else:
                result = gemini_query(command)

            speak(result)
