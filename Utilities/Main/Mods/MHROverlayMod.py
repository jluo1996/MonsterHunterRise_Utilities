from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class MHROverlayMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper, logger):
        super().__init__(resource_folder, game_install_path, state_file_helper, logger)
        self.name = "MHR Overlay"
        self.description = "Overlay mod that exposes in-game data about monsters, creatures, players and damage."
        self.mod_file_path = Path(self.resource_folder) / "MHR Overlay v2.7.3"