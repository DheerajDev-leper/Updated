from threading import Thread
from voice_module import hotword_listener, speak, message_queue
from knowledge_module import wiki_search, gemini_query
from face_recognition_module import start_face_detection
from gui_module import start_gui

def assistant_loop():
    while True:
        command = hotword_listener()

        if not command:
            continue

        message_queue.put(f"You: {command}")

        if "wiki" in command or "search" in command:
            query = command.replace("search", "").replace("wiki", "")
            result = wiki_search(query)
        else:
            result = gemini_query(command)

        message_queue.put("Bot: " + result)
        speak(result)

def run():
    Thread(target=start_gui).start()
    Thread(target=start_face_detection).start()
    Thread(target=assistant_loop).start()

if __name__ == "__main__":
    run()
