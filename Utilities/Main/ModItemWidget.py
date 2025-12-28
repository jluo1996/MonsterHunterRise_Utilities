from PyQt6.QtWidgets import (
    QCheckBox, QWidget, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from ModModel import ModModel

class ModItemWidget(QWidget):
    def __init__(self, mod : ModModel, parent=None):
        super().__init__(parent)
        self.mod = mod

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # Checkbox
        self.check_box = QCheckBox(self.mod.name)
        self.check_box.setCheckable(True)
        self.check_box.setChecked(self.mod.is_selected)
        self.check_box.stateChanged.connect(self.mod.set_selected)
        layout.addWidget(self.check_box, stretch=1)

        # Status label
        self.status_label = QLabel()
        self.update_status_label()
        layout.addWidget(self.status_label)

        # Info icon with tooltip
        self.info_icon = QLabel()
        icon = QIcon.fromTheme("help-about")
        self.info_icon.setPixmap(icon.pixmap(16, 16))
        self.info_icon.setToolTip(
            f"<b>{mod.name}</b><br/>{mod.description or 'No description available.'}"
        )
        self.info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)
        layout.addWidget(self.info_icon)

    def update_status_label(self):
        """Update the status label text based on mod installation."""
        if self.mod.is_installed():
            self.status_label.setText("Installed")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("Not installed")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
