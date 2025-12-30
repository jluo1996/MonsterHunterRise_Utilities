from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from Main.MainViewModel import MainViewModel
from Main.GUI.ModListWidget import ModListWidget
from Main.GUI.FolderSelector import FolderSelector

class MainGUI(QWidget):
    def __init__(self, main_vm: MainViewModel):
        super().__init__()
        
        self.main_vm = main_vm
        main_layout = QVBoxLayout()

        self.file_selector = FolderSelector(self.main_vm.game_install_path)
        self.file_selector.folder_changed_signal.connect(self.on_folder_changed)
        main_layout.addWidget(self.file_selector)
        
        mods = self.main_vm.get_mods()
        self.mod_list_widget = self.get_mod_list_widget(mods)
        main_layout.addWidget(self.mod_list_widget)

        button_layout = QHBoxLayout()
        install_button = QPushButton("Install Selected Mods")
        install_button.clicked.connect(self.install_selected_mods)
        button_layout.addWidget(install_button)
        uninstall_button = QPushButton("Uninstall Selected Mods")
        uninstall_button.clicked.connect(self.uninstall_selected_mods)
        button_layout.addWidget(uninstall_button)
        main_layout.addLayout(button_layout)
        
        self.setWindowTitle("MHR Utilities")
        self.setLayout(main_layout)

    def get_mod_list_widget(self, mods):
        mod_list_widget = ModListWidget(mods)
        return mod_list_widget
    
    def install_selected_mods(self):
        self.main_vm.install_selected_mods()
        self.refresh_mod_statuses()

    def uninstall_selected_mods(self):
        self.main_vm.uninstall_selected_mods()
        self.refresh_mod_statuses()

    def refresh_mod_statuses(self):
        self.mod_list_widget.refresh_statuses()

    def on_folder_changed(self, folder_path):
        self.main_vm.update_game_install_path(folder_path)
        self.refresh_mod_statuses()
