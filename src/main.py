"""
Startpunkt der Anwendung.

Dieses Modul ist zuständig für die Initialisierung des PyQt6-Fensters,
das Laden der Spielressourcen und das Starten der Hauptspiel-Logik.
"""

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedLayout, QPushButton, QHBoxLayout
import time
from .i18n import Translator
from .loading_screen import LoadingScreen
from .menu_screen import MenuScreen, SettingsScreen
from .core import GameLogic, AirportRenderer, AssetManager
from .ui_manager import UIManager, BackgroundWidget

def main(app=None):
    """Erzeugt das Hauptfenster und gibt es zurück."""
    app = app or QApplication.instance() or QApplication([])
    translator = Translator()

    try:
        start_time = time.time()
        window = UIManager(None, None, None, loading_mode=True)
        window.translator = translator

        loading_screen = LoadingScreen(translator)
        window.setCentralWidget(loading_screen)

        window.show()
        window.raise_()
        window.activateWindow()
        app.processEvents()

        loading_screen.set_status(translator.t("loading_assets"))
        loading_screen.set_progress(10)
        app.processEvents()
        assets = AssetManager()

        loading_screen.set_status(translator.t("initializing_renderer"))
        loading_screen.set_progress(40)
        app.processEvents()
        renderer = AirportRenderer()

        loading_screen.set_status(translator.t("starting_logic"))
        loading_screen.set_progress(70)
        app.processEvents()
        game = GameLogic()

        window.game_logic = game
        window.renderer = renderer
        window.assets = assets

        loading_screen.set_progress(100)
        loading_screen.set_status(translator.t("finished"))
        app.processEvents()

        def show_main_ui():
            elapsed = time.time() - start_time
            if elapsed < 5.0:
                return True

            timer.stop()
            window.set_fullscreen()

            # Erstelle BackgroundWidget mit Wallpaper
            bg_widget = BackgroundWidget()
            bg_layout = QVBoxLayout(bg_widget)
            bg_layout.setContentsMargins(0, 0, 0, 0)

            window.menu_screen = MenuScreen(translator, parent=window)
            window.settings_screen = SettingsScreen(translator, parent=window)
            window.menu_screen.new_game_button.clicked.connect(
                lambda: show_placeholder(window, translator.t("game_placeholder_new"))
            )
            window.menu_screen.load_game_button.clicked.connect(
                lambda: show_placeholder(window, translator.t("game_placeholder_load"))
            )
            window.menu_screen.settings_button.clicked.connect(lambda: show_settings())
            window.settings_screen.back_button.clicked.connect(lambda: show_menu())
            window.settings_screen.language_combo.currentIndexChanged.connect(
                lambda _: language_changed()
            )

            window.stack = QStackedLayout()
            bg_layout.addLayout(window.stack, 1)  # stretch=1: nimmt ganzen verfügbaren Platz
            window.stack.addWidget(window.menu_screen)
            window.stack.addWidget(window.settings_screen)

            window.placeholder_screen = QWidget(parent=window)
            placeholder_layout = QVBoxLayout(window.placeholder_screen)
            placeholder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            window.placeholder_label = QLabel()
            window.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            window.placeholder_label.setStyleSheet("font-size: 20px; color: white; padding: 20px;")
            placeholder_layout.addWidget(window.placeholder_label)
            window.stack.addWidget(window.placeholder_screen)

            # Quit-Button am unteren Ende
            quit_layout = QHBoxLayout()
            quit_layout.addStretch()
            quit_button = QPushButton("Spiel schließen")
            quit_button.setMaximumWidth(200)
            quit_button.clicked.connect(window.close)
            quit_button.setStyleSheet("""
                QPushButton {
                    background-color: #d32f2f;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #b71c1c;
                }
            """)
            quit_layout.addWidget(quit_button)
            quit_layout.setContentsMargins(20, 0, 20, 20)
            bg_layout.addLayout(quit_layout, 0)  # stretch=0: nimmt minimal Platz

            window.setCentralWidget(bg_widget)
            window.stack.setCurrentWidget(window.menu_screen)
            return False

        def show_menu() -> None:
            window.menu_screen.update_translations()
            window.stack.setCurrentWidget(window.menu_screen)

        def show_settings() -> None:
            window.settings_screen.update_translations()
            window.stack.setCurrentWidget(window.settings_screen)

        def show_placeholder(window_obj: UIManager, text: str) -> None:
            window_obj.placeholder_label.setText(text)
            window_obj.stack.setCurrentWidget(window_obj.placeholder_screen)

        def language_changed() -> None:
            language_code = window.settings_screen.language_combo.currentData()
            if language_code:
                translator.set_language(language_code)
                window.menu_screen.translator = translator
                window.settings_screen.translator = translator
                window.menu_screen.update_translations()
                window.settings_screen.update_translations()

        timer = QTimer()
        timer.timeout.connect(show_main_ui)
        timer.start(100)

        return window
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        import traceback

        traceback.print_exc()
        raise





