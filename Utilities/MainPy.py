from pathlib import Path
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt
from Main.GUI.MainGUI import MainGUI
from Main.MainViewModel import MainViewModel

if __name__ == "__main__":
    ICON_PATH = Path(__file__).resolve().parent / "Resources" / "AppIcon"
    PICTURE_PATH = Path(__file__).resolve().parent / "Resources" / "Pictures"
    app = QApplication(sys.argv)

    # Set application icon
    app_icon = QIcon(str(ICON_PATH / "App.ico"))
    app.setWindowIcon(app_icon)

    # Create and show a splash screen with custom background
    splash_pixmap = QPixmap(str(PICTURE_PATH / "splash_background.jpg"))  # Load custom image
    splash = QSplashScreen(splash_pixmap)
    splash.setFont(QFont("Arial", 16)) 
    splash.showMessage("Loading MHR Utilities...", alignment=Qt.AlignmentFlag.AlignCenter, color=Qt.GlobalColor.white)
    splash.show()
    app.processEvents()

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    splash.finish(None)  # Close the splash screen

    main_gui = MainGUI(mod_vm)
    main_gui.show()
    main_gui.raise_()
    main_gui.activateWindow()

    sys.exit(app.exec())