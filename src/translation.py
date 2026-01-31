"""
This module provides the TranslationManager class for handling internationalization (i18n)
within the application. It loads and manages translated strings from JSON locale files.
"""
import json
import os
from typing import Dict, Optional

class TranslationManager:
    """
    Manages loading and retrieving translated strings for internationalization.

    It loads translations from specified language JSON files located in the 'locales' directory
    and provides a method to retrieve translated strings, with optional formatting.
    """
    def __init__(self, language: str = "it"):
        """
        Initializes the TranslationManager and loads translations for the specified language.

        Args:
            language: The default language to load translations for (e.g., "it", "en").
        """
        self.language = language
        self.translations: Dict[str, str] = {}
        self.locales_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales")
        self.load_translations(language)

    def load_translations(self, language: str):
        """
        Loads translations from a JSON file for the given language.

        If the specific language file is not found, it attempts to fall back to 'it.json'.
        If neither is found, the translations dictionary remains empty.

        Args:
            language: The language code (e.g., "en", "it") for which to load translations.
        """
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
        """
        Retrieves a translated string by its key and optionally formats it.

        If the key is not found in the loaded translations, the key itself is returned.
        Keyword arguments are used for string formatting.

        Args:
            key: The key of the string to retrieve.
            **kwargs: Arbitrary keyword arguments for string formatting.

        Returns:
            The translated and formatted string, or the key if not found.
        """
        text = self.translations.get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text
