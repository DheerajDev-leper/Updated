import tkinter as tk
from queue import Queue
message_queue = Queue()

def start_gui():
    root = tk.Tk()
    root.title("Pi AI Assistant")
    root.geometry("500x600")

    chat = tk.Text(root, bg="black", fg="white", font=("Arial", 12))
    chat.pack(fill="both", expand=True)

    def update_chat():
        while not message_queue.empty():
            msg = message_queue.get()
            chat.insert(tk.END, msg + "\n")
            chat.see(tk.END)
        root.after(200, update_chat)

    update_chat()
    root.mainloop()
