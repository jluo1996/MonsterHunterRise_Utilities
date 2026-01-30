from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction, QIcon
from Main.GUI.ModInstallUI import ModInstallUI
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper

class MainWindow(QMainWindow):
    def __init__(self, mod_vm, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MHR Utilities")

        self.main_gui = ModInstallUI(mod_vm)
        self.setCentralWidget(self.main_gui)

        # self.statusBar().showMessage("Ready")

        file_helper = FileHelper()
        self._build_menubar(file_helper)


    def _build_menubar(self, file_helper: FileHelper = FileHelper()):
        menubar = self.menuBar()

        # --- Options menu ---
        file_menu = menubar.addMenu("&Options")

        file_menu.addSeparator()

        act_exit = QAction("E&xit", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)
        file_menu.addAction(act_exit)

        # --- Edit / Tools ---
        tools_menu = menubar.addMenu("&Tools")

        backup_icon = QIcon(str(file_helper.get_icons_folder_path() / "App.ico"))  # TODO: add icon file
        act_backup = QAction(backup_icon, "&Backup User Data", self)
        act_backup.setShortcut("Ctrl+B")
        act_backup.triggered.connect(self._backup_user_data)
        tools_menu.addAction(act_backup)

        # --- Help menu (optional) ---
        help_menu = menubar.addMenu("&Help")

        act_about = QAction("&About", self)
        act_about.triggered.connect(self._show_about)
        help_menu.addAction(act_about)


    # ---- Handlers for toolbar actions ----

    def _show_about(self):
        pass

    def _backup_user_data(self):
        game_info_helper = GameInfoHelper()
        success = game_info_helper.backup_MHR_user_data()
        if success:
            print("Backup completed successfully.")
        else:
            print("Backup failed.")