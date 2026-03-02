import os
import shutil
import winreg
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from string import ascii_uppercase
from typing import List

import psutil


MHR_STEAM_APP_ID = 1446780
MHR_EXE_NAME = "MonsterHunterRise.exe"



class GameInfoHelper: 
    def __init__(self, logger):
        self.logger = logger

    def backup_MHR_user_data(self) -> bool:
        steam_user_data_path = Path(self._get_steam_user_data_path())
        if steam_user_data_path is None or not steam_user_data_path.exists():
            self.logger.log("Steam user data path not found or inaccessible.", level="ERROR")
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
            self.logger.log(f"Backing up: {source} -> {destination}")
            shutil.copytree(source, destination, dirs_exist_ok=True)
            if not destination.exists():
                self.logger.log(f"Backup failed for folder: {source}", level="ERROR")
                success = False

        return success

    def _get_steam_user_data_path(self) -> Path | None:
        # Placeholder implementation
        steam_path = self._get_steam_install_path()
        if steam_path is None or not steam_path.exists():
            self.logger.log("Steam installation not found.", level="ERROR")
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
    
    def get_MHR_install_path(self, auto_detect: bool = False) -> Path | None:
        if not auto_detect:
            steam_install_path = self._get_steam_install_path()
            if steam_install_path is None or not steam_install_path.exists():
                self.logger.log("Steam installation not found.", level="ERROR")
                return None
            
            expected_path = steam_install_path / "steamapps" / "common" / "MonsterHunterRise"
            if not expected_path.exists():
                self.logger.log(f"Expected MHR path does not exist: {expected_path}", level="ERROR")
                return None
            return expected_path
        
        found_exes = self._find_exe_in_named_folder(MHR_EXE_NAME, "MonsterHunterRise")
        return found_exes[0] if found_exes else None
    
    def _list_available_drives(self) -> List[Path]:
        """
        Returns a list of root Paths for all available drives on Windows.
        Example: [Path('C:/'), Path('D:/'), ...]
        """
        drives = []
        for letter in ascii_uppercase:
            root = Path(f"{letter}:/")
            if root.exists():
                drives.append(root)
        return drives
    
    def _safe_walk(self,base: Path) -> Iterable[tuple[str, list[str], list[str]]]:
        """
        A wrapper around os.walk that ignores permission errors and prunes
        some noisy/system directories for performance.
        """
        # `onerror` swallows errors like PermissionError
        for dirpath, dirnames, filenames in os.walk(
            base,
            topdown=True,
            onerror=lambda e: None,  # ignore errors
            followlinks=False,       # avoid symlink/shortcut loops
        ):
            # Prune well-known, heavy, or restricted directories
            prune = {
                'System Volume Information',
                '$Recycle.Bin',
                'Windows',        # comment out if you need to scan Windows dir
                'ProgramData',
                'OneDriveTemp',
            }
            # In-place prune: remove entries we don't want to descend into
            dirnames[:] = [d for d in dirnames if d not in prune]
    
            yield dirpath, dirnames, filenames
    
    def _find_exe_in_named_folder(self,
        exe_name: str,
        folder_name: str,
        *,
        case_sensitive: bool = False
    ) -> List[Path]:
        """
        Search for `exe_name` in a directory whose name is exactly `folder_name`.
        Searches *common directories first* (Program Files, Program Files (x86), home),
        then scans all available drives (A:/ to Z:/). Stops at the first match.
    
        Parameters
        ----------
        exe_name : str
            Executable name to search for (e.g., 'mytool.exe').
        folder_name : str
            Name of the directory that must be the *parent folder* of the exe.
        case_sensitive : bool
            If True, match names with case sensitivity; otherwise case-insensitive.
    
        Returns
        -------
        List[Path]
            A list containing at most one Path: the parent folder that matches
            `folder_name` and contains the executable `exe_name`. Returns [] if not found.
        """
        # Normalize comparison based on case sensitivity
        def norm(s: str) -> str:
            return s if case_sensitive else s.lower()
    
        target_file = norm(exe_name)
        target_folder = norm(folder_name)
    
        # COMMON DIRECTORIES: searched first
        COMMON_DIRS = [
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
            Path.home(),
        ]
    
        # 1) Search common directories first
        for base in COMMON_DIRS:
            if not base.exists():
                continue
            
            for dirpath, _dirnames, filenames in self._safe_walk(base):
                # Quick filename check with case handling
                if case_sensitive:
                    match = exe_name in filenames
                else:
                    # Normalize filenames to lowercase to compare
                    match = target_file in (name.lower() for name in filenames)
    
                if not match:
                    continue
                
                parent = Path(dirpath)
                if norm(parent.name) == target_folder:
                    return [parent]  # stop at first match
    
        # 2) Then search ALL available drives
        for root in self._list_available_drives():
            if not root.exists():
                continue
            
            for dirpath, _dirnames, filenames in self._safe_walk(root):
                if case_sensitive:
                    match = exe_name in filenames
                else:
                    match = target_file in (name.lower() for name in filenames)
    
                if not match:
                    continue
                
                parent = Path(dirpath)
                if norm(parent.name) == target_folder:
                    return [parent]  # stop at first match
    
        # Nothing found
        return []
    
    def is_game_running(self):
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == MHR_EXE_NAME.lower():
                    return True
            except psutil.NoSuchProcess:
                pass
        return False
    