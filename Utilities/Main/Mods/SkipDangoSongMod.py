from pathlib import Path

from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class SkipDangoSongMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper, logger):
        super().__init__(resource_folder, game_install_path, state_file_helper, logger)
        self.name = "Skip Dango Song"
        self.description = "This makes all the eating and motley mix cutscenes end almost instantly."
        self.mod_file_path = Path(self.resource_folder) / "Skip Dango Song"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")