from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QMessageBox
from Main.MainViewModel import MainViewModel
from Main.GUI.ModListWidget import ModListWidget
from Main.GUI.FolderSelector import FolderSelector

class ModInstallUI(QWidget):
    def __init__(self, main_vm: MainViewModel, logger):
        super().__init__()
        
        self.main_vm = main_vm
        self.logger = logger
        main_layout = QVBoxLayout()

        self.file_selector = FolderSelector(self.logger, self.main_vm.game_install_path)
        self.file_selector.folder_changed_signal.connect(self._on_folder_changed)
        main_layout.addWidget(self.file_selector)
        
        mods = self.main_vm.get_mods()
        self.mod_list_widget = self._get_mod_list_widget(mods)
        main_layout.addWidget(self.mod_list_widget)

        button_layout = QHBoxLayout()
        install_button = QPushButton("Install Selected Mods")
        install_button.clicked.connect(self._install_selected_mods)
        button_layout.addWidget(install_button)
        uninstall_button = QPushButton("Uninstall Selected Mods")
        uninstall_button.clicked.connect(self._uninstall_selected_mods)
        button_layout.addWidget(uninstall_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def _get_mod_list_widget(self, mods):
        mod_list_widget = ModListWidget(mods, self.logger)
        return mod_list_widget
    
    def _install_selected_mods(self):
        self.logger.log("Install Selected Mods button clicked.", level="UI")
        if not self.main_vm.install_selected_mods():
            self._show_dialog("Installation Error", "One or more mods failed to install. Please check the logs for details.")
        self._refresh_mod_statuses()

    def _show_dialog(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def _uninstall_selected_mods(self):
        self.logger.log("Uninstall Selected Mods button clicked.", level="UI")
        self.main_vm.uninstall_selected_mods()
        self._refresh_mod_statuses()

    def _refresh_mod_statuses(self):
        self.mod_list_widget.refresh_statuses()

    def _on_folder_changed(self, folder_path):
        self.main_vm.update_game_install_path(folder_path)
        self._refresh_mod_statuses()

    def update_game_install_path(self, new_path):
        self.file_selector.update_path(new_path)
