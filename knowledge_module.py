import wikipedia
import google.generativeai as genai

genai.configure(api_key="AIzaSyDP3nkgW-ZmL_YxNp8AeC4Qb0ViG1o72Sc")

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

