import os
from pathlib import Path

class FileHelper:
    def __init__(self, logger=None):
        self.logger = logger
        self.APP_NAME = "MHR Utilities"

    def get_resources_folder_path(self):
        return Path(__file__).resolve().parent.parent.parent / "Resources"
    
    def get_icons_folder_path(self):
        return self.get_resources_folder_path() / "Icons"
    
    def get_pictures_folder_path(self):
        return self.get_resources_folder_path() / "Pictures"
    
    def get_log_folder_path(self):
        log_folder = self.get_app_data_folder_path() / "MHR_Utilities_Logs"
        log_folder.mkdir(parents=True, exist_ok=True)
        return log_folder
    
    def get_install_state_file_path(self):
        install_state_file_path = self.get_app_data_folder_path() / "mhr_utilities_install_state.json"
        try:
            with open(install_state_file_path, "x") as f:   # "x" = create only if not exist
                f.write("{}")  # write default content
            self._log("Install state file created.", level="INFO")
        except FileExistsError:
            self._log("Install state file already exists.", level="ERROR")
        return install_state_file_path
    
    def get_app_data_folder_path(self):
        base_path = Path(os.getenv('LOCALAPPDATA'))
        app_data_folder_path = base_path / self.APP_NAME
        app_data_folder_path.mkdir(parents=True, exist_ok=True)
        return app_data_folder_path
    
    def _log(self, message, level="INFO"):
        if self.logger:
            self.logger.log(message, level)

    def get_app_data_temp_folder_path(self):
        temp_folder = self.get_app_data_folder_path() / "temp"
        temp_folder.mkdir(parents=True, exist_ok=True)
        return temp_folder