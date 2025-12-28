import os
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

    def install(self):
        REFramework_file_path = os.path.join(self.resource_folder, "dinput8.dll")
        if not os.path.exists(REFramework_file_path):
            print(f"REFramework file {REFramework_file_path} not found.")
            return False
        
        if not os.path.exists(self.game_install_path):
            print(f"Game install path {self.game_install_path} does not exist.")
            return False

        shutil.copy(REFramework_file_path, self.game_install_path)
        
        return not os.path.exists(os.path.join(self.game_install_path, "dinput8.dll"))
    
    def uninstall(self):
        target_file = os.path.join(self.game_install_path, "dinput8.dll")
        if os.path.exists(self.game_install_path) and os.path.exists(target_file):
            os.remove(target_file)
        else:
            print("REFramework is not installed.")
            return False
        
        return not os.path.exists(target_file)