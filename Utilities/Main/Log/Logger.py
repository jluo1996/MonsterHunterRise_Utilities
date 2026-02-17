from datetime import datetime 
import os
from pathlib import Path
import tempfile

from PyQt6.QtCore import QObject, pyqtSignal

from Main.Helpers.FileHelper import FileHelper 

# Singleton Logger class
class Logger(QObject):
    # Signal emitted when a new log message is written
    log_message_signal = pyqtSignal(str, str)  # (formatted_message, level)
    
    LEVELS = {
        "INFO": "[INFO]",
        "WARNING": "[WARNING]",
        "ERROR": "[ERROR]",
        "UI": "[UI]"
    }

    def __init__(self):
        super().__init__()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_helper = FileHelper()
        log_folder = file_helper.get_log_folder_path()
        log_file_path = log_folder / f"MHR_Utilities_{timestamp}.log"

        # Use system temp folder if no path is provided
        self.log_file_path = log_file_path or f"{tempfile.gettempdir()}/app.log"
        self._create_log_file(self.log_file_path)
        self.last_log = None
        
    def _create_log_file(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)  # make sure the folder exists
        path.touch(exist_ok=True)  # creates the file if it doesn't exist

    def open_log_file(self):
        try:
            if self.log_file_path.exists():
                os.startfile(str(self.log_file_path))  # Windows-specific way to open the file
            else:
                self.log("Log file does not exist.", level="ERROR")
        except Exception as e:
            self.log(f"Failed to open log file: {e}", level="ERROR")

    def log(self, message, level="INFO"):
        if level not in self.LEVELS:
            level = "INFO"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} {self.LEVELS[level]} {message}"
        print(formatted_message)  # Also print to console

        # Append to log file
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(formatted_message + "\n")
        self.last_log = formatted_message
        
        # Emit signal to notify clients of new log message
        self.log_message_signal.emit(formatted_message, level)

    def get_last_log(self):
        return self.last_log