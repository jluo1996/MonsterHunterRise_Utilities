from datetime import datetime
from pathlib import Path
import shutil
import winreg

MHR_STEAM_APP_ID = 1446780

class GameInfoHelper:
    def backup_MHR_user_data(self) -> bool:
        steam_user_data_path = Path(self._get_steam_user_data_path())
        if steam_user_data_path is None or not steam_user_data_path.exists():
            print("Steam user data path not found or inaccessible.")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        success = True
        
        for folder in steam_user_data_path.iterdir():
            if not folder.is_dir():
                continue

            source = folder / str(MHR_STEAM_APP_ID)
            if not source.exists():
                continue

            backup_folder_name = f"{MHR_STEAM_APP_ID}_backup_{timestamp}"
            destination = folder / backup_folder_name
            print(f"Backing up: {source} -> {destination}")
            shutil.copytree(source, destination, dirs_exist_ok=True)
            if not destination.exists():
                print(f"Backup failed for folder: {source}")
                success = False

        return success


    def _get_steam_user_data_path(self) -> Path | None:
        # Placeholder implementation
        steam_path = self._get_steam_install_path()
        if steam_path is None or not steam_path.exists():
            print("Steam installation not found.")
            return None
        return steam_path / "userdata"
    
    def _get_steam_install_path(self) -> Path | None:
        """
        Returns the Steam installation path as a Path object,
        or None if Steam is not installed.
        """
        reg_paths = [
            r"SOFTWARE\WOW6432Node\Valve\Steam",  # 64-bit Windows
            r"SOFTWARE\Valve\Steam"               # 32-bit Windows
        ]
    
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                    install_path, _ = winreg.QueryValueEx(key, "InstallPath")
                    return Path(install_path)
            except FileNotFoundError:
                continue
            
        return None