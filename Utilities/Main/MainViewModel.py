from pathlib import Path
from REFrameworkMod import REFrameworkMod
from REFrameworkD2DMod import REFrameworkD2DMod
from TeleportMod import TeleportMod
from SpiritBirdsMod import SpiritBirdsMod
from MHROverlayMod import MHROverlayMod
from DropRatesEnhancedMod import DropRatesEnhancedMod

GAME_INSTALL_PATH = Path(__file__).resolve().parent.name

class MainViewModel():
    def __init__(self):
        self.mods = []  # This will hold a list of ModModel instances
        self.resources_path = Path(__file__).resolve().parent.parent / "Resources"
        detected_paths = self.auto_detect_game_install_path()  
        self.game_install_path = str(detected_paths[0]) if detected_paths else str(GAME_INSTALL_PATH)

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

    def auto_detect_game_install_path(self):
        exe_name = "MonsterHunterRise.exe"

        return self._find_exe_in_named_folder(exe_name, "MonsterHunterRise")

    def _find_exe_in_named_folder(self, exe_name: str, folder_name: str):
        COMMON_DIRS = [
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            Path.home(),
        ]

        results = []
        for base in COMMON_DIRS:
            if not base.exists():
                continue
            for p in base.rglob(exe_name):
                if p.parent.name == folder_name:
                    results.append(p.parent)
        return results