from pathlib import Path
from Main.Mods.ModModel import ModModel
from Main.Mods.ModSetting import ModSetting

DROP_RATE_SETTING = "Drop Rate"
DROP_RATE_BALANCED = "Balanced"
DROP_RATE_NOT_SO_BALANCED = "Not so Balanced"
DROP_RATE_UNBALANCED = "Unbalanced"

class DropRatesEnhancedMod(ModModel):
    def __init__(self, resource_folder: str, game_install_path: str, state_file_helper):
        super().__init__(resource_folder, game_install_path, state_file_helper)
        self.name = "Drop Rates Enhanced"
        self.description = "More rewards per monster in a balanced way."
        self.default_drop_rate_option = DROP_RATE_BALANCED
        self.current_drop_rate = self._read_current_drop_rate()
        self.mod_file_path = Path(self.resource_folder) / "Drop Rates Enhanced" / self.current_drop_rate
        self.settings = self._get_settings()

    def _read_current_drop_rate(self):
        """ Read the current drop rate setting from the state file, or return the default if not set or invalid. """
        current_drop_rate = self.state_file_helper.get_state(self.name, DROP_RATE_SETTING)
        if current_drop_rate in self._get_drop_rate_options():
            return current_drop_rate
        return self.default_drop_rate_option

    def _get_drop_rate_options(self):
        return [DROP_RATE_BALANCED, 
                DROP_RATE_NOT_SO_BALANCED,
                DROP_RATE_UNBALANCED]

    def _get_settings(self):
        settings = []
        settings.append(ModSetting(
            name=DROP_RATE_SETTING,
            setting_type=list,
            value=self._get_drop_rate_options(),
            description="Select the desired drop rate enhancement level.",
            current_value=self.current_drop_rate
        ))
        return settings
    
    def _update_state_after_install(self):
        super()._update_state_after_install()
        self.state_file_helper.set_state(self.name, DROP_RATE_SETTING, self.current_drop_rate)
    
    def save_settings(self):
        for setting in self.settings:
            if setting.name == DROP_RATE_SETTING:
                original_drop_rate = setting.current_value
                selected_option = setting.current_value
                if selected_option == self.current_drop_rate:
                    continue  # No change, skip

                if not self.uninstall():
                    self._log(f"Failed to uninstall mod before changing drop rate to: {selected_option}", level="ERROR")
                    continue

                self.mod_file_path = Path(self.resource_folder) / "Drop Rates Enhanced" / selected_option
                self.current_drop_rate = selected_option
                if not self.install():
                    self._log(f"Failed to install mod after changing drop rate to: {selected_option}", level="ERROR")
                    self.mod_file_path = Path(self.resource_folder) / "Drop Rates Enhanced" / self.current_drop_rate  # Revert to previous path if installation fails
                    self.current_drop_rate = original_drop_rate  # Revert to previous drop rate if installation fails
                    continue

                self._log(f"Successfully changed drop rate to: {selected_option}")