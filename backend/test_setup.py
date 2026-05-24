from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API key loaded: {api_key[:8]}...")  # Only prints first 8 chars for safety
print("Setup complete ✓")
