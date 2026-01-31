from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction, QIcon
from Main.GUI.ModInstallUI import ModInstallUI
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper

class MainWindow(QMainWindow):
    def __init__(self, main_vm, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MHR Utilities")

        self.main_vm = main_vm
        self.main_gui = ModInstallUI(self.main_vm)
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

        auto_detect_icon = QIcon(str(file_helper.get_icons_folder_path() / "App.ico"))  # TODO: add icon file
        act_auto_detect = QAction(auto_detect_icon, "&Auto Detect Game Folder", self)
        act_auto_detect.setShortcut("Ctrl+D")
        act_auto_detect.triggered.connect(self._auto_detect_game_folder)
        tools_menu.addAction(act_auto_detect)

        # --- Help menu (optional) ---
        help_menu = menubar.addMenu("&Help")

        act_about = QAction("&About", self)
        act_about.triggered.connect(self._show_about)
        act_about.setShortcut("F1")
        help_menu.addAction(act_about)


    # ---- Handlers for toolbar actions ----

    def _show_about(self):
        # TODO: Implement about dialog
        pass

    def _backup_user_data(self):
        game_info_helper = GameInfoHelper()
        success = game_info_helper.backup_MHR_user_data()
        if success:
            print("Backup completed successfully.")
        else:
            print("Backup failed.")

    def _auto_detect_game_folder(self):
        self.main_vm.auto_detect_game_install_path(auto_detect=True, update_game_install_path=True)
        self.main_gui.update_game_install_path(self.main_vm.game_install_path)