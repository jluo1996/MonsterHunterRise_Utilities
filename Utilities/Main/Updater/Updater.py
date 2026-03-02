import subprocess
import sys
import zipfile

import requests
import win32api
from packaging import version
from pathlib import Path

from Main.Helpers.FileHelper import FileHelper

LATEST_RELEASE_URL = "https://api.github.com/repos/jluo1996/MonsterHunterRise_Utilities/releases/latest"

class Updater():
    def __init__(self, file_helper : FileHelper=None, logger=None):
        self.file_helper = file_helper if file_helper else FileHelper()
        self.logger = logger
        self.updater_script_path = None
        self.temp_update_folder = None

    def _log(self, message, level="INFO"):
        if self.logger:
            self.logger.log(message, level=level)
        else:
            print(f"{level}: {message}")

    def _get_latest_release(self):
        response = requests.get(LATEST_RELEASE_URL)
        data = response.json()

        latest_version = data["tag_name"]
        download_url = data["assets"][0]["browser_download_url"]

        return latest_version, download_url
    
    def _download_file(self, url, save_path):
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def _get_current_exe_version(self):
        exe_path = sys.executable 
        info = win32api.GetFileVersionInfo(exe_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version
    
    def has_newer_version(self):
        latest_version, _ = self._get_latest_release()
        latest_version = latest_version.lstrip('v')
        latest = version.parse(latest_version)

        current_version = self._get_current_exe_version()
        current = version.parse(current_version)

        return latest > current

    def get_latest_version_number(self, only_number=False):
        latest_version, _ = self._get_latest_release()
        return latest_version.lstrip('v') if only_number else latest_version
    
    def _download_latest_release(self, download_url, save_path, retry_count=3):
        self._log("Starting download...", level="INFO")
        while (retry_count > 0):
             try:
                self._download_file(download_url, save_path)
                if save_path.exists():
                    self._log("Download successful.", level="INFO")
                    break
                else:
                    raise Exception("File does not exist after download.")
             except Exception as e:
                self._log(f"Error downloading the update: {e}", level="ERROR")
                retry_count -= 1
                if retry_count > 0:
                    self._log(f"Retrying... ({3 - retry_count}/3)", level="INFO")
                else:
                    self._log("Failed to download the update after 3 attempts.", level="ERROR")
                    return False
        return True

    def _set_temp_update_folder(self, folder_path):
        self.temp_update_folder = folder_path
        if not self.temp_update_folder.exists():
            self.temp_update_folder.mkdir(parents=True, exist_ok=True)

    
    def prepare_to_update(self):
        if not self.has_newer_version():
            self._log("Already on the latest version.", level="INFO")
            return
        
        latest_version, download_url = self._get_latest_release()
        self._set_temp_update_folder(self.file_helper.get_app_data_temp_folder_path() / f"update_{latest_version}")
        save_path = self.temp_update_folder / latest_version

        # download the latest release
        if not self._download_latest_release(download_url, save_path, retry_count=3):
            self._log("Failed to download the latest release.", level="ERROR")
            return False
        
        # extract the release
        extract_destination = self.temp_update_folder / f"extracted_{latest_version}"
        self._log(f"Extracting update to {extract_destination}...", level="INFO")
        extract_destination = self._extract_zip_file(save_path, extract_destination)
        self._log("Extraction completed.", level="INFO")

        # Remove the source file after extraction
        self._log("Cleaning up downloaded zip file...", level="INFO")
        if save_path.exists():
            save_path.unlink()
        self._log("Clean up completed.", level="INFO")

        # generate the updater script
        self._log("Generating updater script...", level="INFO")
        current_exe = Path(sys.executable)
        current_exe_folder = current_exe.parent
        self.updater_script_path = self._generate_updater_script(current_exe.name, current_exe_folder, extract_destination, self.temp_update_folder)
        self._log(f"Updater script generated at {self.updater_script_path}.", level="INFO") 
                
        return True
    
    def _extract_zip_file(self, zip_path, extract_to_path):
        zip_path = Path(zip_path)
        extract_to_path = Path(extract_to_path)

        extract_to_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)

        return extract_to_path 
    
    def _get_updater_script_content(self, current_exe_name, current_exe_folder, new_version_folder):
        return f"""@echo off
        title Updating MonsterHunterRise Utilities...
        echo.
        echo ==========================================
        echo        Updating Application
        echo ==========================================
        echo.

        REM Wait for the main application to close
        echo Waiting for application to close...
        timeout /t 2 /nobreak > nul 

        REM Clear the destination folder
        echo.
        echo Clearing old files from "{current_exe_folder}"...
        if exist "{current_exe_folder}" (
            echo Deleting contents of "{current_exe_folder}"...
            rd /s /q "{current_exe_folder}"
        )
        REM Recreate the destination folder
        mkdir "{current_exe_folder}"

        
        REM Copy everything from source to destination
        echo. 
        echo Copying new files to "{current_exe_folder}"...
        echo Copying files from "{new_version_folder}" to "{current_exe_folder}"...
        xcopy "{new_version_folder}\\*" "{current_exe_folder}\\" /s /e /h /y

        REM Cleanup the extracted update files
        echo. 
        echo Cleaning up temporary files...
        rd /s /q "{new_version_folder}"

        REM Start the new version of the application
        echo.
        echo Update completed!
        echo restarting application...
        start "" "{current_exe_folder}\{current_exe_name}"

        REM Delete the updater script itself
        del "%~f0"
        
        echo.
        echo Done. Closing this window...
        timeout /t 2 > nul
        """
    
    def _generate_updater_script(self, current_exe_name, current_exe_folder, new_version_folder, temp_folder):
        script_content = self._get_updater_script_content(current_exe_name, current_exe_folder, new_version_folder)
        temp_folder_path = Path(temp_folder)
        updater_script_path = temp_folder_path / "update.bat"
        updater_script_path.write_text(script_content, encoding='utf-8')
        return updater_script_path
    
    def _launch_update_script(self):
        if not self.updater_script_path or not self.updater_script_path.exists():
            self._log("Updater script not found. Cannot launch update.", level="ERROR")
            return
        
        subprocess.Popen(
            str(self.updater_script_path),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

    def launch_update(self):
        self._launch_update_script()
        sys.exit()

                
        

