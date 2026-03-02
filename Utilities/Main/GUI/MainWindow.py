from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Main.GUI.AboutDialog import AboutDialog
from Main.GUI.ModInstallUI import ModInstallUI
from Main.GUI.UpdatingDialog import UpdatingDialog
from Main.Helpers.FileHelper import FileHelper
from Main.Helpers.GameInfoHelper import GameInfoHelper
from Main.MainViewModel import MainViewModel
from Main.Thread.ThreadWorker import ThreadWorker
from Main.Updater.Updater import Updater

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

        file_helper = FileHelper(self.logger)
        self._build_menubar(file_helper)

    def _build_menubar(self, file_helper: FileHelper):
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

        check_updates_icon = QIcon(str(file_helper.get_icons_folder_path() / "update.png"))
        act_check_updates = QAction(check_updates_icon, "Check for &Updates (beta)", self)
        act_check_updates.triggered.connect(self._check_for_updates) 
        act_check_updates.setShortcut("Ctrl+U")
        help_menu.addAction(act_check_updates)

        help_menu.addSeparator()

        about_icon = QIcon(str(file_helper.get_icons_folder_path() / "About.png"))
        act_about = QAction(about_icon, "&About", self)
        act_about.triggered.connect(self._show_about)
        act_about.setShortcut("F1")
        help_menu.addAction(act_about)


    # ---- Handlers for toolbar actions ----

    def _check_for_updates(self):
        self.logger.log("Check for updates menu item clicked.", level="UI") 

        updater = Updater()
        if not updater.has_newer_version():
            QMessageBox.information(self, "No Update Available", "You are already using the latest version of MHR Utilities.")
            self.logger.log("Checked for updates: already on the latest version.", level="INFO")
            return

        latest_version = updater.get_latest_version_number()
        result = QMessageBox.question(
            self,
            "Update Available",
            f"New version {latest_version} is available. Do you want to update?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if result != QMessageBox.StandardButton.Ok:
            self.logger.log("Update cancelled by user.", level="INFO")
            return
        
        self.logger.log(f"Starting update to version {latest_version}...", level="INFO")

        updating_dialog = UpdatingDialog(self)
        prepare_thread = ThreadWorker()
        prepare_thread.set_function(updater.prepare_to_update)
        prepare_thread.finished.connect(updating_dialog.accept)  # Close the dialog when preparation is done
        self.prepare_success = True
        prepare_thread.finished.connect(lambda success: setattr(self, 'prepare_success', success))
        prepare_thread.start()
        updating_dialog.exec()  # Show the dialog and wait until preparation is done

        if not self.prepare_success:
            QMessageBox.critical(self, "Update Failed", "An error occurred while preparing the update. Please check the log for details.")
            self.logger.log("Update preparation failed.", level="ERROR")
            return
        
        countdown_dialog = self._get_restart_countdown_dialog(countdown_seconds=5)
        result = countdown_dialog.exec()  # Show the countdown dialog and wait until it's done
        if result == QMessageBox.StandardButton.Cancel:
            self.logger.log("Update cancelled by user.", level="INFO")
            return
        
        updater.launch_update()



    def _get_restart_countdown_dialog(self, countdown_seconds):
        countdown = countdown_seconds
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Restarting Application")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel)
        msg_box.setWindowModality(Qt.WindowModality.ApplicationModal)
        msg_box.setText(f"The app will restart in {countdown_seconds} seconds...")

        timer = QTimer()
        def update_text():
            nonlocal countdown
            countdown -= 1
            if countdown <= 0:
                timer.stop()
                msg_box.accept()  # Close the dialog
            else:
                msg_box.setText(f"The app will restart in {countdown} seconds...")

        timer.timeout.connect(update_text)
        timer.start(1000)

        return msg_box

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
