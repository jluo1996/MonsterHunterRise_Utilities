from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class SkipIntroLogoMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper, logger):
        super().__init__(resource_folder, game_install_path, state_file_helper, logger)
        self.name = "Skip Intro Logo"
        self.description = "Skip logos and press any button."
        self.mod_file_path = Path(self.resource_folder) / "Skip Intro Logo"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")