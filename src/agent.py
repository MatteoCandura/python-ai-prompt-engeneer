
"""
This module defines the PromptConsultant class, which acts as an AI agent
to assist users in crafting and refining prompts for generative AI models.

It leverages the Google Gemini API to facilitate interactive consultation sessions.
"""
from google import genai
from google.genai import types
from typing import List, Dict
import os

from src.translation import TranslationManager

class PromptConsultant:
    """
    Manages interaction with a generative AI model for prompt consultation.

    This class handles API key management, model selection, session management,
    and communication with the Google Gemini API to provide interactive
    prompt refinement assistance.
    """
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash", debug: bool = False, translation_manager: TranslationManager = None):
        """
        Initializes the PromptConsultant with necessary configurations.

        Args:
            api_key: The API key for authenticating with the Google Gemini API.
            model_name: The name of the Gemini model to use for the consultation.
            debug: If True, enables debug output for the consultant.
            translation_manager: An instance of TranslationManager for i18n support.

        Raises:
            ValueError: If the API key is not provided.
        """
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
        """
        Resets the current chat session with the generative AI model.

        This method reloads the system prompt (from the TranslationManager)
        and re-initializes the model with the current configuration,
        effectively starting a new conversation context.
        """
        # Load System Prompt from TranslationManager
        self.system_prompt = self.translation_manager.get("system_prompt")
        self._initialize_model()

    def _initialize_model(self):
        """
        Initializes or re-initializes the generative AI model chat session.

        Configures the chat session with the selected model, system instructions,
        and temperature settings. Handles potential errors during model initialization.
        """
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
        """
        Updates the generative AI model used for the consultation.

        Changes the active model and re-initializes the chat session
        to apply the new model selection.

        Args:
            new_model_name: The name of the new Gemini model to use.
        """
        self.model_name = new_model_name
        if self.debug:
            print(f"[DEBUG] Switching to model: {self.model_name}")
        self.start_new_session()

    def start_consultation(self, initial_text: str) -> str:
        """
        Initiates a new consultation session with an initial user idea.

        Sends a priming message to the AI model to guide it into
        a consultation interview mode based on the user's initial text.

        Args:
            initial_text: The user's initial idea or draft prompt.

        Returns:
            The AI's initial response to start the consultation.
        """
        # We define a priming message to ensure the model knows to start the interview
        user_message = f"Ecco la mia idea iniziale per un prompt che voglio scrivere: '{initial_text}'. Per favore analizzala e inizia la consulenza."
        return self.chat(user_message)

    def chat(self, user_text: str) -> str:
        """
        Sends a user message to the active generative AI chat session and
        retrieves the AI's response.

        Handles communication with the Gemini API for ongoing conversation turns.

        Args:
            user_text: The user's message to send to the AI.

        Returns:
            The AI's generated response as a string.
            Returns an error message if communication with Gemini fails.
        """
        try:
            response = self.chat_session.send_message(user_text)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"
