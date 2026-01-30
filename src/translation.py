import json
import os
from typing import Dict, Optional

class TranslationManager:
    def __init__(self, language: str = "it"):
        self.language = language
        self.translations: Dict[str, str] = {}
        self.locales_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
        self.load_translations(language)

    def load_translations(self, language: str):
        """Loads translations for the specified language."""
        self.language = language
        file_path = os.path.join(self.locales_path, f"{language}.json")
        
        if not os.path.exists(file_path):
            # Fallback to IT if file doesn't exist, or just empty if nothing found
            print(f"Warning: Locale file not found for {language}, trying 'it'")
            file_path = os.path.join(self.locales_path, "it.json")
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            self.translations = {}

    def get(self, key: str, **kwargs) -> str:
        """Retrieves a translated string and formats it with kwargs."""
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text
