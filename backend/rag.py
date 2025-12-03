# rag.py
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

NOTES_FILE = "seed_notes.txt"

# -----------------------------
# Load notes file
# -----------------------------
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into chunks (paragraph-based)
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks


notes = load_notes()
vectorizer = TfidfVectorizer().fit(notes)
note_vectors = vectorizer.transform(notes)


# -----------------------------
# RAG Retrieval
# -----------------------------
def get_relevant_chunks(question: str, top_k=2):
    if not notes:
        return ""  # file missing = return safe empty text

    q_vec = vectorizer.transform([question])
    scores = (note_vectors * q_vec.T).toarray().ravel()

    top_indices = np.argsort(scores)[-top_k:]
    top_chunks = [notes[i] for i in top_indices if scores[i] > 0]

    if not top_chunks:
        return "No directly relevant notes found."

    return "\n\n".join(top_chunks)
