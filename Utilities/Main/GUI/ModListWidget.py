from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QScrollArea, QCheckBox
from PyQt6.QtCore import Qt
from Main.GUI.ModItemWidget import ModItemWidget
from Main.Mods.ModModel import ModModel


class ModListWidget(QWidget):
    def __init__(self, mods: list[ModModel], parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)

        # Add "Select All" checkbox
        

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        layout = QVBoxLayout(container)
        layout.setSpacing(4)

        checkbox_container = QWidget()
        container_layout = QHBoxLayout(checkbox_container)
        container_layout.setContentsMargins(5, 0, 0, 0)  # left, top, right, bottom
        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_changed)
        container_layout.addWidget(self.select_all_checkbox)
        layout.addWidget(checkbox_container)

        self.mods_item_widgets = []
        for mod in mods:
            item = ModItemWidget(mod)
            layout.addWidget(item)
            self.mods_item_widgets.append(item)

        layout.addStretch()

    def on_select_all_changed(self, state):
        checked = state == Qt.CheckState.Checked.value
        for item_widget in self.mods_item_widgets:
            item_widget.check_box.setChecked(checked)

    def refresh_statuses(self):
        for item_widget in self.mods_item_widgets:
            item_widget.update_status_label()