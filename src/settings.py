"""
Class file for loading and saving settings
"""

import os
import json
from typing import Dict, Any

settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')

factory_settings = {
    "showQuickOptions": True,
    "quickOptions": {
        "pad": False,
        "prefix": False,
        "endianness": "big",
        "defaultType": "unsigned"
    },
    "screenSize": {
        "width": 800,
        "height": 600
    }
}

class Settings:
    """
    Class for loading and saving settings
    """

    def __init__(self):
        self.settings_file = settings_file
        self.json_settings = {}
        self.load_settings()

    def load_settings(self):
        """
        Load settings from a JSON file
        """
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.json_settings = json.load(f)
        elif os.path.exists('default_settings.json'):
            with open('default_settings.json', 'r') as f:
                self.json_settings = json.load(f)
        else:
            self.json_settings = factory_settings

    def save_settings(self):
        """
        Save settings to a JSON file
        """
        with open(self.settings_file, 'w') as f:
            json.dump(self.json_settings, f, indent=4)

    def get_setting(self, keys: list[str]) -> Any:
        """
        Get a setting by a list of keys representing the hierarchy
        """
        setting = self.json_settings
        for key in keys:
            if isinstance(setting, str):
                break
            setting = setting.get(key, None)
            if setting is None:
                return None

        # Try to convert numeric strings to integers
        if isinstance(setting, str) and setting.isdigit():
            return int(setting)

        return setting

    def set_setting(self, keys: list[str], value: Any):
        """
        Set a setting by a list of keys representing the hierarchy
        """
        setting = self.json_settings
        for key in keys[:-1]:
            setting = setting.setdefault(key, {})
        setting[keys[-1]] = value