import json
import os
from typing import Optional

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG_FILE)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            self._create_empty_config()
            return {}
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def get_model(self) -> Optional[str]:
        return self.config.get("model")

    def set_model(self, model_name: str):
        self.config["model"] = model_name
        self._save_config()

    def get_language(self) -> Optional[str]:
        return self.config.get("language")

    def set_language(self, language: str):
        self.config["language"] = language
        self._save_config()

    def get_api_key(self) -> Optional[str]:
        return self.config.get("api_key")

    def set_api_key(self, api_key: str):
        self.config["api_key"] = api_key
        self._save_config()

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def _create_empty_config(self):
        with open(self.config_path, "w") as f:
            json.dump({}, f, indent=4)
            
    def clear_config(self):
        """Resets the configuration to empty."""
        self.config = {}
        self._create_empty_config()
