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
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget


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
        icon_path = Path(__file__).resolve().parent.parent / "Images" / "AirplaneGameICO.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1024, 720)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AirplaneGame startet..."))
        layout.addWidget(QLabel("Dashboard, Control Panel und Status Panel werden initialisiert."))
        self.setLayout(layout)

    def show(self):
        """Zeigt das Hauptfenster an."""
        super().show()
