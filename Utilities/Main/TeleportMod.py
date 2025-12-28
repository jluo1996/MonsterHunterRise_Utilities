import os
from pathlib import Path
import shutil
from ModModel import ModModel
from REFrameworkMod import REFrameworkMod
from REFrameworkD2DMod import REFrameworkD2DMod

class TeleportMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Teleport"
        self.description = "A mod that allows teleporting to different monsters."
        self.mod_file_path = Path(self.resource_folder) / "Teleport"
        self.install_path = Path(game_install_path) / "reframework" / "autorun"