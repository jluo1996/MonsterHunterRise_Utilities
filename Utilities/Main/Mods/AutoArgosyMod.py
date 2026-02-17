from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class AutoArgosyMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Auto Argosy"
        self.description = "Automatically receive argosy items and refill bargaining skills."
        self.mod_file_path = Path(self.resource_folder) / "Auto Argosy"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")