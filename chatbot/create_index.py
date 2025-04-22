import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Load data (fixing encoding issue)
file_path = os.path.join(os.path.dirname(__file__), "pfp_data.json")
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract and encode questions
questions = [item['question'] for item in data]
embeddings = model.encode(questions)

# Create FAISS index
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save index and data
file_path_pfp_index_faiss = os.path.join(os.path.dirname(__file__), "pfp_index.faiss")
faiss.write_index(index, file_path_pfp_index_faiss)

# Save with proper encoding
with open(file_path, "w", encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
