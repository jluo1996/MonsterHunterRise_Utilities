class ModModel:
    def __init__(self, resource_folder: str, game_install_path: str):
        self.name = ""
        self.description = ""
        self.resource_folder = resource_folder
        self.game_install_path = game_install_path
        self.is_selected = False

    def install(self):
        print(f"Installing mod: {self.name}")
        # Placeholder for actual installation logic
        return True
    
    def uninstall(self):
        print(f"Uninstalling mod: {self.name}")
        # Placeholder for actual uninstallation logic
        return True
    
    def is_installed(self):
        return False
    
    def set_selected(self, selected: bool):
        self.is_selected = selected

    