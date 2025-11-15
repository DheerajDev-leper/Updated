import threading
from gui_module import PiGPTBotGUI
from face_recognition_module import start_face_recognition
from voice_module import start_hotword_listener
import tkinter as tk

if __name__ == "__main__":
    # Start face recognition in background
    threading.Thread(target=start_face_recognition, daemon=True).start()

    # Start voice hotword listener
    threading.Thread(target=start_hotword_listener, daemon=True).start()

    # Start GUI
    root = tk.Tk()
    app = PiGPTBotGUI(root)
    root.mainloop()
