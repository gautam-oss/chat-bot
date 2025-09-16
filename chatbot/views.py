from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv   # ✅ Import dotenv

# ✅ Load variables from .env into environment
load_dotenv()

# ✅ Configure Gemini API with key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(message: str) -> str:
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'
        
        # Create the conversation with system instruction
        response = model.generate_content(
            f"You are a helpful chatbot. User message: {message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.7,
            )
        )
        
        return response.text.strip()

    except Exception as e:
        # Handle errors gracefully (quota exceeded, invalid key, etc.)
        return f"⚠️ Error: {str(e)}"

# Django view
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        response = ask_gemini(message)
        return JsonResponse({"message": message, "response": response})

    return render(request, "chatbot.html")