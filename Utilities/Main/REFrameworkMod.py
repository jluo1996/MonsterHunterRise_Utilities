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
        self.mod_file_path = Path(self.resource_folder) / "REFramework"