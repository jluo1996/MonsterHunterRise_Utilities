from typing import Mapping
from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, QCheckBox, QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from Main.Mods.ModModel import ModModel


class SettingsDialog(QDialog):
    def __init__(self, mod : ModModel, parent: QWidget | None = None, title: str = "Settings"):
        super().__init__(parent)
        self.mod = mod
        self.setWindowTitle(title)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)  # helps avoid memory leaks

        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_save.clicked.connect(self.on_save)
        self.btn_cancel.clicked.connect(self.on_cancel)

        # Root layout
        root = QVBoxLayout()
        self.setLayout(root)

        # Settings form (inserted above buttons)
        self._settings_layout = QFormLayout()
        root.addLayout(self._settings_layout)

        # Build the dynamic settings UI
        self._editors: dict[str, QWidget] = {}
        self._build_settings_ui()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        root.addLayout(btn_row)

        self.setLayout(root)


    def _build_settings_ui(self):
        """
        Dynamically build the settings UI based on self.mod.settings.

        Rules:
        - bool  -> QCheckBox
        - str/int/float -> QLineEdit (with number validators for int/float)
        - list -> QComboBox (items from the list; selects first if there is no explicit current)

        Supports:
        - self.mod.settings as dict[name -> ModSetting] or list[ModSetting]
        - Uses ModSetting.description as tooltip on label/editor when available
        """
        # Clear existing rows (if this is ever re-built)
        while self._settings_layout.count():
            item = self._settings_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        self._editors.clear()

        settings = getattr(self.mod, "settings", None)
        if not settings:
            self._settings_layout.addRow(QLabel("No settings available"))
            return

        for setting in settings:
            # Defensive gets
            name = getattr(setting, "name", "Unnamed Setting")
            setting_type = getattr(setting, "setting_type", type(getattr(setting, "value", None)))
            value = getattr(setting, "value", None)
            desc = getattr(setting, "description", "") or ""

            label = QLabel(str(name))
            if desc:
                label.setToolTip(desc)

            editor = None

            # --- Bool -> QCheckBox
            if setting_type is bool or isinstance(value, bool):
                cb = QCheckBox()
                cb.setChecked(bool(value))
                if desc:
                    cb.setToolTip(desc)
                editor = cb

            # --- Number or string -> QLineEdit (with validators for numbers)
            elif setting_type in (int, float, str) or isinstance(value, (int, float, str)):
                le = QLineEdit()
                if value is not None:
                    le.setText(str(value))
                le.setClearButtonEnabled(True)

                if setting_type is int or isinstance(value, int):
                    le.setValidator(QIntValidator())
                    le.setPlaceholderText("Enter an integer")
                elif setting_type is float or isinstance(value, float):
                    dv = QDoubleValidator()
                    dv.setNotation(QDoubleValidator.Notation.StandardNotation)
                    le.setValidator(dv)
                    le.setPlaceholderText("Enter a number")
                else:
                    le.setPlaceholderText("Enter text")

                if desc:
                    le.setToolTip(desc)

                editor = le

            # --- List -> QComboBox (use items from list)
            elif (setting_type is list or isinstance(value, (list, tuple))) \
                 or (setting_type is dict or isinstance(value, Mapping)):
                combo = QComboBox()

                default_selection = getattr(setting, "current_value", None)

                # Handle list/tuple: add items directly
                if isinstance(value, (list, tuple)):
                    options = list(value)
                    for item in options:
                        combo.addItem(str(item), userData=item)

                    if options:
                        index = value.index(default_selection) if default_selection in value else 0
                        combo.setCurrentIndex(index)

                # Handle dict/mapping: show dict keys as names
                elif isinstance(value, Mapping):
                    keys = list(value.keys())
                    for k in keys:
                        combo.addItem(str(k), userData=value[k])

                    if keys:
                        index = keys.index(default_selection) if default_selection in keys else 0
                        combo.setCurrentIndex(index)

                if desc:
                    combo.setToolTip(desc)
                editor = combo



            # --- Fallback -> QLineEdit as string
            else:
                le = QLineEdit()
                if value is not None:
                    le.setText(str(value))
                le.setClearButtonEnabled(True)
                le.setPlaceholderText("Enter value")
                if desc:
                    le.setToolTip(desc)
                editor = le

            self._editors[str(name)] = editor
            self._settings_layout.addRow(label, editor)



    
    def on_save(self):
        """
        Read back widget values and write them into self.mod.settings (list[ModSetting]).
        - bool: checkbox.isChecked() -> value
        - int/float/str: lineedit.text() cast appropriately -> value
        - list/tuple: combo.currentText() -> value   (assumes 'value' holds the choices originally)
        """
        settings = getattr(self.mod, "settings", None)
        if not settings:
            self.accept()
            return

        for setting in settings:
            name = getattr(setting, "name", None)
            if not name:
                continue

            editor = self._editors.get(str(name))
            if editor is None:
                continue

            st = getattr(setting, "setting_type", type(getattr(setting, "value", None)))
            current_val = getattr(setting, "value", None)

            # --- Bool (QCheckBox)
            from PyQt6.QtWidgets import QCheckBox, QLineEdit, QComboBox
            if isinstance(editor, QCheckBox):
                setting.value = editor.isChecked()
                continue

            # --- Text/Number (QLineEdit)
            if isinstance(editor, QLineEdit):
                txt = editor.text()
                try:
                    if st is int or isinstance(current_val, int):
                        setting.value = int(txt) if txt.strip() else 0
                    elif st is float or isinstance(current_val, float):
                        setting.value = float(txt) if txt.strip() else 0.0
                    else:
                        setting.value = txt
                except ValueError:
                    pass
                continue

            # --- Choices (QComboBox) - list/tuple originally provided in value
            if isinstance(editor, QComboBox):
                selected_text = editor.currentText()
                setting.current_value = selected_text
                continue

        self.mod.save_settings()
        self.accept()


    def on_cancel(self):
        self.reject() 
