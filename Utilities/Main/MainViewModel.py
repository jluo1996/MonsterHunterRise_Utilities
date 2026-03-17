from pathlib import Path

from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.Helpers.StateFileHelper import StateFileHelper
from Main.Mods.AutoArgosyMod import AutoArgosyMod
from Main.Mods.AutoCohootNestMod import AutoCohootNestMod
from Main.Mods.CharmEditorMod import CharmEditorMod
from Main.Mods.CustomInGameMenuMod import CustomInGameMenuMod
from Main.Mods.DropRatesEnhancedMod import DropRatesEnhancedMod
from Main.Mods.FastReturnMod import FastReturnMod
from Main.Mods.MHROverlayMod import MHROverlayMod
from Main.Mods.MatchmakingMod import MatchmakingMod
from Main.Mods.MonsterWeaknessIconIndicatorMod import MonsterWeaknessIconIndicatorMod
from Main.Mods.REFrameworkD2DMod import REFrameworkD2DMod
from Main.Mods.REFrameworkMod import REFrameworkMod
from Main.Mods.SkipIntroLogoMod import SkipIntroLogoMod
from Main.Mods.SpiritBirdsMod import SpiritBirdsMod
from Main.Mods.TeleportMod import TeleportMod
from Main.Mods.SkipDangoSongMod import SkipDangoSongMod
from Main.Mods.AutoLikeMod import AutoLikeMod
from Main.Updater.Updater import Updater
from Main.Log.Logger import Logger
from Main.Thread.ThreadWorker import ThreadWorker

GAME_INSTALL_PATH = Path(__file__).resolve().parent.name

class MainViewModel():
    def __init__(self, logger : Logger):
        self.mods = []  # This will hold a list of ModModel instances
        self.logger = logger
        self.file_helper = FileHelper(self.logger)
        self.state_file_helper = StateFileHelper(file_helper=self.file_helper)
        self.updater = Updater(file_helper=self.file_helper, logger=self.logger)
        self.resources_path = self.file_helper.get_resources_folder_path()
        

    def on_startup(self):
        _ = self.auto_detect_game_install_path(auto_detect=False, update_game_install_path=True)  
        self._init_mods()

    def has_newer_version(self):
        return self.updater.has_newer_version()
    
    def get_latest_version_number(self, only_number=False):
        return self.updater.get_latest_version_number(only_number)
    
    def start_update_preparation_process(self, finish_callback=None):
        self.prepare_thread = ThreadWorker()
        self.prepare_thread.set_function(self.updater.prepare_to_update)
        for callback in finish_callback if isinstance(finish_callback, list) else [finish_callback]:
            if callback:
                self.prepare_thread.finished.connect(callback)
        self.prepare_thread.start()

    def start_update_process(self):
        self.updater.launch_update()

    def get_mods(self) -> list:
        return self.mods
    
    def _init_mods(self):    
        self.mods.append(REFrameworkMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(REFrameworkD2DMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(TeleportMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(SpiritBirdsMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(AutoArgosyMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger)) 
        self.mods.append(AutoCohootNestMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(MHROverlayMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(DropRatesEnhancedMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(CharmEditorMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(MonsterWeaknessIconIndicatorMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        # self.mods.append(KillCamMod(self.resources_path, self.game_install_path, self.state_file_helper)) # Use FastReturnMod instead since it is simpler.
        self.mods.append(FastReturnMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(MatchmakingMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(CustomInGameMenuMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(SkipIntroLogoMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(SkipDangoSongMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))
        self.mods.append(AutoLikeMod(self.resources_path, self.game_install_path, self.state_file_helper, self.logger))

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
        game_info_helper = GameInfoHelper(self.logger)
        detected_path = game_info_helper.get_MHR_install_path(auto_detect)
        if update_game_install_path and detected_path:
            self.update_game_install_path(str(detected_path))
                # TODO: if game install path is changed, need to apply the original config on the new game path
        return [detected_path] if detected_path else []