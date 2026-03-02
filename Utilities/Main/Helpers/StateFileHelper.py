import json
import os

from Main.Helpers.FileHelper import FileHelper

class StateFileHelper:
    def __init__(self, file_helper: FileHelper):
        self.file_helper = file_helper
        self.state_file_path = self.file_helper.get_install_state_file_path()
        self._state = self._load_state()
        pass

    def set_state(self, mod_name: str, key: str, value):
        if mod_name not in self._state:
            self._state[mod_name] = {}
        self._state[mod_name][key] = value
        self._save_state()

    def get_state(self, mod_name: str, key: str, default=None):
        return self._state.get(mod_name, {}).get(key, default)

    def remove_mod_state(self, mod_name: str):
        if mod_name in self._state:
            del self._state[mod_name]
            self._save_state()

    def _load_state(self):
        with open(self.state_file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
            
    def _save_state(self):
        temp_file = self.state_file_path.with_suffix(".tmp")

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=4)

        # Atomic replace (safe against crash)
        os.replace(temp_file, self.state_file_path)