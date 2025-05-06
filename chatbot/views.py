# from django.shortcuts import render
# from django.http import JsonResponse
# import json
# import google.generativeai as genai
#
# # Configure API key
# genai.configure(api_key="AIzaSyCSg_rCntFkzagtsgfyQvK8wjNXTnE7-gI")
#
# def chat_view(request):
#     return render(request, 'chatbot/chat.html')
#
# def is_relevant(message):
#     greetings = ['hello', 'hi', 'hey', 'how are you', 'good morning', 'good evening', '???']
#     words = ['pakistan food', 'recipe', 'cuisine', 'dish', 'restaurant', 'ingredient',
#                     'food portal', 'pakistanfoodportal', 'pfp', 'what to eat', 'privacy policy', '??']
#     keywords = greetings + words
#     return any(keyword.lower() in message.lower() for keyword in keywords)
#
# def chat_api(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message', '')
#             print("user input: ", user_message)
#
#
#
#             if not is_relevant(user_message):
#                 return JsonResponse({'response': 'Sorry, I can only answer questions about Pakistan Food Portal.'})
#
            # model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=(
            #     "You are a helpful assistant for Pakistan Food Portal (https://pakistanfoodportal.com), a site about Pakistani cuisine, "
            #     "including restaurant listings, food recipes, and a 'What to Eat' feature. You can also help users search for food-related queries.\n\n"
            #
            #     "You should respond politely to greetings (e.g., 'hi', 'hello') and small talk (e.g., 'how are you?'), but for questions outside the site’s purpose, "
            #     "respond with: 'Sorry, I can only help with questions related to Pakistan Food Portal.'\n\n"
            #
            #     "If the user asks about restaurants in general, give a brief description (e.g., 'You can explore a variety of Pakistani restaurants based on cities, cuisines, or ratings.') "
            #     "and then provide the link: https://pakistanfoodportal.com/restaurants.\n\n"
            #
            #     "If the user asks about recipes, describe what they can expect (e.g., 'You’ll find a wide variety of Pakistani dishes like Biryani, Karahi, and more with step-by-step instructions.') "
            #     "and provide the link: https://pakistanfoodportal.com/recipes.\n\n"
            #
            #     "If the user asks about a specific restaurant, first create a slug by converting the name to lowercase and replacing spaces with hyphens "
            #     "(e.g., 'Karachi Spice Biryani' → 'karachi-spice-biryani') and then give a friendly message before sharing the link like: "
            #     "'Here’s the page for Karachi Spice Biryani: https://pakistanfoodportal.com/restaurant/karachi-spice-biryani.'\n\n"
            #
            #     "If the user wants to find something or has a custom query, invite them to search and provide the link like: "
            #     "'You can search for it here: https://pakistanfoodportal.com/search?name=chicken-karahi' "
            #     "(replace spaces with hyphens in the search term).\n\n"
            #
            #     "Always keep answers helpful, friendly, and related to Pakistan Food Portal. Avoid short, robotic replies—offer a helpful sentence before sharing links."
            # ))
            #
            # response = model.generate_content(
            #     f"You are a chatbot for Pakistan Food Portal (https://pakistanfoodportal.com). Answer this question only if it's related to the portal: {user_message}"
            # )
            #
            # bot_response = response.text.strip()
#             print("bot response: ", bot_response)
#             return JsonResponse({'response': bot_response})
#         except Exception as e:
#             print(e)
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.shortcuts import render
from django.http import JsonResponse

import json

from .chatbot import get_answer
def chat_view(request):
    return render(request, 'chatbot/chat.html')
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message.strip():
                return JsonResponse({'response': 'Please ask something related to Pakistan Food Portal.'})

            response_text = get_answer(user_message)

            if not response_text or response_text == "":
                response_text = "❌ Sorry, I can only help with food-related questions from Pakistan Food Portal (PFP). Try asking about recipes or restaurants!"

            return JsonResponse({'response': response_text})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)