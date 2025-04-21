from django.shortcuts import render
from django.http import JsonResponse
import json
import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyCSg_rCntFkzagtsgfyQvK8wjNXTnE7-gI")
models = genai.list_models()
for model in models:
    print(f"{model.name} -> {model.supported_generation_methods}")

def chat_view(request):
    return render(request, 'chatbot/chat.html')

def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            print("user input: ", user_message)

            # ✅ Use a working model name
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(user_message)

            bot_response = response.text.strip()
            print("bot response: ", bot_response)
            return JsonResponse({'response': bot_response})
        except Exception as e:
            print("Exception:", e)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
