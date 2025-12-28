from pathlib import Path
from REFrameworkMod import REFrameworkMod
from REFrameworkD2DMod import REFrameworkD2DMod
from TeleportMod import TeleportMod
from SpiritBirdsMod import SpiritBirdsMod
from MHROverlayMod import MHROverlayMod
from DropRatesEnhancedMod import DropRatesEnhancedMod

GAME_INSTALL_PATH = r"D:\\Output\\"

class MainViewModel():
    def __init__(self):
        self.mods = []  # This will hold a list of ModModel instances
        self.resources_path = Path(__file__).resolve().parent.parent / "Resources"
        self.game_install_path = GAME_INSTALL_PATH

    def get_mods(self):
        return self.mods
    
    def init_mods(self):
        self.mods.append(REFrameworkMod(self.resources_path, self.game_install_path))
        self.mods.append(REFrameworkD2DMod(self.resources_path, self.game_install_path))
        self.mods.append(TeleportMod(self.resources_path, self.game_install_path))
        self.mods.append(SpiritBirdsMod(self.resources_path, self.game_install_path))    
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

    