from PyQt6.QtWidgets import (
    QCheckBox, QWidget, QHBoxLayout, QLabel, QPushButton, QStyle
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

from Main.Mods.ModModel import ModModel
from Main.Helpers.FileHelper import FileHelper
from Main.GUI.SettingsDialog import SettingsDialog

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
        self.info_icon.setCursor(Qt.CursorShape.ArrowCursor)
        layout.addWidget(self.info_icon)

        # Setting button (only enabled if mod has settings)
        has_settings = self.mod.get_has_settings()
        self.settings_button = QPushButton()
        self.settings_button.setEnabled(has_settings)
        self.settings_button.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.06);
                    border-radius: 2px;
                }
            """)
        file_helper = FileHelper()
        settings_icon = QIcon(str(file_helper.get_icons_folder_path() / "Setting.png"))
        if has_settings:
            self.settings_button.setIcon(settings_icon)
            self.settings_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.settings_button.setToolTip(f"Configure settings for {self.mod.name}")
            self.settings_button.clicked.connect(lambda: self._settings_button_clicked(self.mod))
            self.settings_button.setFlat(True)
            self.settings_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        else:
            icon_px = self.settings_button.style().pixelMetric(
                QStyle.PixelMetric.PM_SmallIconSize, None, self.settings_button
                )
            icon_size = QSize(icon_px, icon_px)
            pm = QPixmap(icon_size)
            pm.fill(Qt.GlobalColor.transparent)
            self.settings_button.setIcon(QIcon(pm))  # Empty transparent icon to maintain layout
        layout.addWidget(self.settings_button)

    def update_status_label(self):
        """Update the status label text based on mod installation."""
        if self.mod.is_installed():
            self.status_label.setText("Installed")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("Not installed")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

    def _settings_button_clicked(self, mod: ModModel):
        settings_dialog = SettingsDialog(mod, parent=self)
        settings_dialog.exec()