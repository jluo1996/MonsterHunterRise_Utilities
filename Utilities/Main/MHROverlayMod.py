from ModModel import ModModel

class MHROverlayMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "MHR Overlay"
        self.description = "MHR Overlay is a mod that adds an overlay to Monster Hunter Rise."

    def install(self):
        # Placeholder for actual installation logic
        return True

    def uninstall(self):
        # Placeholder for actual uninstallation logic
        return True

    def is_installed(self):
        # Placeholder for actual installed check logic
        return False