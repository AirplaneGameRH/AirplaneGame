"""
Startpunkt der Anwendung.

Dieses Modul ist zuständig für die Initialisierung des PyQt6-Fensters,
das Laden der Spielressourcen und das Starten der Hauptspiel-Logik.

Geplante Aufgaben:
- PyQt6-Anwendung und Hauptfenster einrichten
- UI-Manager und Game-Logic-Komponenten instanziieren
- Hauptaktualisierungsschleife starten
"""

from PyQt6.QtWidgets import QApplication
from .core import GameLogic, AirportRenderer, AssetManager
from .ui_manager import UIManager
from .entities import Player, Airport


def main(app=None):
    """Erzeugt das Hauptfenster und gibt es zurück."""
    app = app or QApplication.instance() or QApplication([])
    assets = AssetManager()
    renderer = AirportRenderer()
    game = GameLogic()
    ui = UIManager(game, renderer, assets)
    ui.show()
    ui.raise_()
    ui.activateWindow()
    return ui
