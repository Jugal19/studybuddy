# StudyBuddy – Assignment 2 (LLM App)

StudyBuddy is a lightweight local LLM-powered tutor for math, CS, and linear algebra.  
It supports Retrieval-Augmented Generation (RAG), includes guardrails, telemetry,
and an offline evaluation suite, and runs fully locally using Ollama.

---

## 🚀 Features

### ✔ Core LLM Feature
Users type a question into the frontend and receive a structured explanation generated
by a local LLM (Gemma 2B). The backend applies:
- A controlled system prompt
- Subject detection (math / CS / linear algebra)
- Safety guardrails
- Optional RAG to improve grounding

### ✔ Enhancement: RAG (Retrieval-Augmented Generation)
Relevant chunks are retrieved from `seed_notes.txt` using TF-IDF + cosine similarity.
The top-scoring chunks are injected into the prompt before sending to the LLM.

### ✔ Safety Guardrails
- Prompt-injection filter (blocks “ignore previous…” etc.)
- Input length limit (max 500 chars)
- CORS restrictions
- Fallback error messages
- JSON-safe response handling

### ✔ Telemetry
Each request logs:
- Timestamp  
- Latency  
- Subject  
- User question  
- Pathway (`"RAG"`)  

Stored in `telemetry.log`.

### ✔ Offline Evaluation
A `tests.json` file (≥15 tests) and a runner script `run_tests.py`
evaluate correctness using simple keyword pattern matching.

---

## 📦 Project Structure

---
studybuddy/
├── backend/
│ ├── main.py
│ ├── rag.py
│ ├── seed_notes.txt
│ ├── telemetry.log
│ ├── tests.json
│ ├── run_tests.py
│ ├── requirements.txt
│ ├── .env.example
│ └── (optional venv)
│
└── frontend/
├── index.html
├── script.js
└── styles.css
---


---

# 🛠 Installation & Running the App

## 1️⃣ Backend Setup (FastAPI + Ollama)

### Install dependencies
```
cd backend
pip install -r requirements.txt
```

### Start the backend
`uvicorn main:app --reload`


### Make sure Ollama is running in the background  
Olama model pull:
`ollama pull gemma:2b-instruct`


---

## 2️⃣ Frontend (No Live Server Needed)

### 🚨 IMPORTANT NOTE ABOUT LIVE SERVER (BUG WARNING)

Visual Studio Code's Live Server **automatically reloads the page** when:
- Backend responses are slow (e.g., 10–20 seconds from Ollama)
- Files change
- The browser detects a stalled request  
- Long-running AI responses occur

This causes the **entire chat to refresh** and messages disappear.

### ✅ FIX: Open index.html *directly* from the filesystem

Instead of Live Server, use:

1. Navigate to the `frontend` folder  
2. **Double-click `index.html`**, or open it in your browser via:

file:///path/to/studybuddy/frontend/index.html


This is the intended way to run the frontend because:
- Our backend CORS allows file:// origin  
- No auto-refresh  
- No disappearing messages  
- Works consistently with Ollama  

> **Professor:** Please open `index.html` from the folder, not Live Server,
> to avoid the known Live Server auto-reload bug with long-running LLM responses.

---

# 🧪 Offline Evaluation (Required for Assignment)

The `tests.json` file contains ≥15 tests.  
Run:

```
cd backend
python3 run_tests.py
```