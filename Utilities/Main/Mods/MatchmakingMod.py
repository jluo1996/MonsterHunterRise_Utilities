from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class MatchmakingMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Matchmaking"
        self.description = "Disables timeout when searching for Join Requests. Disables Region Lock for Join Requests and Lobbies. Fixes Language Filter for Lobbies."
        self.mod_file_path = Path(self.resource_folder) / "Better Matchmaking"
        self.update_install_path(game_install_path)

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")