# # chatbot.py
#
# import json
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from transformers import pipeline
# import os
# import re
#
# # unanswered file
# UNANSWERED_FILE = os.path.join(os.path.dirname(__file__), "unanswered_questions.json")
#
# # Load components
# model = SentenceTransformer('all-MiniLM-L6-v2')
# index_path = os.path.join(os.path.dirname(__file__), "pfp_index.faiss")
# print("file path: ",os.path.join(os.path.dirname(__file__), "pfp_index.faiss"))
# index = faiss.read_index(index_path)
#
# pfp_data_file_path = os.path.join(os.path.dirname(__file__), "pfp_data.json")
# with open(pfp_data_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
#     # Optional: Use huggingface for text generation
# generator = pipeline("text-generation", model="distilgpt2")
#
# # def get_answer(user_input):
# #     query_embedding = model.encode([user_input])
# #     _, I = index.search(np.array(query_embedding), k=1)
# #
# #     best_match = data[I[0][0]]
# #     question, answer = best_match['question'], best_match['answer']
# #
# #     # Optional: make response more conversational
# #     prompt = f"User asked: {user_input}\nBased on: {answer}\nChatbot says:"
# #     generated = generator(prompt, max_length=80, do_sample=True)[0]['generated_text']
# #
# #     return generated.split("Chatbot says:")[-1].strip()
#
# # def get_answer(user_input):
# #     query_embedding = model.encode([user_input])
# #     _, I = index.search(np.array(query_embedding), k=1)
# #
# #     best_match = data[I[0][0]]
# #     answer = best_match['answer']
# #
# #     # Return the direct answer from pfp_data.json
# #     return answer
#
# def save_unanswered_question(question):
#     if not (is_food_related(question) or is_restaurant_related(question)):
#         return  # skip out-of-scope
#
#     try:
#         if os.path.exists(UNANSWERED_FILE):
#             with open(UNANSWERED_FILE, 'r', encoding='utf-8') as f:
#                 unanswered = json.load(f)
#         else:
#             unanswered = []
#
#         # Avoid duplicates
#         if question not in [q['question'] for q in unanswered]:
#             unanswered.append({'question': question})
#             with open(UNANSWERED_FILE, 'w', encoding='utf-8') as f:
#                 json.dump(unanswered, f, ensure_ascii=False, indent=2)
#     except Exception as e:
#         print("Error saving unanswered question:", e)
#
#
# def train_unanswered_questions():
#     if not os.path.exists(UNANSWERED_FILE):
#         print("No unanswered questions.")
#         return
#
#     with open(UNANSWERED_FILE, 'r', encoding='utf-8') as f:
#         unanswered = json.load(f)
#
#     if not unanswered:
#         print("No new questions to process.")
#         return
#
#     with open(pfp_data_file_path, 'r', encoding='utf-8') as f:
#         existing_data = json.load(f)
#
#     new_data = []
#     for item in unanswered:
#         q = item['question']
#         prompt = f"Question: {q}\nAnswer about Pakistan Food Portal:"
#         response = generator(prompt, max_length=80, do_sample=True)[0]['generated_text']
#         answer = response.split("Answer about Pakistan Food Portal:")[-1].strip()
#
#         if not answer:
#             answer = "This is a food-related question, but I currently don't have a detailed answer."
#
#         new_data.append({
#             "question": q,
#             "answer": answer
#         })
#
#     # Add to existing
#     existing_data.extend(new_data)
#
#     with open(pfp_data_file_path, 'w', encoding='utf-8') as f:
#         json.dump(existing_data, f, ensure_ascii=False, indent=2)
#
#     # Clear unanswered file
#     with open(UNANSWERED_FILE, 'w', encoding='utf-8') as f:
#         json.dump([], f)
#
#     print(f"Trained and added {len(new_data)} new entries.")
#
# def normalize_input(text):
#     text = text.lower()
#     text = re.sub(r'\b(pfp|pakistanfoodportal|pakistan food portal)\b', 'pakistan food portal', text)
#     return text.strip()
#
# def is_food_related(text):
#     food_keywords = [
#         "recipe", "cook", "make", "prepare", "ingredients",
#         "dish", "how to cook", "how to make", "karahi", "biryani", "tikka", "curry"
#     ]
#     text_lower = text.lower()
#     return any(keyword in text_lower for keyword in food_keywords)
#
# def is_restaurant_related(text):
#     restaurant_keywords = [
#         "kfc", "daily deli co", "brim", "mcdonalds", "melt", "karachi silver spoon", "cheezious", "eggspectation restaurant cafe", "nandos", "chashni", "novu", "tim hortons", "hardees",
#         "restaurant", "restaurants", "place to eat", "eatery", "where is", "about", "location of",
#         "menu", "nearby restaurant", "recommend",
#         # Popular areas/locations
#         "dha", "dha raya", "gulberg", "mm alam", "f-7", "f-10", "clifton", "bahadurabad",
#         "north nazimabad", "blue area", "bahria", "zamzama", "liberty", "model town"
#     ]
#     text_lower = text.lower()
#     return any(keyword in text_lower for keyword in restaurant_keywords)
#
# def is_discount_query(text):
#     discount_keywords = ["discount", "offer", "offers", "deal", "promotion", "promo"]
#     bank_names = [
#         "hbl", "ubl", "meezan", "al baraka", "bank alfalah", "habib bank", "standard chartered",
#         "faysal bank", "askari", "js bank", "mcb", "nbp", "samba", "summit", "dubai islamic"
#     ]
#     cards = ["visa", "mastercard", "unionpay", "paypak"]
#
#     text = text.lower()
#     for bank in bank_names:
#         if bank in text:
#             return f"Yes! You can view discounts for {bank.title()} and other banks here: https://pakistanfoodportal.com/discounts-and-offers"
#
#     for card in cards:
#         if card in text:
#             return f"You can filter discounts using your {card.title()} card here: https://pakistanfoodportal.com/discounts-and-offers"
#
#     for keyword in discount_keywords:
#         if keyword in text:
#             return "Explore all available restaurant discounts by banks and card types here: https://pakistanfoodportal.com/discounts-and-offers"
#
#     return None
#
#
# def extract_restaurant_name(text):
#     match = re.search(r'about (.*)', text.lower())
#     if match:
#         return match.group(1).strip()
#     match = re.search(r'where is (.*)', text.lower())
#     if match:
#         return match.group(1).strip()
#     match = re.search(r'what do you know about (.*)', text.lower())
#     if match:
#         return match.group(1).strip()
#     match = re.search(r'(.*) restaurant', text.lower())
#     if match:
#         return match.group(1).strip()
#     return None
#
# def get_answer(user_input, threshold=0.45):
#     normalized_input = normalize_input(user_input.strip())
#     query_embedding = model.encode([normalized_input])
#     D, I = index.search(np.array(query_embedding), k=5)  # Get top 3 matches
#
#     best_distance = D[0][0]
#     best_match = data[I[0][0]]
#     answer = best_match['answer']
#
#     # Convert L2 distance to similarity (lower is better)
#     if best_distance > threshold:
#         # Check if it's food-related
#         if is_food_related(user_input):
#             # Optionally, extract the dish name
#             fallback = (
#                 "I don't have the exact recipe, but you can explore recipes here: \n"
#                 "https://pakistanfoodportal.com/recipes"
#             )
#             return fallback
#         if is_restaurant_related(user_input):
#             restaurant_name = extract_restaurant_name(user_input)
#             if restaurant_name:
#                 return (
#                     f"You can find details about {restaurant_name.title()} here: \n"
#                     f"https://pakistanfoodportal.com/search?name={restaurant_name}"
#                 )
#             return (
#                 "You can explore restaurants here: https://pakistanfoodportal.com/restaurants"
#             )
#
#         discount_response = is_discount_query(normalized_input)
#         if discount_response:
#             return discount_response
#
#         save_unanswered_question(user_input)
#         return "Sorry, I’m not sure how to help with that. Try asking something about Pakistani food, recipes, or restaurants."
#
#     return answer











