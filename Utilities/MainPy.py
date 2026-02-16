from datetime import datetime
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt
from Main.MainViewModel import MainViewModel
from Main.GUI.MainWindow import MainWindow
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.Log.Logger import Logger

def _init_logger(self, file_helper: FileHelper = FileHelper()):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_folder = file_helper.get_log_folder_path()
    log_file_path = log_folder / f"MHR_Utilities_{timestamp}.log"
    return Logger(log_file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_helper = FileHelper()

    logger = _init_logger(file_helper)
    
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

    game_info_helper = GameInfoHelper()
    if game_info_helper.is_game_running():
        QMessageBox.critical(None, "Game Running", "Please close Monster Hunter Rise before using this utility.")
        sys.exit(0)

    mod_vm = MainViewModel()
    mod_vm.init_mods()

    splash.finish(None)  # Close the splash screen


    win = MainWindow(mod_vm)
    win.show()
    win.raise_()
    win.activateWindow()


    sys.exit(app.exec())