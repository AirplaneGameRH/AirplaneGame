"""
Benutzeroberfläche und Interaktion.

Dieses Modul verwaltet die PyQt6-Widgets, Layouts und Benutzerinteraktionen.
Es stellt die UI-Elemente für Statistiken, Buttons und Spielaktionen bereit.

Geplante Funktionen:
- Statistische Anzeige von Geld, Treibstoff, Flugzeugen
- Buttons für Kaufen, Reparieren, Werbung, Tankfüllung
- Verbindung der UI mit der Game-Logic
- Responsives Layout für unterschiedliche Fenstergrößen
"""

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from PyQt6.QtCore import Qt

from .config import ICON_PATHS, IMAGES_DIR
from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget


def _apply_window_icon(widget):
    """Setzt das Fenstericon für das Hauptfenster und die Taskleiste."""
    for icon_path in ICON_PATHS:
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                widget.setWindowIcon(icon)
                app = QApplication.instance()
                if app is not None:
                    app.setWindowIcon(icon)
                return


class UIManager(QMainWindow):
    """Verwaltet das Hauptfenster und die UI-Komponenten."""

    def __init__(self, game_logic, renderer, assets, loading_mode=False):
        super().__init__()
        self.game_logic = game_logic
        self.renderer = renderer
        self.assets = assets
        self.dashboard = None
        self.control_panel = None
        self.status_panel = None
        self.loading_mode = loading_mode

        self.setWindowTitle("AirplaneGame")
        _apply_window_icon(self)
        
        # Während des Ladescreen: Kleines Fenster in der Mitte
        if loading_mode:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.resize(500, 500)
            
            # Zentriere das Fenster auf dem Bildschirm
            from PyQt6.QtGui import QScreen
            screen = QApplication.primaryScreen()
            geometry = screen.geometry()
            x = (geometry.width() - 500) // 2
            y = (geometry.height() - 500) // 2
            self.move(x, y)
        else:
            # Normal Mode - wird später zum Fullscreen
            self.resize(1024, 720)
        
        # Wenn Komponenten vorhanden sind, erstelle das UI
        if game_logic is not None and renderer is not None and assets is not None:
            self.dashboard = DashboardWidget()
            self.control_panel = ControlPanelWidget()
            self.status_panel = StatusPanelWidget()

            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            layout.addWidget(self.dashboard)
            layout.addWidget(self.control_panel)
            layout.addWidget(self.status_panel)
            layout.setContentsMargins(0, 0, 0, 0)
            self.setCentralWidget(central_widget)

    def set_fullscreen(self):
        """Wechsle in den Fullscreen Mode mit Fensterleiste."""
        self.setWindowFlags(Qt.WindowType.Window)
        self.showFullScreen()

    def show(self):
        """Zeigt das Hauptfenster an."""
        super().show()
