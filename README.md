# StudyBuddy – LLM Tutor with RAG, Safety, and Evaluation  
**Assignment 2 – CSCI Topics in Computer Science 1**

This project is a locally-running LLM tutor application called **StudyBuddy**.  
It uses a small open-source model (Gemma 2B) running through **Ollama**, and includes:

- A FastAPI backend  
- A simple HTML/CSS/JavaScript front-end  
- RAG (Retrieval-Augmented Generation) using course notes  
- Safety guardrails  
- Telemetry logging  
- Offline evaluation using a test suite (`tests.json`)  
- A reproducible environment with requirements.txt and seed files

---

## 🚀 Features Overview

### ✅ 1. **LLM Response Generation**
The backend sends prompts to a local LLM (`gemma:2b-instruct`) via Ollama’s REST API.

### ✅ 2. **RAG — Retrieval-Augmented Generation**
Before answering:
1. The user's message is embedded  
2. Compared to preloaded chunks from `seed_notes.txt`  
3. Top relevant chunks are added to the prompt  

This improves factual accuracy.

### ✅ 3. **Safety Guardrails**
Implemented safety includes:
- Prompt-injection detection  
- Forbidden keywords filter  
- Message length limits  
- System prompt rules (never reveal system prompt, stay in tutor mode)

### ✅ 4. **Auto Subject Detection**
If the user chooses **subject: auto**, the backend assigns:
- **linear algebra**  
- **math**  
- **computer science**  

Based on keyword matching.

### ✅ 5. **Offline Evaluation**
`run_tests.py` loads `tests.json` and measures:
- Quality of model answers  
- Consistency  
- Similarity to expected output  

Output appears in console.

### ✅ 6. **Telemetry Logging**
Every `/chat` request logs:
- Timestamp  
- Latency (ms)  
- Subject pathway  
- User message  
- Whether RAG was used  

Saved to `telemetry.log`.

---

## 📁 Project Structure
backend/
│── main.py # FastAPI backend
│── rag.py # Embeddings + similarity search
│── requirements.txt # Python dependencies
│── seed_notes.txt # Course notes for RAG
│── tests.json # Evaluation cases
│── run_tests.py # Evaluates model performance
│── telemetry.log # (auto-generated) logs
│── .env.example # Environment variables
│── run.sh # One-command run script
│── venv/ # Virtual environment (ignored)
frontend/
│── index.html
│── script.js
│── styles.css

---

## 🧩 Installation & Setup

### 1️⃣ Install Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2️⃣ Install Ollama

For Linux:

curl https://ollama.ai/install.sh | sh

3️⃣ Pull the model
ollama pull gemma:2b-instruct

4️⃣ Confirm Ollama is running
systemctl status ollama


Backend expects Ollama at:

http://localhost:11434

▶️ One-Command Run

Activate virtual environment and start FastAPI:

sh run.sh


If Windows (PowerShell):

./run.ps1


This launches the server at:

http://127.0.0.1:8000


Open the frontend (index.html) using Live Server or any static server.

🎯 How RAG Works (Summary)

seed_notes.txt → loaded at startup

Notes → split into chunks

Each chunk → embedded via embedding model

Query → embedded

Top chunks selected using cosine similarity

Inserted into LLM prompt under Relevant course notes

If no relevant chunks exist, the bot still answers using its base model.

🔐 Safety Design

Rejects prompt injections (ignore previous, jailbreak, etc.)

Filters harmful / manipulative instructions

Rejects extremely long messages

System prompt enforces tutor mode & safe behaviour

📊 Running Offline Evaluation

You can evaluate the model with:

python run_tests.py


This prints:

For each test: pass/fail + similarity score

A final average performance score

🛠 Environment Variables

.env.example shows default values:

MODEL=gemma:2b-instruct
OLLAMA_URL=http://localhost:11434/api/generate


Create your own .env file:

cp .env.example .env

🎥 Video Requirements (Not included)

You still need to record a 3–5 minute demo video:

What your app does

How to use it

Architecture explanation

Show tests & RAG

👤 Author

Jugal Patel
Ontario Tech University
StudyBuddy – Assignment 2