from pathlib import Path
from ModModel import ModModel

class SpiritBirdsMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Spirit Birds Mod"
        self.description = "Adds spirit birds to the game for a more immersive experience."
        self.mod_file_path = Path(self.resource_folder) / "Spirit Birds v1.8"
        self.install_path = Path(game_install_path) / "reframework" / "autorun"
