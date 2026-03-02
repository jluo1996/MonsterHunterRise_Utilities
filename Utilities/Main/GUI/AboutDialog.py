import sys
import win32api
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtWidgets

GITHUB_URL = "https://github.com/jluo1996/MonsterHunterRise_Utilities"

class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setFixedWidth(460)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("About This App")
        title_font = QtGui.QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)

        desc = QtWidgets.QLabel(
            "The source code for this application is available on GitHub.<br>"
            "You can also download the latest version there.<br><br>"
            "Visit the repository here:"
        )
        desc.setWordWrap(True)

        # No f-string; use format() to avoid brace issues
        link = QtWidgets.QLabel('<a href="{0}">{0}</a>'.format(GITHUB_URL))
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
            | Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
        link.setOpenExternalLinks(True)

        btns = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
        )
        btns.accepted.connect(self.accept)

        version_text = self._get_current_exe_version()
        version = QtWidgets.QLabel(f"Version: {version_text}")
        version_font = QtGui.QFont()
        version_font.setPointSize(9)
        version.setFont(version_font)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(link)
        layout.addStretch(1)
        layout.addWidget(version)
        layout.addWidget(btns)

    def _get_current_exe_version(self):
        exe_path = sys.executable 
        info = win32api.GetFileVersionInfo(exe_path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
        return version