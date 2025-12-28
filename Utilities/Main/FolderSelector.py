from pathlib import Path
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QWidget


class FolderSelector(QWidget):
    folder_changed_signal = pyqtSignal(Path)

    def __init__(self, default_path=None, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Line edit to show the selected folder path
        self.path_edit = QLineEdit(default_path)
        self.path_edit.setPlaceholderText("Select a folder...")
        self.layout.addWidget(self.path_edit, stretch=1)
        self.path_edit.textChanged.connect(self._on_text_changed)

        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.browse_button)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder", str(Path(self.path_edit.text()).expanduser())
        )
        if folder:
            self.path_edit.setText(folder)

    def get_folder(self) -> Path | None:
        text = self.path_edit.text().strip()
        return Path(text) if text else None
    
    def _on_text_changed(self, text: str):
        if text:
            self.folder_changed_signal.emit(Path(text))