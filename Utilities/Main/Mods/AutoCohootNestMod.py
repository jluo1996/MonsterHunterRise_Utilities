from pathlib import Path
from Main.Mods.ModModel import ModModel

class AutoCohootNestMod(ModModel):
    def __init__(self, resources_path, game_install_path):
        super().__init__(resources_path, game_install_path)
        self.name = "Auto Cohoot Nest"
        self.description = "Automatically collects items from Cohoot nests."
        self.mod_file_path = Path(self.resource_folder) / "Auto Cohoot Nest"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")