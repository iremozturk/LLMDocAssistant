import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv('OPENAI_API_KEY')
print("API Key loaded (first 20 chars):", api_key[:20] if api_key else "None")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

try:
    # Try a simple API call
    print("\nAttempting API call...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("\nAPI call successful!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("\nError occurred:")
    print(str(e))
    print("\nFull API Key length:", len(api_key) if api_key else 0) 