import os
from google import genai
from src.config import ConfigManager

# load_dotenv() # Removed
config = ConfigManager()
api_key = config.get_api_key()

if not api_key:
    print("No API Key found in config.json. Run main.py first to setup.")
else:
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