# New File Code
# chatbot.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import re

# File paths
BASE_DIR = os.path.dirname(__file__)
UNANSWERED_FILE = os.path.join(BASE_DIR, "unanswered_questions.json")
INDEX_PATH = os.path.join(BASE_DIR, "pfp_index.faiss")
PFP_DATA_FILE = os.path.join(BASE_DIR, "pfp_data.json")

# Load Sentence Transformer model and FAISS index
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Loading FAISS index from:", INDEX_PATH)
index = faiss.read_index(INDEX_PATH)

# Load data
with open(PFP_DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)


def normalize_input(text):
    text = text.lower().strip()
    text = re.sub(r'\b(pfp|pakistanfoodportal|pakistan food portal)\b', 'pakistan food portal', text)
    return text


def is_food_related(text):
    food_keywords = [
        "recipe", "cook", "make", "prepare", "ingredients",
        "dish", "how to cook", "how to make", "karahi", "biryani", "tikka", "curry"
    ]
    text = text.lower()
    return any(keyword in text for keyword in food_keywords)


def is_restaurant_related(text):
    restaurant_keywords = [
        "kfc", "daily deli co", "brim", "mcdonalds", "melt", "karachi silver spoon",
        "cheezious", "eggspectation restaurant cafe", "nandos", "chashni", "novu",
        "tim hortons", "hardees", "restaurant", "restaurants", "place to eat", "eatery",
        "where is", "about", "location of", "menu", "nearby restaurant", "recommend",
        "dha", "dha raya", "gulberg", "mm alam", "f-7", "f-10", "clifton", "bahadurabad",
        "north nazimabad", "blue area", "bahria", "zamzama", "liberty", "model town"
    ]
    text = text.lower()
    return any(keyword in text for keyword in restaurant_keywords)


