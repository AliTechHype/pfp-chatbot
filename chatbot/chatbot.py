# chatbot.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os

# Load components
model = SentenceTransformer('all-MiniLM-L6-v2')
index_path = os.path.join(os.path.dirname(__file__), "pfp_index.faiss")
print("file path: ",os.path.join(os.path.dirname(__file__), "pfp_index.faiss"))
index = faiss.read_index(index_path)
# index = faiss.read_index("pfp_index.faiss")

pfp_data_file_path = os.path.join(os.path.dirname(__file__), "pfp_data.json")
with open(pfp_data_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Optional: Use huggingface for text generation
generator = pipeline("text-generation", model="distilgpt2")

# def get_answer(user_input):
#     query_embedding = model.encode([user_input])
#     _, I = index.search(np.array(query_embedding), k=1)
#
#     best_match = data[I[0][0]]
#     question, answer = best_match['question'], best_match['answer']
#
#     # Optional: make response more conversational
#     prompt = f"User asked: {user_input}\nBased on: {answer}\nChatbot says:"
#     generated = generator(prompt, max_length=80, do_sample=True)[0]['generated_text']
#
#     return generated.split("Chatbot says:")[-1].strip()

def get_answer(user_input):
    query_embedding = model.encode([user_input])
    _, I = index.search(np.array(query_embedding), k=1)

    best_match = data[I[0][0]]
    answer = best_match['answer']

    # Return the direct answer from pfp_data.json
    return answer
