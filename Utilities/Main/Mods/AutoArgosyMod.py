from pathlib import Path
from Main.Mods.ModModel import ModModel

class AutoArgosyMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Auto Argosy"
        self.description = "Automatically sails the Argosy when it's available."
        self.mod_file_path = Path(self.resource_folder) / "Auto Argosy"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        self.install_path = Path(new_game_install_path) / "reframework" / "autorun"