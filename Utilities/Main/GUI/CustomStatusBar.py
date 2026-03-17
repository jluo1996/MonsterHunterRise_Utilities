from PyQt6.QtWidgets import QStatusBar

class CustomStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: black;")  # Default color
        self.messageChanged.connect(lambda msg: self.setVisible(bool(msg)))  # Hide when no message

    def set_message_color(self, color):
        self.setStyleSheet(f"color: {color};")
    