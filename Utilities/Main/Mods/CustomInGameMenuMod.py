from pathlib import Path
from Main.Mods.REFrameWorkDependentMod import REFrameWorkDependentMod

class CustomInGameMenuMod(REFrameWorkDependentMod):
    def __init__(self, resource_folder, game_install_path, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Custom In-Game Mod Menu"
        self.description = "A user-friendly IMGUI inspired API for drawing in-game settings menus for REF mods in MHRise."
        self.mod_file_path = Path(self.resource_folder) / "Custom In Game Mod Menu"

    def update_install_path(self, new_game_install_path):
        super().update_install_path(Path(new_game_install_path) / "reframework" / "autorun")