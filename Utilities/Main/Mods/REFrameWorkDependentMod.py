from Main.Mods.ModModel import ModModel
from Main.Mods.REFrameworkD2DMod import REFrameworkD2DMod
from Main.Mods.REFrameworkMod import REFrameworkMod


class REFrameWorkDependentMod(ModModel):
    def get_is_REFramework_installed(self) -> bool:
        """Check if REFramework is installed in the current install path."""
        reframework_mod = REFrameworkMod(self.resource_folder, self.game_install_path, self.state_file_helper, self.logger)
        return reframework_mod.is_installed()
    
    def get_is_REFrameworkD2D_installed(self) -> bool:
        """Check if REFrameworkD2D is installed in the current install path."""
        reframework_d2d_mod = REFrameworkD2DMod(self.resource_folder, self.game_install_path, self.state_file_helper, self.logger)
        return reframework_d2d_mod.is_installed()
    
    def install(self):
        if not self.get_is_REFramework_installed():
            self._log("Cannot install mod because REFramework is not installed.", level="ERROR")
            return False
        
        if not self.get_is_REFrameworkD2D_installed():
            self._log("Cannot install mod because REFrameworkD2D is not installed.", level="ERROR")
            return False
        
        return super().install()