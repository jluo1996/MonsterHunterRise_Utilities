from datetime import datetime
import os
from pathlib import Path
import shutil

from Main.Helpers.StateFileHelper import StateFileHelper

class ModModel:
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper: StateFileHelper, logger):
        self.name = ""
        self.description = ""
        self.resource_folder = resource_folder
        self.mod_file_path = None
        self.install_path = Path(game_install_path)
        self.game_install_path = Path(game_install_path)
        self.is_selected = False
        self.settings = []
        self.logger = logger
        self.state_file_helper = state_file_helper

    def get_has_settings(self) -> bool:
        return isinstance(self.settings, list) and len(self.settings) > 0
    
    def _get_settings(self):
        """Initialize settings with default values. Override in subclass if needed."""
        return []
    
    def save_settings(self):
        """Override in subclass if you need to persist settings changes."""
        return

    def install(self):
        if self.is_installed():
            self._log("Mod is already installed. Skipping installation.")
            return True  # Already installed
        
        source_folder = self.mod_file_path
        target_folder = self.install_path

        if not source_folder.exists() or not source_folder.is_dir():
            self._log(f"Source folder does not exist: {source_folder}", level="ERROR")
            return False
        if not target_folder.exists():
            self._log(f"Target folder does not exist, creating: {target_folder}")
            target_folder.mkdir(parents=True)

        # Iterate all files and folders in source
        for item in source_folder.rglob("*"):
            relative_path = item.relative_to(source_folder)
            target_item = target_folder / relative_path

            if item.is_dir():
                # Create subfolder if it doesn't exist
                target_item.mkdir(parents=True, exist_ok=True)
                self._log(f"Created folder: {target_item}")
            else:
                # Copy file (overwrites if exists)
                shutil.copy2(item, target_item)
                self._log(f"Copied file: {target_item}")

        if not self._is_install_internal():
            self._log("Failed to install mod. Some files may not have been copied.", level="ERROR")
            return False
            
        self._log("Mod installed successfully.")
        now = datetime.now()
        self._update_state_after_install()
        return True
    
    def _update_state_after_install(self):
        now = datetime.now()
        self.state_file_helper.set_state(self.name, "InstallTime", now.isoformat())
    
    def uninstall(self):
        if not self.is_installed():
            self._log("Mod is not installed. Skipping uninstallation.")
            return True  # Already uninstalled
        
        source_folder = self.mod_file_path
        target_folder = self.install_path

        if not source_folder.exists() or not source_folder.is_dir():
            self._log(f"Source folder does not exist: {source_folder}", level="ERROR")
            return False
        if not target_folder.exists() or not target_folder.is_dir():
            self._log(f"Target folder does not exist: {target_folder}", level="ERROR")
            return False

        # Remove files in target that exist in source
        for src_file in source_folder.rglob("*"):
            if src_file.is_file():
                relative_path = src_file.relative_to(source_folder)
                tgt_file = target_folder / relative_path
                if tgt_file.exists() and tgt_file.is_file():
                    try:
                        tgt_file.unlink()
                        self._log(f"Removed file: {tgt_file}")
                    except Exception as e:
                        self._log(f"Failed to remove {tgt_file}: {e}", level="ERROR")
                        return False

        # Optionally, remove empty directories in target
        for tgt_dir in sorted(target_folder.rglob("*"), key=lambda p: -p.parts.__len__()):
            if tgt_dir.is_dir() and not any(tgt_dir.iterdir()):
                try:
                    tgt_dir.rmdir()
                    self._log(f"Removed empty folder: {tgt_dir}")
                except Exception as e:
                    self._log(f"Failed to remove {tgt_dir}: {e}", level="ERROR")
                    return False
                
        if self._is_install_internal():
            self._log("Failed to uninstall mod. Some files may not have been removed.", level="ERROR")
            return False
        
        self._log("Mod uninstalled successfully.")
        self.state_file_helper.remove_mod_state(self.name)
        return True
    
    def _is_install_internal(self) -> bool:
        """ This method checks if the mod is installed by verifying that all files in the mod's source folder exist in the target install folder with matching types and sizes. """
        source_folder = self.mod_file_path
        target_folder = self.install_path

        return self._get_content_exist(str(source_folder), str(target_folder))
                    
    def is_installed(self) -> bool:
        return self.state_file_helper.get_state(self.name, "InstallTime") is not None
    
    def set_selected(self, selected: bool):
        self.is_selected = selected

    def update_install_path(self, new_game_install_path):
        self._log(f"Updating install path from {self.install_path} to: {new_game_install_path}")
        self.install_path = Path(new_game_install_path)

    def _log(self, message: str, level: str = "INFO"):
        self.logger.log(f"[{self.name}] {message}", level=level)
    
    def _get_content_exist(self, sourceFolderPath: str, destinationFolderPath: str) -> bool:
        """
        Returns True if *all contents* of `sourceFolderPath` exist under
        `destinationFolderPath` with matching types and (for files) matching sizes.

        Notes:
        - Shallow check: existence + type + size (no hashing).
        - Allows extra files/dirs in the destination.
        - Does not follow directory symlinks (os.walk default). Symlinked files are treated as files.
        - Fails safe (returns False) on permission/stat errors.
        """
        src_root = Path(sourceFolderPath)
        dst_root = Path(destinationFolderPath)

        # Both must exist and be directories
        if not src_root.is_dir() or not dst_root.is_dir():
            return False

        # Walk the source tree and ensure each entry exists correspondingly in destination
        for root, dirnames, filenames in os.walk(src_root, topdown=True, followlinks=False):
            root_path = Path(root)
            rel_dir = root_path.relative_to(src_root)
            dst_here = dst_root / rel_dir  # map source subtree directly under destination root

            # 1) Ensure directories exist as directories
            for d in dirnames:
                dst_dir = dst_here / d
                if not dst_dir.exists() or not dst_dir.is_dir():
                    return False

            # 2) Ensure files exist as files with matching size
            for f in filenames:
                src_file = root_path / f
                dst_file = dst_here / f

                if not dst_file.exists() or not dst_file.is_file():
                    return False

                try:
                    if src_file.stat().st_size != dst_file.stat().st_size:
                        return False
                except OSError:
                    return False

        return True

