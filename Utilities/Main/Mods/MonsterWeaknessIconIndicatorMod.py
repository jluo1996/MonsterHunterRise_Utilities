from pathlib import Path
from Main.Mods.ModModel import ModModel 

class MonsterWeaknessIconIndicatorMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Monster Weakness Icon Indicator"
        self.description = "Adds an icon to the monster's picture that indicates the monster's weakness."
        self.mod_file_path = Path(self.resource_folder) / "Monster Weakness Icon Indicator"