from pathlib import Path
from ModModel import ModModel

class DropRatesEnhancedMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "Drop Rates Enhanced"
        self.description = "Enhances drop rates in Monster Hunter Rise."
        self.mod_file_path = Path(self.resource_folder) / "Drop Rates Enhanced" / "Balanced"