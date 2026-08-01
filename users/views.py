import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pyttsx3
import threading
import re
import base64
import cv2
import numpy as np
from langdetect import detect
import pythoncom




# Configure Gemini API
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Initialize Gemini Model

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Language code mapping (if needed)
language_code_map = {
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
    "it": "it",
    "pt": "pt",
    "ru": "ru",
    "ja": "ja",
    "ko": "ko",
    "zh-cn": "zh-cn"
}

# def play_audio_from_text(text, lang_code):
#     try:
#         engine = pyttsx3.init()  # create engine instance in each thread.
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         print(f"TTS error: {e}")


def play_audio_from_text(text, lang_code):
    try:
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS error: {e}")
    finally:
        pythoncom.CoUninitialize()

@csrf_exempt
def capture_image(request):
    if request.method == "POST" and request.FILES.get('image'):
        try:
            print(f"FILES: {request.FILES}")
            image_file = request.FILES['image']
            image_data = image_file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None or frame.size == 0:
                return JsonResponse({"error": "Failed to decode image data"}, status=400)

            # Convert to base64
            _, buffer = cv2.imencode(".jpg", frame)
            image_data_base64 = base64.b64encode(buffer).decode("utf-8")

            # Generate TTS: "Please ask your question."
            try:
                engine_local = pyttsx3.init()  # local engine instance.
                engine_local.say("Please ask your question.")
                engine_local.runAndWait()
            except Exception as tts_error:
                print(f"TTS error: {tts_error}")
                return JsonResponse({"error": f"TTS error: {tts_error}"}, status=500)

            return JsonResponse({"message": "Image captured", "image_data": image_data_base64})

        except Exception as e:
            print(f"Error in capture_image: {e}")
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request or no image provided"}, status=400)

@csrf_exempt
def ask_question(request):
    """ Handles follow-up questions to previous AI responses, similar to send_message """
    if request.method == "POST" and request.FILES.get('image'):
        user_input = request.POST.get("question", "").strip()
        if not user_input:
            user_input = ""

        try:
            image_file = request.FILES['image']
            image_data = image_file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None or frame.size == 0:
                return JsonResponse({"error": "Failed to decode image data"}, status=400)

            # Convert to base64
            _, buffer = cv2.imencode(".jpg", frame)
            image_data_base64 = base64.b64encode(buffer).decode("utf-8")

            image_parts = [
                {
                    "mime_type": "image/jpeg",  # Assuming it's JPEG
                    "data": image_data_base64
                }
            ]

            prompt = [user_input, image_parts[0]]

            response_text = model.generate_content(prompt)
            cleaned_text = response_text.text if response_text.text else "No response."
            response = re.sub(r'\*', '', cleaned_text)
            print(response)
            detected_lang = detect(response)
            language_code = language_code_map.get(detected_lang, 'en')
            threading.Thread(target=play_audio_from_text, args=(response, language_code)).start()
            return JsonResponse({"response": response}, status=200)

        except Exception as e:
            print(f"Error in ask_question: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request or no image provided"}, status=400)

def chatbot(request):
    return render(request, 'index.html')