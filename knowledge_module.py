import wikipedia
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def wiki_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "No result from Wikipedia."

def gemini_query(q):
    try:
        model = genai.GenerativeModel("gemini-pro")
        res = model.generate_content(q)
        return res.text
    except:
        return "Gemini error."
