from pathlib import Path
from Main.Mods.ModModel import ModModel

class REFrameworkMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper, logger):
        super().__init__(
            resource_folder=resource_folder,
            game_install_path=game_install_path,
            state_file_helper=state_file_helper,
            logger=logger
        )
        self.name = "REFramework"
        self.description = "Modding tool/framework with a powerful scripting API using Lua. Comes with fixes for DLLs/ReShade crashing, FreeCam, Timescale, FOV, VR, and tools for script/mod developers"
        self.mod_file_path = Path(self.resource_folder) / "REFramework"