import os
from pathlib import Path
import shutil
from ModModel import ModModel

class REFrameworkMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(
            resource_folder=resource_folder,
            game_install_path=game_install_path
        )
        self.name = "REFramework"
        self.description = "REFramework is a modding framework for RE Engine games."
        self.REFramework_file_path = Path(self.resource_folder) / "REFramework" / "dinput8.dll"

    def install(self):
        if self.is_installed():
            print("REFramework is already installed.")
            return False
        
        if not self.REFramework_file_path.exists():
            print(f"REFramework file {self.REFramework_file_path} not found.")
            return False

        if not self.install_path.exists():
            print(f"Game install path {self.game_install_path} does not exist.")
            return False

        shutil.copy(self.REFramework_file_path, self.game_install_path)

        return self.is_installed()
    
    def uninstall(self):
        target_file = Path(self.game_install_path) / "dinput8.dll"
        if self.install_path.exists() and self.is_installed():
            os.remove(target_file)
        else:
            print("REFramework is not installed.")
            return False
        
        return not self.is_installed()
    
    def is_installed(self):
        target_file = Path(self.game_install_path) / "dinput8.dll"
        return target_file.exists()