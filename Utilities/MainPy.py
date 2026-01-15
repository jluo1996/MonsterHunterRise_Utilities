import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from Main.GUI.MainGUI import MainGUI
from Main.MainViewModel import MainViewModel


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show a splash screen
    splash_pixmap = QPixmap(200, 200)
    splash_pixmap.fill(Qt.GlobalColor.white)
    splash = QSplashScreen(splash_pixmap)
    splash.showMessage("Loading mods...", alignment=Qt.AlignmentFlag.AlignCenter, color=Qt.GlobalColor.black)
    splash.show()
    app.processEvents()

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    splash.finish(None)  # Close the splash screen

    main_gui = MainGUI(mod_vm)
    main_gui.show()

    sys.exit(app.exec())