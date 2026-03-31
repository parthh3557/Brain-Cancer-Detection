import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
import json
data = response.json()
if 'models' in data:
    for model in data['models']:
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            print(model['name'])
else:
    print(data)
