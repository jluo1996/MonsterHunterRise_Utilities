from pathlib import Path
from Main.Mods.REFrameworkMod import REFrameworkMod
from Main.Mods.REFrameworkD2DMod import REFrameworkD2DMod
from Main.Mods.TeleportMod import TeleportMod
from Main.Mods.SpiritBirdsMod import SpiritBirdsMod
from Main.Mods.DropRatesEnhancedMod import DropRatesEnhancedMod
from Main.Mods.MHROverlayMod import MHROverlayMod
from Main.Mods.AutoArgosyMod import AutoArgosyMod
from Main.Mods.AutoCohootNestMod import AutoCohootNestMod
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.Helpers.FileHelper import FileHelper


GAME_INSTALL_PATH = Path(__file__).resolve().parent.name

class MainViewModel():
    def __init__(self):
        self.mods = []  # This will hold a list of ModModel instances
        file_helper = FileHelper()
        self.resources_path = file_helper.get_resources_folder_path()
        _ = self.auto_detect_game_install_path(auto_detect=False, update_game_install_path=True)  

    def get_mods(self):
        return self.mods
    
    def init_mods(self):
        self.mods.append(REFrameworkMod(self.resources_path, self.game_install_path))
        self.mods.append(REFrameworkD2DMod(self.resources_path, self.game_install_path))
        self.mods.append(TeleportMod(self.resources_path, self.game_install_path))
        self.mods.append(SpiritBirdsMod(self.resources_path, self.game_install_path))
        self.mods.append(AutoArgosyMod(self.resources_path, self.game_install_path)) 
        self.mods.append(AutoCohootNestMod(self.resources_path, self.game_install_path))
        self.mods.append(MHROverlayMod(self.resources_path, self.game_install_path))
        self.mods.append(DropRatesEnhancedMod(self.resources_path, self.game_install_path))

    def install_selected_mods(self):
        for mod in self.mods:
            if mod.is_selected:
                mod.install()

    def uninstall_selected_mods(self):
        for mod in self.mods:
            if mod.is_selected:
                mod.uninstall()

    def update_game_install_path(self, new_path):
        self.game_install_path = new_path
        for mod in self.mods:
            mod.update_install_path(new_path)

    def auto_detect_game_install_path(self, auto_detect: bool = False, update_game_install_path: bool = False) -> list[Path]:
        game_info_helper = GameInfoHelper()
        detected_path = game_info_helper.get_MRH_install_path(auto_detect)
        if update_game_install_path and detected_path:
            self.update_game_install_path(str(detected_path))
        return [detected_path] if detected_path else []