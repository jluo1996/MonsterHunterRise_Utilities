from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ModItemWidget import ModItemWidget
from ModModel import ModModel


class ModListWidget(QWidget):
    def __init__(self, mods: list[ModModel], parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setSpacing(4)

        for mod in mods:
            item = ModItemWidget(mod)
            layout.addWidget(item)

        layout.addStretch()
