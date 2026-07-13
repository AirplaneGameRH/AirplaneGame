"""Hauptmenü und Einstellungen für das AirportGame."""

from PyQt6.QtCore import Qt, QTimer
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
from .settings import get_settings


class MenuScreen(QWidget):
    """Zeigt das Hauptmenü mit New Game, Load Game und Settings."""

    def __init__(self, translator: Translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self._create_ui()
        self.translator.language_changed.connect(self.update_translations)

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)

        self.title_label = QLabel(self.translator.t("main_menu_title"))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.title_label)

        self.instruction_label = QLabel(self.translator.t("menu_instruction"))
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.instruction_label.setStyleSheet("font-size: 16px; color: #cccccc;")
        layout.addWidget(self.instruction_label)

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
        self.title_label.setText(self.translator.t("main_menu_title"))
        self.instruction_label.setText(self.translator.t("menu_instruction"))
        self.new_game_button.setText(self.translator.t("new_game"))
        self.load_game_button.setText(self.translator.t("load_game"))
        self.settings_button.setText(self.translator.t("settings"))


class SettingsScreen(QWidget):
    """Einstellungen mit Sprachauswahl und Audio-Reglern."""

    def __init__(self, translator: Translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        settings = get_settings()
        self.master_volume = settings.get("master_volume", 100)
        self.music_volume = settings.get("music_volume", 30)
        self._translation_pending = False
        self._signal_connected = False
        self._create_ui()

    def _create_ui(self) -> None:
        self.setStyleSheet("background-color: rgba(18, 18, 18, 0.88);")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        self.title_label = QLabel(self.translator.t("settings_title"))
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            "QTabWidget::pane { background-color: #1e1e1e; border-radius: 8px; }"
            "QTabWidget { font-size: 18px; }"
            "QTabBar::tab { background-color: #2d2d2d; color: white; padding: 12px 26px; font-size: 18px; border-top-left-radius: 8px; border-top-right-radius: 8px; }"
            "QTabBar::tab:selected { background-color: #4CAF50; }"
        )
        layout.addWidget(self.tabs)

        self.general_tab = self._create_general_tab()
        self.audio_tab = self._create_audio_tab()
        
        self.tabs.addTab(self.general_tab, self.translator.t("settings_tab_general"))
        self.tabs.addTab(self.audio_tab, self.translator.t("settings_tab_audio"))

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

        self.language_label = QLabel(self.translator.t("language_label"))
        self.language_label.setStyleSheet("font-size: 20px; color: #ffffff;")
        tab_layout.addWidget(self.language_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.language_combo = QComboBox()
        self.language_combo.setMaximumWidth(300)
        self.language_combo.setStyleSheet(
            "QComboBox { background-color: #2d2d2d; color: white; border-radius: 6px; padding: 10px; font-size: 18px; }"
            "QComboBox QAbstractItemView { background-color: #2d2d2d; color: white; font-size: 18px; }"
        )
        tab_layout.addWidget(self.language_combo, alignment=Qt.AlignmentFlag.AlignLeft)

        self.translation_status = QLabel("")
        self.translation_status.setStyleSheet("font-size: 14px; color: #888; margin-top: 8px;")
        self.translation_status.hide()
        tab_layout.addWidget(self.translation_status, alignment=Qt.AlignmentFlag.AlignLeft)

        tab_layout.addStretch()
        self._populate_languages()
        
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
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
            current_lang = self.translator.language
            for code in self.translator.available_languages:
                name = self.translator.language_name(code)
                is_cached = self.translator.is_translation_ready(code)
                display_name = f"{name} {'✓' if is_cached else '⟳'}"
                self.language_combo.addItem(display_name, code)
            current_index = self.translator.available_languages.index(current_lang)
            self.language_combo.setCurrentIndex(current_index)
        finally:
            self.language_combo.blockSignals(False)

    def _on_language_changed(self, index: int) -> None:
        if index < 0:
            return

        lang_code = self.language_combo.itemData(index)
        if not lang_code or lang_code == self.translator.language:
            return

        self._translation_pending = True
        self.translation_status.setText(f"Lade {self.translator.language_name(lang_code)}...")
        self.translation_status.show()
        self.language_combo.setEnabled(False)

        if not self._signal_connected:
            self.translator.language_changed.connect(self._on_language_ready)
            self._signal_connected = True

        self.translator.set_language(lang_code)

    def _on_language_ready(self, lang_code: str) -> None:
        if not self._translation_pending:
            return

        self._translation_pending = False
        self.translation_status.setText(f"{self.translator.language_name(lang_code)} bereit")
        self.language_combo.setEnabled(True)

        # Zuerst Settings speichern, DANN UI aktualisieren
        self.apply_settings()
        self.update_translations()

        QTimer.singleShot(2000, self.translation_status.hide)

    def update_translations(self) -> None:
        self.title_label.setText(self.translator.t("settings_title"))
        self.tabs.setTabText(0, self.translator.t("settings_tab_general"))
        self.tabs.setTabText(1, self.translator.t("settings_tab_audio"))
        self.language_label.setText(self.translator.t("language_label"))
        self.master_label.setText(self.translator.t("master_volume"))
        self.music_label.setText(self.translator.t("music_volume"))
        self.back_button.setText(self.translator.t("back"))
        self._populate_languages()

    def apply_settings(self) -> None:
        settings = get_settings()
        settings.set("master_volume", self.master_slider.value())
        settings.set("music_volume", self.music_slider.value())
        # Sprache direkt vom Translator lesen, nicht aus Combo (die könnte resettet sein)
        settings.set("language", self.translator.language)
