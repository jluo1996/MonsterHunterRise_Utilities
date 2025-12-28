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
        self.mod_file_path = Path(self.resource_folder) / "Teleport" / "Teleport_to_target.lua"

    def install(self):
        if self.is_installed():
            print("Teleport mod is already installed.")
            return False
        
        if not self.mod_file_path.exists():
            print(f"Teleport mod file {self.mod_file_path} not found.")
            return False
        
        if not self.install_path.exists():
            print(f"Game install path {self.game_install_path} does not exist.")
            return False
        
        REFramework_mod = REFrameworkMod(self.resource_folder, self.game_install_path)
        if not REFramework_mod.is_installed():
            print("REFramework is not installed. Please install REFramework first.")
            return False
        
        REFramework_D2D_mod = REFrameworkD2DMod(self.resource_folder, self.game_install_path)
        if not REFramework_D2D_mod.is_installed():
            print("REFramework Direct2D is not installed. Please install REFramework Direct2D first.")
            return False
        
        destination = self.install_path / "reframework" / "autorun" / self.mod_file_path.name
        shutil.copy(self.mod_file_path, destination)
        
        return self.is_installed()

    def uninstall(self):
        if not self.install_path.exists() or not self.is_installed():
            print("Teleport mod is not installed.")
            return False
        
        targe_file = self.install_path / "reframework" / "autorun" / self.mod_file_path.name
        os.remove(targe_file)
        return True

    def is_installed(self):
        targe_file = self.install_path / "reframework" / "autorun" / self.mod_file_path.name
        return targe_file.is_file()