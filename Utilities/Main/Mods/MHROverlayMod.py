from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class MHROverlayMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "MHR Overlay"
        self.description = "MHR Overlay is a mod that adds an overlay to Monster Hunter Rise."
        self.mod_file_path = Path(self.resource_folder) / "MHR Overlay v2.7.3"