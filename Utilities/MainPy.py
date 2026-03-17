import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt
from Main.Log.Logger import Logger

from Main.MainViewModel import MainViewModel
from Main.GUI.MainWindow import MainWindow
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper

if __name__ == "__main__":
    app = QApplication(sys.argv)

    logger = Logger()
    logger.log("Application initializing...", level="INFO")
    
    file_helper = FileHelper(logger)
    picture_path = file_helper.get_pictures_folder_path()
    icon_path = file_helper.get_icons_folder_path()

    # Set application icon
    app_icon = QIcon(str(icon_path / "App.png"))
    app.setWindowIcon(app_icon)
    
    # Create and show a splash screen with custom background
    splash_pixmap = QPixmap(str(picture_path / "splash_background.jpg"))  # Load custom image
    splash = QSplashScreen(splash_pixmap)
    splash.setFont(QFont("Arial", 16)) 
    splash.showMessage("Loading MHR Utilities...", alignment=Qt.AlignmentFlag.AlignCenter, color=Qt.GlobalColor.white)
    splash.show()
    app.processEvents()

    game_info_helper = GameInfoHelper(logger)
    if game_info_helper.is_game_running():
        logger.log("Game is currently running. Exiting application.", level="ERROR")
        QMessageBox.critical(None, "Game Running", "Please close Monster Hunter Rise before using this utility.")
        sys.exit(0)

    mod_vm = MainViewModel(logger)
    logger.log("Launching MainWindow...", level="INFO")
    win = MainWindow(mod_vm, logger)
    splash.finish(None)  # Close the splash screen
    win.show()
    win.raise_()
    win.activateWindow()
    logger.log("MainWindow launched successfully.", level="INFO")


    sys.exit(app.exec())