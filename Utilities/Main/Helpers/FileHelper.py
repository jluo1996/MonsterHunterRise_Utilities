import os
import shutil
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
            self._log("Install state file already exists.", level="WARNING")
        return install_state_file_path
    
    def get_app_data_folder_path(self):
        base_path = Path(os.getenv('LOCALAPPDATA'))
        app_data_folder_path = base_path / self.APP_NAME
        app_data_folder_path.mkdir(parents=True, exist_ok=True)
        return app_data_folder_path

    def clear_cache(self, active_log_file_path: Path | None = None):
        removed_items = []

        temp_removed = self._clear_directory_contents(self.get_app_data_temp_folder_path())
        if temp_removed:
            removed_items.append(f"removed {temp_removed} temporary item(s)")

        log_removed = self._clear_log_files(active_log_file_path=active_log_file_path)
        if log_removed:
            removed_items.append(f"cleared {log_removed} log file(s)")

        if not removed_items:
            return "Cache was already empty."

        return "Successfully cleared cache: " + ", ".join(removed_items) + "."

    def _clear_directory_contents(self, directory_path: Path):
        removed_count = 0

        for item in directory_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            removed_count += 1

        return removed_count

    def _clear_log_files(self, active_log_file_path: Path | None = None):
        log_folder = self.get_log_folder_path()
        removed_count = 0
        active_log_file_path = Path(active_log_file_path) if active_log_file_path else None

        for log_file in log_folder.glob('*.log'):
            if active_log_file_path and log_file == active_log_file_path:
                log_file.write_text('', encoding='utf-8')
            else:
                log_file.unlink()
            removed_count += 1

        return removed_count

    def _log(self, message, level="INFO"):
        if self.logger:
            self.logger.log(message, level)

    def get_app_data_temp_folder_path(self):
        temp_folder = self.get_app_data_folder_path() / "temp"
        temp_folder.mkdir(parents=True, exist_ok=True)
        return temp_folder
