import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "Hello"}]}],
    "systemInstruction": {"parts": [{"text": "You are a bot"}]}
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.text)
