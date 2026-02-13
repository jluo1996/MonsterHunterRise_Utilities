from pathlib import Path
import re
from Main.Mods.ModModel import ModModel
from Main.Mods.ModSetting import ModSetting 

TELEPORT_GESTURE_SETTING = "Teleport Gesture"

class TeleportMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Teleport"
        self.description = "A mod that allows teleporting to different monsters."
        self.mod_file_path = Path(self.resource_folder) / "Teleport"
        self.update_install_path(game_install_path)
        self.INSTALL_FILE_NAME = "Teleport_to_target.lua"
        self.settings = self._get_settings()
        
    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")
    
    def _get_default_gesture(self, gestures):
        return "Greetings" if "Greetings" in gestures.keys() else next(iter(gestures.keys()), None)
    
    def _get_current_gesture(self):
        if self.is_installed():
            current_gesture_id = self._get_gesture_id_from_file(str(self.install_path / self.INSTALL_FILE_NAME))
            return self._get_gesture_name_by_id(current_gesture_id, self.gestures) if current_gesture_id is not None else None
        return self._get_default_gesture(self.gestures)

    
    def _get_gesture_id_from_file(self, path: str) -> int | None:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(r"curNodeID\s*==\s*(\d+)", line)
                if match:
                    return int(match.group(1))
        return None

    def install(self):
        super().install()
        self.settings = self._get_settings()  # Load settings after installation

    def uninstall(self):
        super().uninstall()

        if not self.is_installed():
            # restore default gesture in case user changed it
            default_gesture = self._get_default_gesture(self.gestures)
            if default_gesture:
                self._update_teleport_gesture_in_file(self.mod_file_path / self.INSTALL_FILE_NAME, default_gesture)
                if self.is_installed():
                    self._update_teleport_gesture_in_file(self.install_path / self.INSTALL_FILE_NAME, default_gesture)

    def _get_settings(self):
        settings = []
        self.gestures = self._load_gestures_file(str(Path(self.resource_folder) / "GestureLUT.data"))
        settings.append(ModSetting(
            name=TELEPORT_GESTURE_SETTING,
            setting_type=dict,
            value=self.gestures,
            description="The gestures used to teleport.",
            current_value=self._get_current_gesture()
        ))
        return settings 
    
    def _get_gesture_id_by_name(self, name: str, gestures_dict: dict[str, int]) -> int:
        return gestures_dict.get(name)
    
    def _get_gesture_name_by_id(self, id: int, gestures_dict: dict[str, int]) -> str | None:
        for name, num in gestures_dict.items():
            if num == id:
                return name
        return None
    
    def _load_gestures_file(self, path: str) -> dict[str, int]:
        gestures = {}

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip empty lines

                if "," not in line:
                    continue  # skip malformed lines (optional)

                name, num = line.split(",", 1)  # split only on first comma
                name = name.strip()
                num = num.strip()

                try:
                    gestures[name] = int(num)
                except ValueError:
                    # If the number isn't valid, skip or handle as needed
                    continue

        return gestures
    
    def _update_teleport_gesture_in_file(self, file_path: Path | str, gesture_name: str):
        gesture_id = self._get_gesture_id_by_name(gesture_name, self.gestures)
        if gesture_id is None:
            self._log(f"Gesture '{gesture_name}' not found in gestures list.", level="ERROR")
            return False
        
        if not file_path.exists():
            self._log(f"Install file not found at {file_path}", level="ERROR")
            return False
        
        old_gesture_id = self._get_gesture_id_from_file(str(file_path))
        if old_gesture_id is None:
            self._log(f"Current gesture ID not found in file {file_path}", level="ERROR")
            return False
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content.replace(str(old_gesture_id), str(gesture_id))
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True
    
    def save_settings(self):
        for setting in self.settings:
            if setting.name == TELEPORT_GESTURE_SETTING:
                selected_gesture_name = setting.current_value
                current_gesture_name = self._get_current_gesture()
                if selected_gesture_name != current_gesture_name:
                    if self._update_teleport_gesture_in_file(self.mod_file_path / self.INSTALL_FILE_NAME, selected_gesture_name):
                        self._log(f"Updated teleport gesture to '{selected_gesture_name}' in file {self.mod_file_path / self.INSTALL_FILE_NAME}.")
                    else:
                        self._log(f"Failed to update teleport gesture in file {self.mod_file_path / self.INSTALL_FILE_NAME}.", level="ERROR")

                if self.is_installed():
                    if self._update_teleport_gesture_in_file(self.install_path / self.INSTALL_FILE_NAME, selected_gesture_name):
                        self._log(f"Updated teleport gesture to '{selected_gesture_name}' in installed file {self.install_path / self.INSTALL_FILE_NAME}.")
                    else:
                        self._log(f"Failed to update teleport gesture in installed file {self.install_path / self.INSTALL_FILE_NAME}.", level="ERROR")
                    