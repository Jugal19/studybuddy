import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

with open("seed_notes.txt", "r") as f:
    NOTES = f.read().split("\n")

def retrieve_relevant_chunks(query, top_k=3):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(NOTES + [query])
    notes_vecs = vectors[:-1]
    query_vec = vectors[-1]

    sims = notes_vecs @ query_vec.T
    sims = sims.toarray().flatten()

    idxs = np.argsort(sims)[::-1][:top_k]
    return "\n".join([NOTES[i] for i in idxs])
