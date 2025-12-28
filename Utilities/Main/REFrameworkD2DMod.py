from pathlib import Path
import shutil
from ModModel import ModModel

class REFrameworkD2DMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str):
        super().__init__(resource_folder, game_install_path)
        self.name = "REFramework Direct2D"
        self.description = "REFramework Direct2D is an extension for REFramework that enables Direct2D rendering."
        self.REFrameworkD2D_folder_path = Path(self.resource_folder) / "REFramework Direct2D" / "reframework"

    def install(self):
        if self.is_installed():
            print("REFramework Direct2D is already installed.")
            return False
        
        if not self.REFrameworkD2D_folder_path.exists() or not self.REFrameworkD2D_folder_path.is_dir():
            print(f"REFramework Direct2D folder {self.REFrameworkD2D_folder_path} not found.")
            return False

        if not self.install_path.exists():
            print(f"Game install path {self.game_install_path} does not exist.")
            return False

        destination = self.install_path / self.REFrameworkD2D_folder_path.name
        try:
            shutil.copytree(
                self.REFrameworkD2D_folder_path,
                destination,
                dirs_exist_ok=True  # allows overwrite / merge
            )
        except Exception as e:
            print(f"Failed to copy REFramework folder: {e}")
            return False

        return self.is_installed()
    
    def uninstall(self):
        if not self.is_installed():
            print("REFramework Direct2D is not installed.")
            return False

        if not self.REFrameworkD2D_folder_path.exists() or not self.REFrameworkD2D_folder_path.is_dir():
            print(f"REFramework Direct2D folder {self.REFrameworkD2D_folder_path} not found.")
            return False

        target_path = self.install_path / self.REFrameworkD2D_folder_path.name
        files_to_remove = {
                "autorun": ["reframework-d2d.lua"],
                "plugins": ["reframework-d2d.dll"]
            }

        for subfolder, filenames in files_to_remove.items():
            folder_path = target_path / subfolder
            for filename in filenames:
                file_path = folder_path / filename
                if file_path.exists() and file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"Removed {file_path}")
                    except Exception as e:
                        print(f"Failed to remove {file_path}: {e}")
                else:
                    print(f"{file_path} does not exist")

        return not self.is_installed()
    
    def is_installed(self):
        reframework = self.install_path / "reframework"
        autorun = reframework / "autorun"
        plugins = reframework / "plugins"

        return (
            reframework.is_dir() and
            autorun.is_dir() and
            plugins.is_dir() and
            (autorun / "reframework-d2d.lua").is_file() and
            (plugins / "reframework-d2d.dll").is_file()
        )