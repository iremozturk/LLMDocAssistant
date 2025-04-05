import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv('OPENAI_API_KEY')
print("API Key loaded (first 20 chars):", api_key[:20] if api_key else "None")

# API endpoint
url = "https://api.openai.com/v1/chat/completions"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request body
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello!"}
    ]
}

try:
    print("\nAttempting API call...")
    response = requests.post(url, headers=headers, json=data)
    
    # Print response status and headers
    print(f"\nStatus Code: {response.status_code}")
    print("Response Headers:", json.dumps(dict(response.headers), indent=2))
    
    if response.status_code == 200:
        print("\nAPI call successful!")
        print("Response:", json.dumps(response.json(), indent=2))
    else:
        print("\nError occurred:")
        print("Response:", response.text)
        
except Exception as e:
    print("\nError occurred:")
    print(str(e)) 