from pathlib import Path
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt
import psutil
from Main.GUI.ModInstallUI import ModInstallUI
from Main.MainViewModel import MainViewModel

ICON_PATH = Path(__file__).resolve().parent / "Resources" / "AppIcon"
PICTURE_PATH = Path(__file__).resolve().parent / "Resources" / "Pictures"

GAME_EXE = "MonsterHunterRise.exe"   
def is_game_running():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == GAME_EXE.lower():
                return True
        except psutil.NoSuchProcess:
            pass
    return False

if __name__ == "__main__":
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

    if is_game_running():
        QMessageBox.critical(None, "Game Running", "Please close Monster Hunter Rise before using this utility.")
        sys.exit(0)

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    splash.finish(None)  # Close the splash screen

    main_gui = ModInstallUI(mod_vm)
    main_gui.show()
    main_gui.raise_()
    main_gui.activateWindow()

    sys.exit(app.exec())