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

from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget


def _apply_window_icon(widget):
    """Setzt das Fenstericon für das Hauptfenster und die Taskleiste."""
    icon_paths = (
        Path(__file__).resolve().parent.parent / "assets" / "images" / "AirplaneGameICO.ico",
        Path(__file__).resolve().parent.parent / "assets" / "images" / "AirplaneGameICO.png",
        Path(__file__).resolve().parent.parent / "assets" / "images" / "AirplaneGame.png",
    )
    for icon_path in icon_paths:
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                widget.setWindowIcon(icon)
                app = QApplication.instance()
                if app is not None:
                    app.setWindowIcon(icon)
                return


class UIManager(QWidget):
    """Verwaltet das Hauptfenster und die UI-Komponenten."""

    def __init__(self, game_logic, renderer, assets):
        super().__init__()
        self.game_logic = game_logic
        self.renderer = renderer
        self.assets = assets
        self.dashboard = DashboardWidget()
        self.control_panel = ControlPanelWidget()
        self.status_panel = StatusPanelWidget()

        self.setWindowTitle("AirplaneGame")
        _apply_window_icon(self)
        self.resize(1024, 720)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AirplaneGame startet..."))
        layout.addWidget(QLabel("Dashboard, Control Panel und Status Panel werden initialisiert."))
        self.setLayout(layout)

    def show(self):
        """Zeigt das Hauptfenster an."""
        super().show()
