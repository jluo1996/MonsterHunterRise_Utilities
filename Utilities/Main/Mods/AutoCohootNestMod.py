from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class AutoCohootNestMod(REFrameWorkDependentMod):
    def __init__(self, resources_path, game_install_path, state_file_helper):
        super().__init__(resources_path, game_install_path, state_file_helper)
        self.name = "Auto Cohoot Nest"
        self.description = "Auto harvest cohoot nest when it's max."
        self.mod_file_path = Path(self.resource_folder) / "Auto Cohoot Nest"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")