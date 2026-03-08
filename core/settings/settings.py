# core/settings/settings.py
import os
import json

SETTINGS_FILE = "user_settings.json"

class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.paths = {}
            cls._instance.load_settings()
        return cls._instance

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.paths = data  # مستقیم جایگزین کن
            except Exception:
                self.paths = {}

    def save_settings(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.paths, f, indent=4)

    def set_path(self, module_name: str, path: str):
        self.paths[module_name] = path
        self.save_settings()

    def get_path(self, module_name: str):
        return self.paths.get(module_name)