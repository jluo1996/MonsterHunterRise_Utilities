from pathlib import Path

class FileHelper:
    def __init__(self):
        pass

    def get_resources_folder_path(self):
        return Path(__file__).resolve().parent.parent.parent / "Resources"
    
    def get_icons_folder_path(self):
        return self.get_resources_folder_path() / "Icons"
    
    def get_pictures_folder_path(self):
        return self.get_resources_folder_path() / "Pictures"