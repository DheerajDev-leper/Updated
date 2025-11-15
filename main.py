import threading
import tkinter as tk
from gui_module import PiGPTBotGUI
from face_recognition_module import start_face_recognition
from voice_module import start_hotword_listener


def run_face_recognition():
    try:
        start_face_recognition()
    except Exception as e:
        print("[ERROR] Face Recognition crashed:", e)


def run_voice_listener():
    try:
        start_hotword_listener()
    except Exception as e:
        print("[ERROR] Voice Listener crashed:", e)


if __name__ == "__main__":
    # Start Face Recognition Thread
    face_thread = threading.Thread(
        target=run_face_recognition,
        daemon=True
    )
    face_thread.start()

    # Start Hotword Listener Thread
    hotword_thread = threading.Thread(
        target=run_voice_listener,
        daemon=True
    )
    hotword_thread.start()

    # Start GUI
    root = tk.Tk()
    app = PiGPTBotGUI(root)

    print("Pi GPT Bot Started Successfully ✔")
    print(" - Face Recognition Running")
    print(" - Hotword Detection Running")
    print(" - GUI Active")

    root.mainloop()

    print("Shutting down Pi GPT Bot...")
