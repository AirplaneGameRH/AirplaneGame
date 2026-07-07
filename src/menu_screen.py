"""Hauptmenü und Einstellungen für das AirportGame."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTabWidget,
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
    """Einstellungen mit Sprachauswahl und Audio-Reglern."""

    def __init__(self, translator: Translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self.master_volume = 100
        self.music_volume = 30
        self._create_ui()

    def _create_ui(self) -> None:
        self.setStyleSheet("background-color: rgba(18, 18, 18, 0.88);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        title = QLabel(self.translator.t("settings_title"))
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { background-color: #1e1e1e; border-radius: 8px; }"
            "QTabWidget { font-size: 18px; }"
            "QTabBar::tab { background-color: #2d2d2d; color: white; padding: 12px 26px; font-size: 18px; border-top-left-radius: 8px; border-top-right-radius: 8px; }"
            "QTabBar::tab:selected { background-color: #4CAF50; }"
        )
        layout.addWidget(self.tabs)

        self.tabs.addTab(self._create_general_tab(), self.translator.t("settings_tab_general"))
        self.tabs.addTab(self._create_audio_tab(), self.translator.t("settings_tab_audio"))

        layout.addStretch()

        self.back_button = QPushButton(self.translator.t("back"))
        self.back_button.setFixedSize(170, 52)
        self.back_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; border-radius: 10px; font-size: 18px; }"
            "QPushButton:hover { background-color: #45a049; }"
        )
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignLeft)

    def _create_general_tab(self) -> QWidget:
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        tab_layout.setSpacing(12)
        tab_layout.setContentsMargins(20, 20, 20, 20)

        language_label = QLabel(self.translator.t("language_label"))
        language_label.setStyleSheet("font-size: 20px; color: #ffffff;")
        tab_layout.addWidget(language_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.language_combo = QComboBox()
        self.language_combo.setMaximumWidth(300)
        self.language_combo.setStyleSheet(
            "QComboBox { background-color: #2d2d2d; color: white; border-radius: 6px; padding: 10px; font-size: 18px; }"
            "QComboBox QAbstractItemView { background-color: #2d2d2d; color: white; font-size: 18px; }"
        )
        tab_layout.addWidget(self.language_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        tab_layout.addStretch()
        self._populate_languages()
        return tab

    def _create_audio_tab(self) -> QWidget:
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        tab_layout.setSpacing(20)
        tab_layout.setContentsMargins(20, 20, 20, 20)

        self._audio_rows = []

        self.master_slider, self.master_value, master_row, self.master_label = self._create_volume_row(
            self.translator.t("master_volume")
        )
        self.music_slider, self.music_value, music_row, self.music_label = self._create_volume_row(
            self.translator.t("music_volume")
        )

        self._audio_rows = [master_row, music_row]

        self.master_slider.setValue(self.master_volume)
        self.music_slider.setValue(self.music_volume)

        tab_layout.addWidget(master_row)
        tab_layout.addWidget(music_row)
        tab_layout.addStretch()
        return tab

    def _create_volume_row(self, label_text: str):
        """Erstellt eine Zeile mit Beschriftung, Regler und Wertanzeige."""
        row = QWidget()
        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        header = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 20px; color: #ffffff;")
        value_label = QLabel("100%")
        value_label.setStyleSheet("font-size: 18px; color: #cccccc;")
        header.addWidget(label)
        header.addStretch()
        header.addWidget(value_label)
        row_layout.addLayout(header)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setStyleSheet(
            "QSlider::groove:horizontal { height: 8px; background: #555; border-radius: 4px; }"
            "QSlider::handle:horizontal { background: #4CAF50; width: 24px; margin: -8px 0; border-radius: 12px; }"
        )

        slider.valueChanged.connect(lambda v: value_label.setText(f"{v}%"))
        row_layout.addWidget(slider)
        return slider, value_label, row, label

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
        self.layout().itemAt(0).widget().setText(self.translator.t("settings_title"))
        self.tabs.setTabText(0, self.translator.t("settings_tab_general"))
        self.tabs.setTabText(1, self.translator.t("settings_tab_audio"))
        self.tabs.widget(0).layout().itemAt(0).widget().setText(self.translator.t("language_label"))
        self.master_label.setText(self.translator.t("master_volume"))
        self.music_label.setText(self.translator.t("music_volume"))
        self.back_button.setText(self.translator.t("back"))
        self._populate_languages()
