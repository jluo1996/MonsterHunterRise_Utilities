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

        self.mods_item_widgets = []
        for mod in mods:
            item = ModItemWidget(mod)
            layout.addWidget(item)
            self.mods_item_widgets.append(item)

        layout.addStretch()

    def refresh_statuses(self):
        for item_widget in self.mods_item_widgets:
            item_widget.update_status_label()