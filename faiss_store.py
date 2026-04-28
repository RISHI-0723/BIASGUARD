from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

known_terms = [
    "gender", "sex", "male female",
    "approved", "selected", "hired",
    "age", "race", "caste"
]

vectors = model.encode(known_terms)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors).astype("float32"))

def search_term(term, k=3):
    vec = model.encode([term]).astype("float32")
    D, I = index.search(vec, k)
    return [known_terms[i] for i in I[0]]