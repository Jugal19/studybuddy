from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import time
import json
from datetime import datetime
from urllib.parse import quote

# Your local model
MODEL = "qwen2.5:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    topic: str


# ================================================================
#  FIXED WIKIPEDIA SEARCH (supports all casing + underscores)
# ================================================================
def get_wikipedia_summary(topic: str):
    """Retrieve a clean summary from Wikipedia using multiple fallback strategies."""

    def fetch(query):
        encoded = quote(query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        try:
            r = requests.get(url, timeout=10)

            if r.status_code == 200:
                data = r.json()

                # Reject "not_found" responses
                if data.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
                    return None

                return data.get("extract")
        except:
            return None

    # Wikipedia page titles can vary in capitalization + underscores
    attempts = [
        topic,                                 # linear algebra
        topic.replace(" ", "_"),               # linear_algebra
        topic.title(),                         # Linear Algebra
        topic.title().replace(" ", "_"),       # Linear_Algebra
        topic.capitalize(),                    # Linear algebra
        topic.capitalize().replace(" ", "_"),  # Linear_algebra (correct page)
    ]

    for attempt in attempts:
        result = fetch(attempt)
        if result:
            return result

    return None


# ================================================================
#  QUIZ GENERATION ENDPOINT
# ================================================================
@app.post("/quiz")
async def quiz(req: UserInput):
    start = time.time()

    topic = req.topic.strip()
    if not topic:
        return {"error": "Please enter a topic."}

    # 1. Get Wikipedia summary
    wiki_text = get_wikipedia_summary(topic)

    if not wiki_text:
        return {"error": "Topic not found on Wikipedia."}

    # 2. Build prompt for Qwen
    prompt = f"""
You are StudyBuddy.

Using ONLY the following text from Wikipedia:

\"\"\"{wiki_text}\"\"\"

Generate EXACTLY 3 quiz questions about this topic.
The questions must be:
- clear
- factual
- short
- beginner-friendly

Do NOT include answers. Only questions.
"""

    # 3. Call Qwen via Ollama
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=180
        )

        print("\n================ RAW OLLAMA RESPONSE ================")
        print(response.text)
        print("=====================================================\n")

        res = response.json()

        # Handle Ollama output variations
        if "response" in res:
            raw_output = res["response"]
        elif "output" in res:
            raw_output = res["output"]
        else:
            return {"error": f"Unexpected Ollama output: {res}"}

    except Exception as e:
        return {"error": f"Ollama error: {e}"}

    # 4. Split questions cleanly
    questions = [q.strip() for q in raw_output.split("\n") if q.strip()]

    return {"questions": questions}
