from pathlib import Path
from ModModel import ModModel
from REFrameworkMod import REFrameworkMod

GAME_INSTALL_PATH = r"D:\\Output\\"

class MainViewModel():
    def __init__(self):
        self.mods = []  # This will hold a list of ModModel instances
        self.resources_path = Path(__file__).resolve().parent.parent / "Resources/"
        print(f"Resources path set to: {self.resources_path}")

    def get_mods(self):
        return self.mods
    
    def init_mods(self):
        self.mods.append(REFrameworkMod(self.resources_path, GAME_INSTALL_PATH))

    def install_selected_mods(self):
        for mod in self.mods:
            if mod.is_selected:
                mod.install()

    def uninstall_selected_mods(self):
        for mod in self.mods:
            if mod.is_selected:
                mod.uninstall()

    