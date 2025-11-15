import tkinter as tk
from tkinter import scrolledtext
import time
import queue

message_queue = queue.Queue()

class PiGPTBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi GPT Bot - Alexa Style")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E1E")

        # Canvas for face
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.head = self.canvas.create_oval(50, 50, 250, 250, fill="#4caf50", outline="")
        self.left_eye = self.canvas.create_oval(90, 100, 130, 140, fill="white")
        self.right_eye = self.canvas.create_oval(170, 100, 210, 140, fill="white")
        self.left_pupil = self.canvas.create_oval(105, 115, 115, 125, fill="black")
        self.right_pupil = self.canvas.create_oval(185, 115, 195, 125, fill="black")
        self.mouth = self.canvas.create_arc(100, 170, 200, 210, start=0, extent=-180, fill="black")

        # Chat display
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Helvetica", 12), state=tk.DISABLED)
        self.text_area.pack(padx=10, pady=10)

        # Clear chat button
        self.btn_frame = tk.Frame(root, bg="#1E1E1E")
        self.btn_frame.pack(pady=10)
        self.clear_btn = tk.Button(self.btn_frame, text="Clear Chat", command=self.clear_chat, bg="#f44336", fg="white", font=("Helvetica", 12))
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.update_text()
        self.blink()

    def update_text(self):
        while not message_queue.empty():
            msg = message_queue.get()
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, msg + "\n")
            self.text_area.config(state=tk.DISABLED)
            self.text_area.see(tk.END)
            if "Bot:" in msg:
                self.canvas.itemconfig(self.mouth, start=0, extent=180)
                self.root.update()
                time.sleep(0.3)
                self.canvas.itemconfig(self.mouth, start=0, extent=-180)
        self.root.after(100, self.update_text)

    def clear_chat(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

    def blink(self):
        self.canvas.itemconfig(self.left_eye, fill="#1E1E1E")
        self.canvas.itemconfig(self.right_eye, fill="#1E1E1E")
        self.root.update()
        time.sleep(0.1)
        self.canvas.itemconfig(self.left_eye, fill="white")
        self.canvas.itemconfig(self.right_eye, fill="white")
        self.root.after(4000, self.blink)
