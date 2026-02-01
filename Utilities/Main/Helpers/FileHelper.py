from pathlib import Path
import tempfile

class FileHelper:
    def get_resources_folder_path(self):
        return Path(__file__).resolve().parent.parent.parent / "Resources"
    
    def get_icons_folder_path(self):
        return self.get_resources_folder_path() / "Icons"
    
    def get_pictures_folder_path(self):
        return self.get_resources_folder_path() / "Pictures"
    
    def _get_temp_folder_path(self):
        temp_dir = tempfile.gettempdir()
        return Path(temp_dir)
    
    def get_log_folder_path(self):
        log_folder = self._get_temp_folder_path() / "MHR_Utilities_Logs"
        log_folder.mkdir(parents=True, exist_ok=True)
        return log_folder