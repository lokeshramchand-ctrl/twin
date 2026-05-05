import os
import requests
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle

# =========================
# CONFIG
# =========================
OLLAMA_URL = "https://ollama.splsystems.in/api/generate"
MODEL_NAME = "gemma4:latest"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedder = SentenceTransformer(EMBED_MODEL)

# =========================
# DOCUMENT LOADING
# =========================
def load_documents(folder):
    docs = []
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), "r") as f:
            docs.append(f.read())
    return docs

# =========================
# CHUNKING
# =========================
def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

# =========================
# INDEX BUILDING
# =========================
def build_index(documents):
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc))

    embeddings = embedder.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, chunks

# =========================
# SAVE / LOAD
# =========================
def save_index(index, chunks, path="index"):
    faiss.write_index(index, f"{path}.faiss")

    with open(f"{path}.pkl", "wb") as f:
        pickle.dump(chunks, f)


def load_index(path="index"):
    index = faiss.read_index(f"{path}.faiss")

    with open(f"{path}.pkl", "rb") as f:
        chunks = pickle.load(f)

    return index, chunks

# =========================
# RETRIEVAL
# =========================
def retrieve(query, index, chunks, k=3):
    query_vec = embedder.encode([query])
    distances, indices = index.search(np.array(query_vec), k)

    return [chunks[i] for i in indices[0]]

# =========================
# OLLAMA CALL
# =========================
def query_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    return response.json().get("response", "[No response]")

# =========================
# RAG QUERY
# =========================
def rag_query(question, index, chunks):
    retrieved_docs = retrieve(question, index, chunks)
    context = "\n".join(retrieved_docs)

    prompt = f"""
Answer ONLY using the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    return query_ollama(prompt)