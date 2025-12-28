import sys
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
from MainViewModel import MainViewModel
from ModListWidget import ModListWidget

class MainGUI(QWidget):
    def __init__(self, main_vm: MainViewModel):
        super().__init__()
        
        self.main_vm = main_vm
        main_layout = QVBoxLayout()
        
        mods = self.main_vm.get_mods()
        mod_list_widget = self.get_mod_list_widget(mods)
        main_layout.addWidget(mod_list_widget)

        button_layout = QHBoxLayout()
        install_button = QPushButton("Install Selected Mods")
        install_button.clicked.connect(self.main_vm.install_selected_mods)
        button_layout.addWidget(install_button)
        uninstall_button = QPushButton("Uninstall Selected Mods")
        uninstall_button.clicked.connect(self.main_vm.uninstall_selected_mods)
        button_layout.addWidget(uninstall_button)
        main_layout.addLayout(button_layout)
        

        self.setWindowTitle("MHR Utilities - Main GUI")
        self.setLayout(main_layout)

    def get_mod_list_widget(self, mods):
        mod_list_widget = ModListWidget(mods)
        return mod_list_widget



if __name__ == "__main__":
    app = QApplication(sys.argv)

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    main_gui = MainGUI(mod_vm)
    main_gui.show()

    sys.exit(app.exec())
