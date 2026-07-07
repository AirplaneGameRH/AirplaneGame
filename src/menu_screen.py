"""Hauptmenü und Einstellungen für das AirportGame."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .i18n import Translator


class MenuScreen(QWidget):
    """Zeigt das Hauptmenü mit New Game, Load Game und Settings."""

    def __init__(self, translator: Translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(self.translator.t("main_menu_title"))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        instruction = QLabel(self.translator.t("menu_instruction"))
        instruction.setAlignment(Qt.AlignmentFlag.AlignLeft)
        instruction.setStyleSheet("font-size: 16px; color: #cccccc;")
        layout.addWidget(instruction)

        self.new_game_button = QPushButton(self.translator.t("new_game"))
        self.load_game_button = QPushButton(self.translator.t("load_game"))
        self.settings_button = QPushButton(self.translator.t("settings"))

        for button in (self.new_game_button, self.load_game_button, self.settings_button):
            button.setFixedSize(240, 52)
            button.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; border-radius: 10px; font-size: 16px; }"
                "QPushButton:hover { background-color: #45a049; }"
            )
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()

    def update_translations(self) -> None:
        self.layout().itemAt(0).widget().setText(self.translator.t("main_menu_title"))
        self.layout().itemAt(1).widget().setText(self.translator.t("menu_instruction"))
        self.new_game_button.setText(self.translator.t("new_game"))
        self.load_game_button.setText(self.translator.t("load_game"))
        self.settings_button.setText(self.translator.t("settings"))


class SettingsScreen(QWidget):
    """Einstellungen mit Sprachauswahl."""

    def __init__(self, translator: Translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        title = QLabel(self.translator.t("settings_title"))
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        language_label = QLabel(self.translator.t("language_label"))
        language_label.setStyleSheet("font-size: 18px; color: #ffffff;")
        layout.addWidget(language_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.language_combo = QComboBox()
        self.language_combo.setMaximumWidth(240)
        self.language_combo.setStyleSheet(
            "QComboBox { background-color: #2d2d2d; color: white; border-radius: 6px; padding: 8px; }"
            "QComboBox QAbstractItemView { background-color: #2d2d2d; color: white; }"
        )
        layout.addWidget(self.language_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()

        self.back_button = QPushButton(self.translator.t("back"))
        self.back_button.setFixedSize(140, 44)
        self.back_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border-radius: 10px; font-size: 16px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self._populate_languages()

    def _populate_languages(self) -> None:
        self.language_combo.blockSignals(True)
        try:
            self.language_combo.clear()
            for code in self.translator.available_languages():
                self.language_combo.addItem(self.translator.language_name(code), code)
            current_index = self.translator.available_languages().index(self.translator.language)
            self.language_combo.setCurrentIndex(current_index)
        finally:
            self.language_combo.blockSignals(False)

    def update_translations(self) -> None:
        self.layout().itemAtPosition(0, 0).widget().setText(self.translator.t("settings_title"))
        self.layout().itemAtPosition(1, 0).widget().setText(self.translator.t("language_label"))
        self.back_button.setText(self.translator.t("back"))
        self._populate_languages()
