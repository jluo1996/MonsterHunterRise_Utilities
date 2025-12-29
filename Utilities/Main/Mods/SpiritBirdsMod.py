from pathlib import Path
from Main.Mods.ModModel import ModModel

class SpiritBirdsMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Spirit Birds"
        self.description = "Adds spirit birds to the game for a more immersive experience."
        self.mod_file_path = Path(self.resource_folder) / "Spirit Birds v1.8"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        self.install_path = Path(new_game_install_path) / "reframework" / "autorun"
