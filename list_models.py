"""
This script lists available generative AI models using the Google Gemini API.

It retrieves the API key from the ConfigManager and connects to the Gemini client
to fetch and display the names and display names of the available models.
"""
import os
from google import genai
from src.config import ConfigManager

# load_dotenv() # Removed
config = ConfigManager()
api_key = config.get_api_key()

if not api_key:
    print("No API Key found in config.json. Run main.py first to setup.")
else:
    """
    Main execution block to fetch and display available generative AI models.

    It initializes the ConfigManager, retrieves the API key, and if available,
    connects to the Gemini client to list models.
    Handles cases where the API key is missing or an error occurs during fetching.
    """
    client = genai.Client(api_key=api_key)
    try:
        print("Fetching models...")
        for m in client.models.list():
            # Debugging: print first model dir
            # print(dir(m))
            # Just print name for now to see if it works
            print(f"- {m.name} ({m.display_name})")
    except Exception as e:
        print(f"Error: {e}")
