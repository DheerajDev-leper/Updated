import wikipedia
import requests

# Gemini API key
GEMINI_API_KEY = "AIzaSyDP3nkgW-ZmL_YxNp8AeC4Qb0ViG1o72Sc"
GEMINI_ENDPOINT = "https://api.gemini.com/v1/query"  # Replace with correct Gemini endpoint

def wiki_search(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return "Sorry, I could not find that on Wikipedia."

def gemini_query(query):
    """
    Sends query to Gemini API and returns response text.
    """
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": query,
        "max_tokens": 150
    }

    try:
        response = requests.post(GEMINI_ENDPOINT, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            # Adjust based on Gemini API response format
            return result.get("answer", "Gemini could not generate a response.")
        else:
            return f"Gemini API error: {response.status_code}"
    except Exception as e:
        return f"Error contacting Gemini API: {e}"
