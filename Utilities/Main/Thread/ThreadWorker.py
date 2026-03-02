from PyQt6.QtCore import QThread, pyqtSignal

class ThreadWorker(QThread):
    finished = pyqtSignal(bool)  # emit True if successful, False if failed
    
    def set_function(self, func):
        self.func = func

    def run(self):
        try:
            if hasattr(self, 'func'):
                success = self.func()
        except Exception as e:
            print(f"Error occurred in ThreadWorker: {e}")
            success = False
        finally:
            self.finished.emit(success)
        