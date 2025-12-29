import sys
from PyQt6.QtWidgets import QApplication
from Main.GUI.MainGUI import MainGUI
from Main.MainViewModel import MainViewModel


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    main_gui = MainGUI(mod_vm)
    main_gui.show()

    sys.exit(app.exec())