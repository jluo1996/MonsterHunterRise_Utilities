from pathlib import Path
from Main.Mods.REFrameworkMod import REFrameworkMod
from Main.Mods.REFrameworkD2DMod import REFrameworkD2DMod
from Main.Mods.TeleportMod import TeleportMod
from Main.Mods.SpiritBirdsMod import SpiritBirdsMod
from Main.Mods.DropRatesEnhancedMod import DropRatesEnhancedMod
from Main.Mods.MHROverlayMod import MHROverlayMod
from Main.Mods.AutoArgosyMod import AutoArgosyMod
from Main.Mods.AutoCohootNestMod import AutoCohootNestMod
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.Helpers.FileHelper import FileHelper
from Main.Mods.CharmEditorMod import CharmEditorMod
from Main.Mods.MonsterWeaknessIconIndicatorMod import MonsterWeaknessIconIndicatorMod
from Main.Helpers.StateFileHelper import StateFileHelper
from Main.Mods.FastReturnMod import FastReturnMod
from Main.Mods.MatchmakingMod import MatchmakingMod
from Main.Mods.CustomInGameMenuMod import CustomInGameMenuMod
from Main.Mods.SkipIntroLogoMod import SkipIntroLogoMod

GAME_INSTALL_PATH = Path(__file__).resolve().parent.name

class MainViewModel():
    def __init__(self):
        self.mods = []  # This will hold a list of ModModel instances
        file_helper = FileHelper()
        self.state_file_helper = StateFileHelper(file_helper=file_helper)
        self.resources_path = file_helper.get_resources_folder_path()
        _ = self.auto_detect_game_install_path(auto_detect=False, update_game_install_path=True)  

    def get_mods(self) -> list:
        return self.mods
    
    def init_mods(self):    
        self.mods.append(REFrameworkMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(REFrameworkD2DMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(TeleportMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(SpiritBirdsMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(AutoArgosyMod(self.resources_path, self.game_install_path, self.state_file_helper)) 
        self.mods.append(AutoCohootNestMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(MHROverlayMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(DropRatesEnhancedMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(CharmEditorMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(MonsterWeaknessIconIndicatorMod(self.resources_path, self.game_install_path, self.state_file_helper))
        # self.mods.append(KillCamMod(self.resources_path, self.game_install_path, self.state_file_helper)) # Use FastReturnMod instead since it is simpler.
        self.mods.append(FastReturnMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(MatchmakingMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(CustomInGameMenuMod(self.resources_path, self.game_install_path, self.state_file_helper))
        self.mods.append(SkipIntroLogoMod(self.resources_path, self.game_install_path, self.state_file_helper))

        # self.mods.sort(key=lambda mod: mod.name)

    def install_selected_mods(self):
        all_success = True

        for mod in self.mods:
            if mod.is_selected:
                if not mod.install():
                    all_success = False

        return all_success

    def uninstall_selected_mods(self):
        all_success = True

        for mod in self.mods:
            if mod.is_selected:
                if not mod.uninstall():
                    all_success = False

        return all_success

    def update_game_install_path(self, new_path):
        self.game_install_path = new_path
        for mod in self.mods:
            mod.update_install_path(new_path)

    def auto_detect_game_install_path(self, auto_detect: bool = False, update_game_install_path: bool = False) -> list[Path]:
        game_info_helper = GameInfoHelper()
        detected_path = game_info_helper.get_MRH_install_path(auto_detect)
        if update_game_install_path and detected_path:
            self.update_game_install_path(str(detected_path))
        return [detected_path] if detected_path else []