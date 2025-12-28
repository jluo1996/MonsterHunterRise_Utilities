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


        # Info icon with tooltip
        self.info_icon = QLabel()
        icon = QIcon.fromTheme("help-about")
        self.info_icon.setPixmap(icon.pixmap(16, 16))
        self.info_icon.setToolTip(
            f"<b>{mod.name}</b><br/>{mod.description or 'No description available.'}"
        )
        self.info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)
        layout.addWidget(self.info_icon)

        # self.toggle_button.setStyleSheet("""
        # QPushButton {
        #     padding: 4px;
        # }
        # QPushButton:checked {
        #     background-color: #4CAF50;
        #     color: white;
        # }
        # """)


    # def on_toggled(self, checked: bool):
    #     self.toggle_button.setText("On" if checked else "Off")