def is_discount_query(text):
    discount_keywords = ["discount", "offer", "offers", "deal", "promotion", "promo"]
    bank_names = [
        "hbl", "ubl", "meezan", "al baraka", "bank alfalah", "habib bank", "standard chartered",
        "faysal bank", "askari", "js bank", "mcb", "nbp", "samba", "summit", "dubai islamic"
    ]
    cards = ["visa", "mastercard", "unionpay", "paypak"]

    text = text.lower()
    for bank in bank_names:
        if bank in text:
            return f"Yes! You can view discounts for {bank.title()} and other banks here: https://pakistanfoodportal.com/discounts-and-offers"
    for card in cards:
        if card in text:
            return f"You can filter discounts using your {card.title()} card here: https://pakistanfoodportal.com/discounts-and-offers"
    for keyword in discount_keywords:
        if keyword in text:
            return "Explore all available restaurant discounts by banks and card types here: https://pakistanfoodportal.com/discounts-and-offers"
    return None


def extract_restaurant_name(text):
    patterns = [
        r'about (.*)',
        r'where is (.*)',
        r'what do you know about (.*)',
        r'(.*) restaurant'
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return match.group(1).strip()
    return None


def save_unanswered_question(question):

    try:
        if os.path.exists(UNANSWERED_FILE):
            with open(UNANSWERED_FILE, 'r', encoding='utf-8') as f:
                unanswered = json.load(f)
        else:
            unanswered = []

        if question not in [q['question'] for q in unanswered]:
            unanswered.append({'question': question})
            with open(UNANSWERED_FILE, 'w', encoding='utf-8') as f:
                json.dump(unanswered, f, ensure_ascii=False, indent=2)
            print(f"Saved unanswered question: {question}")
    except Exception as e:
        print("Error saving unanswered question:", e)


def train_unanswered_questions():
    from transformers import pipeline  # Import only when needed
    generator = pipeline("text-generation", model="distilgpt2")

    if not os.path.exists(UNANSWERED_FILE):
        print("No unanswered questions.")
        return

    with open(UNANSWERED_FILE, 'r', encoding='utf-8') as f:
        unanswered = json.load(f)

    if not unanswered:
        print("No new questions to process.")
        return

    with open(PFP_DATA_FILE, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    new_data = []
    for item in unanswered:
        q = item['question']
        prompt = f"Question: {q}\nAnswer about Pakistan Food Portal:"
        response = generator(prompt, max_length=80, do_sample=True)[0]['generated_text']
        answer = response.split("Answer about Pakistan Food Portal:")[-1].strip()

        if not answer:
            answer = "This is a food-related question, but I currently don't have a detailed answer."

        new_data.append({
            "question": q,
            "answer": answer
        })

    existing_data.extend(new_data)

    with open(PFP_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    with open(UNANSWERED_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

    print(f"Trained and added {len(new_data)} new entries.")


def get_answer(user_input, threshold=0.45):
    normalized_input = normalize_input(user_input)
    query_embedding = model.encode([normalized_input])
    D, I = index.search(np.array(query_embedding), k=5)

    best_distance = D[0][0]
    best_match = data[I[0][0]]
    answer = best_match['answer']

    if best_distance > threshold:
        if is_food_related(user_input):
            return (
                "I don't have the exact recipe, but you can explore recipes here: \n"
                "https://pakistanfoodportal.com/recipes"
            )
        if is_restaurant_related(user_input):
            restaurant_name = extract_restaurant_name(user_input)
            if restaurant_name:
                return (
                    f"You can find details about {restaurant_name.title()} here: \n"
                    f"https://pakistanfoodportal.com/search?name={restaurant_name}"
                )
            return "You can explore restaurants here: https://pakistanfoodportal.com/restaurants"

        discount_response = is_discount_query(normalized_input)
        if discount_response:
            return discount_response

        print(f"Saving unanswered: {user_input}")
        save_unanswered_question(user_input)
        return "Sorry, I’m not sure how to help with that. Try asking something about Pakistani food, recipes, or restaurants."

    return answer
