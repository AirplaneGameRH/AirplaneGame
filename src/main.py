"""
Startpunkt der Anwendung.

Dieses Modul ist zuständig für die Initialisierung des PyQt6-Fensters,
das Laden der Spielressourcen und das Starten der Hauptspiel-Logik.
"""

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedLayout,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QGraphicsBlurEffect,
)
import time
from .i18n import Translator
from .loading_screen import LoadingScreen
from .menu_screen import MenuScreen, SettingsScreen
from .core import GameLogic, AirportRenderer, AssetManager
from .ui_manager import UIManager, BackgroundWidget
from .audio_manager import BackgroundMusic


def main(app=None):
    """Erzeugt das Hauptfenster und gibt es zurück."""
    app = app or QApplication.instance() or QApplication([])
    translator = Translator()

    try:
        start_time = time.time()
        # Erstelle UIManager im Loading-Modus (ohne GameLogic/Renderer/Assets)
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
        game.start_game()

        window.game_logic = game
        window.renderer = renderer
        window.assets = assets

        loading_screen.set_progress(100)
        loading_screen.set_status("")
        app.processEvents()

        def show_main_ui():
            elapsed = time.time() - start_time
            if elapsed < 5.0:
                return True

            timer.stop()
            window.set_fullscreen()

            # UI-Komponenten erstellen (nutzt die bereits initialisierten game_logic, renderer, assets)
            if window.dashboard is None:
                from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget
                window.dashboard = DashboardWidget()
                window.control_panel = ControlPanelWidget()
                window.status_panel = StatusPanelWidget()

            # Erstelle BackgroundWidget mit Wallpaper
            bg_widget = BackgroundWidget()

            # Inhaltsebene (Menü, Einstellungen, Quit-Button) als transparentes Overlay
            content_widget = QWidget()
            content_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)

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

            def apply_volumes() -> None:
                master = window.settings_screen.master_volume / 100.0
                music = window.settings_screen.music_volume / 100.0
                if window.background_music is not None:
                    window.background_music.set_volume(master * music)

            window.settings_screen.master_slider.valueChanged.connect(
                lambda v: (setattr(window.settings_screen, "master_volume", v), apply_volumes())
            )
            window.settings_screen.music_slider.valueChanged.connect(
                lambda v: (setattr(window.settings_screen, "music_volume", v), apply_volumes())
            )

            window.stack = QStackedLayout()
            content_layout.addLayout(window.stack, 1)  # stretch=1: nimmt ganzen verfügbaren Platz
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
            content_layout.addLayout(quit_layout, 0)  # stretch=0: nimmt minimal Platz

            # UI-Komponenten zum Stack hinzufügen (als Game-Screen)
            window.game_screen = QWidget()
            game_layout = QVBoxLayout(window.game_screen)
            game_layout.setContentsMargins(20, 20, 20, 20)
            game_layout.addWidget(window.dashboard)
            game_layout.addWidget(window.control_panel)
            game_layout.addWidget(window.status_panel)
            window.stack.addWidget(window.game_screen)

            # Hintergrund und Inhalt überlagern (beide füllen den Bildschirm)
            central = QWidget()
            grid = QGridLayout(central)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(0)
            grid.addWidget(bg_widget, 0, 0)
            grid.addWidget(content_widget, 0, 0)

            window.bg_widget = bg_widget

            window.setCentralWidget(central)
            window.stack.setCurrentWidget(window.menu_screen)

            # Starte die Hintergrundmusik in Dauerschleife
            window.background_music = BackgroundMusic(volume=0.3)
            window.background_music.play()
            window.settings_screen.master_volume = 100
            window.settings_screen.music_volume = 30
            window.settings_screen.master_slider.setValue(100)
            window.settings_screen.music_slider.setValue(30)

            # Starte Game Loop Timer
            window.game_timer = QTimer()
            window.game_timer.timeout.connect(lambda: game_loop(window))
            window.game_timer.start(100)  # 10 FPS

            return False

        def game_loop(window_obj: UIManager) -> None:
            """Hauptspielschleife - wird alle 100ms aufgerufen."""
            if window_obj.game_logic and window_obj.game_logic.running:
                window_obj.game_logic.update(0.1)
                state = window_obj.game_logic.get_game_state()
                
                # Update Dashboard
                if window_obj.dashboard:
                    window_obj.dashboard.update_stats(
                        money=state["money"],
                        reputation=state["reputation"],
                        aircraft_count=state["aircraft_count"],
                        active_flights=state["active_flights"],
                        fuel_percent=100.0  # TODO: proper fuel tracking
                    )
                
                # Update Renderer
                if window_obj.renderer:
                    window_obj.renderer.set_airport(window_obj.game_logic.airport)
                    window_obj.renderer.set_aircraft(window_obj.game_logic.aircraft)
                    window_obj.renderer.set_flights(window_obj.game_logic.flights)
                    window_obj.renderer.update_display()
                
                # Update Status Panel
                if window_obj.status_panel:
                    for flight in window_obj.game_logic.flights:
                        if flight.status == "in_progress":
                            window_obj.status_panel.add_flight(
                                flight.flight_number, 
                                flight.status, 
                                getattr(flight, 'progress', 0.0)
                            )

        def show_menu() -> None:
            window.menu_screen.update_translations()
            window.bg_widget.setGraphicsEffect(None)
            window.stack.setCurrentWidget(window.menu_screen)

        def show_settings() -> None:
            window.settings_screen.update_translations()
            blur = QGraphicsBlurEffect()
            blur.setBlurRadius(18)
            window.bg_widget.setGraphicsEffect(blur)
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




