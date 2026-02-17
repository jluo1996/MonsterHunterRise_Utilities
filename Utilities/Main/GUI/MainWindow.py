from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction, QIcon
from Main.GUI.ModInstallUI import ModInstallUI
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.GUI.AboutDialog import AboutDialog
from Main.MainViewModel import MainViewModel

class MainWindow(QMainWindow):
    def __init__(self, main_vm : MainViewModel, logger, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MHR Utilities")
        self.setMinimumWidth(330)
 
        self.main_vm = main_vm
        self.logger = logger
        
        self.main_gui = ModInstallUI(self.main_vm, self.logger)
        self.setCentralWidget(self.main_gui)

        self.logger.log_message_signal.connect(self._on_log_message_received)

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

        backup_icon = QIcon(str(file_helper.get_icons_folder_path() / "Backup.png"))
        act_backup = QAction(backup_icon, "&Backup User Data", self)
        act_backup.setShortcut("Ctrl+B")
        act_backup.triggered.connect(self._backup_user_data)
        tools_menu.addAction(act_backup)

        auto_detect_icon = QIcon(str(file_helper.get_icons_folder_path() / "Search.png")) 
        act_auto_detect = QAction(auto_detect_icon, "&Auto Detect Game Folder", self)
        act_auto_detect.setShortcut("Ctrl+D")
        act_auto_detect.triggered.connect(self._auto_detect_game_folder)
        tools_menu.addAction(act_auto_detect)

        # --- Help menu ---
        help_menu = menubar.addMenu("&Help")

        log_icon = QIcon(str(file_helper.get_icons_folder_path() / "Log.png"))  
        act_view_log = QAction(log_icon, "View &Log", self)
        act_view_log.triggered.connect(self._view_log)
        act_view_log.setShortcut("Ctrl+L")
        help_menu.addAction(act_view_log)

        help_menu.addSeparator()

        about_icon = QIcon(str(file_helper.get_icons_folder_path() / "About.png"))
        act_about = QAction(about_icon, "&About", self)
        act_about.triggered.connect(self._show_about)
        act_about.setShortcut("F1")
        help_menu.addAction(act_about)


    # ---- Handlers for toolbar actions ----

    def _show_about(self):
        self.logger.log("About menu item clicked.", level="UI")
        about_dialog = AboutDialog()
        about_dialog.exec() 

    def _backup_user_data(self):
        self.logger.log("Backup User Data menu item clicked.", level="UI")
        game_info_helper = GameInfoHelper(self.logger)
        success = game_info_helper.backup_MHR_user_data()
        if success:
            self.logger.log("Backup completed successfully.")
        else:
            self.logger.log("Backup failed.", level="ERROR")

    def _view_log(self):
        self.logger.log("View Log menu item clicked.", level="UI")
        self.logger.open_log_file()

    def _auto_detect_game_folder(self):
        self.logger.log("Auto Detect Game Folder menu item clicked.", level="UI")
        self.main_vm.auto_detect_game_install_path(auto_detect=True, update_game_install_path=True)
        self.main_gui.update_game_install_path(self.main_vm.game_install_path)

    def _on_log_message_received(self, formatted_message, level):
        levels = ["ERROR", "WARNING"]  # Define which levels should be shown in the status bar
        if level not in levels:
            self.statusBar().setVisible(False)  # Hide status bar for non-error/warning messages
            return  # Ignore messages that are not in the defined levels
        
        self.statusBar().showMessage(formatted_message)
        self.statusBar().setVisible(True)  # Ensure status bar is visible for relevant messages

        match level:
            case "ERROR":
                self.statusBar().setStyleSheet("color: red;")
            case "WARNING":
                self.statusBar().setStyleSheet("color: orange;")
            case "INFO":
                self.statusBar().setStyleSheet("color: grey;")
