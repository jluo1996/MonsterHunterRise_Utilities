from datetime import datetime 
from pathlib import Path
import tempfile

from Main.Helpers.FileHelper import FileHelper 

# Singleton Logger class
class Logger:
    _instance = None
    LEVELS = {
        "INFO": "[INFO]",
        "WARNING": "[WARNING]",
        "ERROR": "[ERROR]"
    }

    def __new__(cls, log_file_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file_path=None):
        if self._initialized:
            return
        self._initialized = True

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_helper = FileHelper()
        log_folder = file_helper.get_log_folder_path()
        log_file_path = log_folder / f"MHR_Utilities_{timestamp}.log"

        # Use system temp folder if no path is provided
        self.log_file_path = log_file_path or f"{tempfile.gettempdir()}/app.log"
        self._create_log_file(self.log_file_path)
        
    def _create_log_file(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)  # make sure the folder exists
        path.touch(exist_ok=True)  # creates the file if it doesn't exist


    def log(self, message, level="INFO"):
        if level not in self.LEVELS:
            level = "INFO"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"{timestamp} {self.LEVELS[level]} {message}"
        print(formatted_message)  # Also print to console

        # Append to log file
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(formatted_message + "\n")
