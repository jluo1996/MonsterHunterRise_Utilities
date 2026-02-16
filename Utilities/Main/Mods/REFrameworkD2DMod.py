from pathlib import Path
from Main.Mods.ModModel import ModModel

class REFrameworkD2DMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "REFramework Direct2D"
        self.description = "REFramework Direct2D is an extension for REFramework that enables Direct2D rendering."
        self.mod_file_path = Path(self.resource_folder) / "REFramework Direct2D" 

