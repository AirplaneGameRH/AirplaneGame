"""
Startpunkt der Anwendung.

Dieses Modul ist zuständig für die Initialisierung des PyQt6-Fensters,
das Laden der Spielressourcen und das Starten der Hauptspiel-Logik.

Geplante Aufgaben:
- PyQt6-Anwendung und Hauptfenster einrichten
- UI-Manager und Game-Logic-Komponenten instanziieren
- Hauptaktualisierungsschleife starten
"""

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
import time
from .loading_screen import LoadingScreen
from .core import GameLogic, AirportRenderer, AssetManager
from .ui_manager import UIManager
from .config import ICON_PATHS


def main(app=None):
    """Erzeugt das Hauptfenster und gibt es zurück."""
    app = app or QApplication.instance() or QApplication([])
    
    try:
        # Speichere die Startzeit für die 5 Sekunden Ladebildschirm
        start_time = time.time()
        
        # Erstelle das Hauptfenster mit Ladebildschirm
        window = UIManager(None, None, None, loading_mode=True)  # Frameless mit Bildformat
        
        # Erstelle Ladebildschirm und setze ihn als zentrales Widget
        loading_screen = LoadingScreen()
        window.setCentralWidget(loading_screen)
        
        # Zeige das Fenster
        window.show()
        window.raise_()
        window.activateWindow()
        app.processEvents()
        
        # Lade Assets
        loading_screen.set_status("Lade Assets...")
        loading_screen.set_progress(10)
        app.processEvents()
        assets = AssetManager()
        
        # Initialisiere Renderer
        loading_screen.set_status("Initialisiere Renderer...")
        loading_screen.set_progress(40)
        app.processEvents()
        renderer = AirportRenderer()
        
        # Initialisiere Spiel-Logik
        loading_screen.set_status("Starte Spiel-Logik...")
        loading_screen.set_progress(70)
        app.processEvents()
        game = GameLogic()
        
        # Speichere die echten Komponenten
        window.game_logic = game
        window.renderer = renderer
        window.assets = assets
        
        # Fertig!
        loading_screen.set_progress(100)
        loading_screen.set_status("Fertig!")
        app.processEvents()
        
        def show_main_ui():
            """Zeige den echten UI nach 5 Sekunden im Fullscreen."""
            elapsed = time.time() - start_time
            if elapsed < 5.0:
                return True  # Weiter warten
            
            # Stoppe den Timer
            timer.stop()
            
            # Wechsle zu Fullscreen mit Fensterleiste
            window.set_fullscreen()
            
            # Erstelle ein leeres UI Widget (echte Widgets können später hinzugefügt werden)
            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)
            status = QLabel("Spiel wird geladen...")
            layout.addWidget(status)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Ersetze den Ladebildschirm mit dem echten UI
            window.setCentralWidget(central_widget)
            
            return False  # Timer stoppen
        
        # Starte Timer, um nach 5 Sekunden den echten UI zu zeigen
        timer = QTimer()
        timer.timeout.connect(show_main_ui)
        timer.start(100)  # Checke alle 100ms
        
        return window
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        import traceback
        traceback.print_exc()
        raise





