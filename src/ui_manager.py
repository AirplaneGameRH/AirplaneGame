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

from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget, QPushButton, QLabel
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


class BackgroundWidget(QWidget):
    """Widget mit Hintergrundbild."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_pixmap = None
        self.scaled_pixmap = None
        
        # Lade Wallpaper.png
        wallpaper_path = IMAGES_DIR / "Wallpaper.png"
        if wallpaper_path.exists():
            self.background_pixmap = QPixmap(str(wallpaper_path))

    def resizeEvent(self, event):
        """Skaliere das Hintergrundbild bei Größenänderung."""
        super().resizeEvent(event)
        if self.background_pixmap is not None:
            # Skaliere das Bild auf die Fensterbreite/höhe, zentriert
            screen_size = self.size()
            img_size = self.background_pixmap.size()
            
            # Berechne das Seitenverhältnis
            img_ratio = img_size.width() / img_size.height()
            screen_ratio = screen_size.width() / screen_size.height()
            
            if img_ratio > screen_ratio:
                # Bild ist breiter - skaliere auf Höhe
                new_height = screen_size.height()
                new_width = int(new_height * img_ratio)
            else:
                # Bild ist höher - skaliere auf Breite
                new_width = screen_size.width()
                new_height = int(new_width / img_ratio)
            
            self.scaled_pixmap = self.background_pixmap.scaled(
                new_width, new_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

    def paintEvent(self, event):
        """Zeichnet das Hintergrundbild."""
        painter = QPainter(self)
        
        # Zeichne dunklen Hintergrund
        painter.fillRect(self.rect(), Qt.GlobalColor.black)
        
        # Zeichne das zentrierte Bild
        if self.scaled_pixmap is not None:
            x = (self.width() - self.scaled_pixmap.width()) // 2
            y = (self.height() - self.scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, self.scaled_pixmap)
        
        painter.end()
        super().paintEvent(event)


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

            # Erstelle zentrales Widget mit Hintergrundbild
            bg_widget = BackgroundWidget()
            
            # Erstelle Overlay-Layout mit UI-Komponenten und Quit-Button
            main_layout = QVBoxLayout(bg_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
            # Oberer Bereich mit UI-Komponenten
            content_layout = QVBoxLayout()
            content_layout.addWidget(self.dashboard)
            content_layout.addWidget(self.control_panel)
            content_layout.addWidget(self.status_panel)
            main_layout.addLayout(content_layout)
            
            # Quit-Button unten rechts
            quit_button = QPushButton("Spiel schließen")
            quit_button.setMaximumWidth(200)
            quit_button.clicked.connect(self.close)
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
            
            bottom_layout = QVBoxLayout()
            bottom_layout.addStretch()
            bottom_layout.addWidget(quit_button)
            main_layout.addLayout(bottom_layout)
            
            self.setCentralWidget(bg_widget)

    def set_fullscreen(self):
        """Wechsle in den Fullscreen Mode mit Fensterleiste."""
        self.setWindowFlags(Qt.WindowType.Window)
        self.showFullScreen()

    def show(self):
        """Zeigt das Hauptfenster an."""
        super().show()
