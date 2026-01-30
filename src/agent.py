from google import genai
from google.genai import types
from typing import List, Dict
import os

from src.translation import TranslationManager

class PromptConsultant:
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash", debug: bool = False, translation_manager: TranslationManager = None):
        if not api_key:
            raise ValueError("API Key is required to initialize PromptConsultant.")
        
        self.api_key = api_key
        # Default to Italian if no TM provided
        self.translation_manager = translation_manager if translation_manager else TranslationManager("it")
        self.model_name = model_name
        self.debug = debug
        self.client = genai.Client(api_key=self.api_key)
        
        self.start_new_session()

    def start_new_session(self):
        """Resets the session with the current configuration and system prompt."""
        # Load System Prompt from TranslationManager
        self.system_prompt = self.translation_manager.get("system_prompt")
        self._initialize_model()

    def _initialize_model(self):
        try:
            if self.debug:
                print(f"[DEBUG] Initializing model: {self.model_name}")

            self.chat_session = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7,
                )
            )
        except Exception as e:
            print(f"Error initializing model: {e}")

    def update_model(self, new_model_name: str):
        """Updates the model and re-initializes the chat session."""
        self.model_name = new_model_name
        if self.debug:
            print(f"[DEBUG] Switching to model: {self.model_name}")
        self.start_new_session()

    def start_consultation(self, initial_text: str) -> str:
        """Starts the consultation with the user's initial idea."""
        # We define a priming message to ensure the model knows to start the interview
        user_message = f"Ecco la mia idea iniziale per un prompt che voglio scrivere: '{initial_text}'. Per favore analizzala e inizia la consulenza."
        return self.chat(user_message)

    def chat(self, user_text: str) -> str:
        """Sends a message to the agent and gets a response."""
        try:
            response = self.chat_session.send_message(user_text)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"
