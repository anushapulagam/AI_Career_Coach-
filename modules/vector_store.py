import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_job_descriptions(json_path):
    try:
        with open(json_path, "r") as f:
            jobs = json.load(f)
        if not jobs or len(jobs) == 0:
            raise ValueError("Job descriptions file is empty.")
        return jobs
    except FileNotFoundError:
        raise FileNotFoundError("❌ data/job_descriptions.json not found. Please create this file.")
    except json.JSONDecodeError:
        raise ValueError("❌ job_descriptions.json has invalid format. Please check the file.")

def build_vector_store(jobs):
    try:
        descriptions = [job["description"] for job in jobs]
        embeddings = model.encode(descriptions)
        embeddings = np.array(embeddings).astype("float32")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, descriptions, jobs
    except Exception as e:
        raise RuntimeError(f"❌ Failed to build vector store: {str(e)}")

def search_job(query, index, jobs, top_k=1):
    try:
        if not query.strip():
            raise ValueError("Job role cannot be empty.")
        query_vector = model.encode([query])
        query_vector = np.array(query_vector).astype("float32")
        distances, indices = index.search(query_vector, top_k)
        best_match = jobs[indices[0][0]]
        return best_match
    except Exception as e:
        raise RuntimeError(f"❌ Search failed: {str(e)}")
