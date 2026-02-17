from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class FastReturnMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Fast Return"
        self.description = "Skip carve timer and quest ending animation."
        self.mod_file_path = Path(self.resource_folder) / "Fast Return"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework")