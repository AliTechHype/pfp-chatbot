# chatbot.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import os
import re

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

# def get_answer(user_input):
#     query_embedding = model.encode([user_input])
#     _, I = index.search(np.array(query_embedding), k=1)
#
#     best_match = data[I[0][0]]
#     answer = best_match['answer']
#
#     # Return the direct answer from pfp_data.json
#     return answer

def normalize_input(text):
    text = text.lower()
    text = re.sub(r'\b(pfp|pakistanfoodportal|pakistan food portal)\b', 'pakistan food portal', text)
    return text.strip()

def is_food_related(text):
    food_keywords = [
        "recipe", "cook", "make", "prepare", "ingredients",
        "dish", "how to cook", "how to make", "karahi", "biryani", "tikka", "curry"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in food_keywords)

def is_restaurant_related(text):
    restaurant_keywords = [
        "restaurant", "restaurants", "place to eat", "eatery", "where is", "about", "location of",
        "menu", "nearby restaurant", "recommend"
        # Popular areas/locations
        "dha", "dha raya", "gulberg", "mm alam", "f-7", "f-10", "clifton", "bahadurabad",
        "north nazimabad", "blue area", "bahria", "zamzama", "liberty", "model town"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in restaurant_keywords)

def extract_restaurant_name(text):
    match = re.search(r'about (.*)', text.lower())
    if match:
        return match.group(1).strip()
    match = re.search(r'where is (.*)', text.lower())
    if match:
        return match.group(1).strip()
    match = re.search(r'what do you know about (.*)', text.lower())
    if match:
        return match.group(1).strip()
    return None

def get_answer(user_input, threshold=0.45):
    normalized_input = normalize_input(user_input)
    query_embedding = model.encode([normalized_input])
    D, I = index.search(np.array(query_embedding), k=1)  # Get top 3 matches

    best_distance = D[0][0]
    best_match = data[I[0][0]]
    answer = best_match['answer']

    # Convert L2 distance to similarity (lower is better)
    if best_distance > threshold:
        # Check if it's food-related
        if is_food_related(user_input):
            # Optionally, extract the dish name
            fallback = (
                "I don't have the exact recipe, but you can explore recipes here: "
                "https://pakistanfoodportal.com/recipes"
            )
            return fallback
        if is_restaurant_related(user_input):
            restaurant_name = extract_restaurant_name(user_input)
            if restaurant_name:
                return (
                    f"You can find details about {restaurant_name.title()} here: "
                    f"https://pakistanfoodportal.com/search?name={restaurant_name}"
                )
            return (
                "You can explore restaurants here: https://pakistanfoodportal.com/restaurants"
            )

        return "Sorry, I’m not sure how to help with that. Try asking something about Pakistani food, recipes, or restaurants."

    return answer