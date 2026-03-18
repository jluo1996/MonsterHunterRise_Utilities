from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap, QFont
from PyQt6.QtWidgets import QSplashScreen


class LoadingSplashScreen(QSplashScreen):
    def __init__(self, background_file_path: str | None = None):
        if background_file_path:
            pixmap = QPixmap(str(background_file_path))
            if pixmap.isNull():
                pixmap = QPixmap(600, 300)
                pixmap.fill(QColor("black"))
        else:
            pixmap = QPixmap(600, 300)
            pixmap.fill(QColor("black"))

        super().__init__(pixmap)

        self._font = QFont("Arial", 12)
        self._bottom_margin = 20
        self._text = ""
        self._align = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        self._color = QColor("white")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def drawContents(self, painter: QPainter):
        painter.save()
        painter.setFont(self._font)
        painter.setPen(self._color)

        rect = self.rect()
        rect.adjust(0, 0, 0, -self._bottom_margin)
        painter.drawText(rect, self._align, self._text)
        painter.restore()

    def showMessage(self, message: str, align: Qt.AlignmentFlag | None = None, color: QColor | None = None):
        self._text = message or ""
        if align is not None:
            self._align = align
        if color is not None:
            self._color = color
        self.update()

    def clearMessage(self):
        self._text = ""
        self.update()

    def mousePressEvent(self, event):
        # Ignore clicks so it doesn't close
        event.ignore()