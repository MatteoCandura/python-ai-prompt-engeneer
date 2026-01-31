"""
This module provides the ConfigManager class for handling application configuration,
including API keys, selected models, and language preferences.

Configurations are stored and retrieved from a `config.json` file.
"""
import json
import os
from typing import Optional

CONFIG_FILE = "config.json"

class ConfigManager:
    """
    Manages the application's configuration settings.

    This includes loading, saving, and retrieving various configuration parameters
    such as API keys, model names, and language settings from a JSON file.
    """
    def __init__(self):
        """
        Initializes the ConfigManager by loading the configuration from `config.json`.
        """
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """
        Loads the configuration from the `config.json` file.

        If the file does not exist, an empty configuration file is created.
        Handles JSON decoding errors by returning an empty dictionary.

        Returns:
            A dictionary containing the loaded configuration.
        """
        if not os.path.exists(self.config_path):
            self._create_empty_config()
            return {}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def get_model(self) -> Optional[str]:
        """
        Retrieves the currently configured generative AI model name.

        Returns:
            The model name as a string, or None if not set.
        """
        return self.config.get("model")

    def set_model(self, model_name: str):
        """
        Sets the generative AI model name in the configuration.

        Args:
            model_name: The name of the model to set.
        """
        self.config["model"] = model_name
        self._save_config()

    def get_language(self) -> Optional[str]:
        """
        Retrieves the currently configured language preference.

        Returns:
            The language code (e.g., "en", "it") as a string, or None if not set.
        """
        return self.config.get("language")

    def set_language(self, language: str):
        """
        Sets the language preference in the configuration.

        Args:
            language: The language code (e.g., "en", "it") to set.
        """
        self.config["language"] = language
        self._save_config()

    def get_api_key(self) -> Optional[str]:
        """
        Retrieves the currently configured API key.

        Returns:
            The API key as a string, or None if not set.
        """
        return self.config.get("api_key")

    def set_api_key(self, api_key: str):
        """
        Sets the API key in the configuration.

        Args:
            api_key: The API key to set.
        """
        self.config["api_key"] = api_key
        self._save_config()

    def _save_config(self):
        """
        Saves the current configuration dictionary to the `config.json` file.
        """
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def _create_empty_config(self):
        """
        Creates an empty `config.json` file, effectively resetting the configuration.
        """
        with open(self.config_path, "w") as f:
            json.dump({}, f, indent=4)
            
    def clear_config(self):
        """
        Resets the configuration to an empty state by clearing the internal
        config dictionary and writing an empty JSON object to `config.json`.
        """
        self.config = {}
        self._create_empty_config()
