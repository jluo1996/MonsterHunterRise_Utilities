from pathlib import Path
import shutil

class ModModel:
    def __init__(self, resource_folder: str, game_install_path: str):
        self.name = ""
        self.description = ""
        self.resource_folder = resource_folder
        self.mod_file_path = None
        self.install_path = Path(game_install_path)
        self.is_selected = False

    def install(self):
        source_folder = self.mod_file_path
        target_folder = self.install_path

        if not source_folder.exists() or not source_folder.is_dir():
            raise ValueError(f"Source folder does not exist: {source_folder}")
        if not target_folder.exists():
            target_folder.mkdir(parents=True)

        # Iterate all files and folders in source
        for item in source_folder.rglob("*"):
            relative_path = item.relative_to(source_folder)
            target_item = target_folder / relative_path

            if item.is_dir():
                # Create subfolder if it doesn't exist
                target_item.mkdir(parents=True, exist_ok=True)
            else:
                # Copy file (overwrites if exists)
                shutil.copy2(item, target_item)
    
    def uninstall(self):
        source_folder = self.mod_file_path
        target_folder = self.install_path

        if not source_folder.exists() or not source_folder.is_dir():
            raise ValueError(f"Source folder does not exist: {source_folder}")
        if not target_folder.exists() or not target_folder.is_dir():
            raise ValueError(f"Target folder does not exist: {target_folder}")

        # Remove files in target that exist in source
        for src_file in source_folder.rglob("*"):
            if src_file.is_file():
                relative_path = src_file.relative_to(source_folder)
                tgt_file = target_folder / relative_path
                if tgt_file.exists() and tgt_file.is_file():
                    try:
                        tgt_file.unlink()
                        print(f"Removed file: {tgt_file}")
                    except Exception as e:
                        print(f"Failed to remove {tgt_file}: {e}")

        # Optionally, remove empty directories in target
        for tgt_dir in sorted(target_folder.rglob("*"), key=lambda p: -p.parts.__len__()):
            if tgt_dir.is_dir() and not any(tgt_dir.iterdir()):
                try:
                    tgt_dir.rmdir()
                    print(f"Removed empty folder: {tgt_dir}")
                except Exception as e:
                    print(f"Failed to remove {tgt_dir}: {e}")

    def is_installed(self) -> bool:
        source_folder = self.mod_file_path
        target_folder = self.install_path

        if not source_folder.exists() or not source_folder.is_dir():
            raise ValueError(f"Source folder does not exist: {source_folder}")
        if not target_folder.exists() or not target_folder.is_dir():
            raise ValueError(f"Target folder does not exist: {target_folder}")

        # Iterate through all files in source_folder recursively
        for src_file in source_folder.rglob("*"):
            if src_file.is_file():
                # Compute the relative path of the file to source_folder
                rel_path = src_file.relative_to(source_folder)
                # Corresponding file in target folder
                tgt_file = target_folder / rel_path
                if not tgt_file.is_file():
                    # File missing in target
                    return False

        # All files exist in target
        return True
    
    def set_selected(self, selected: bool):
        self.is_selected = selected

    