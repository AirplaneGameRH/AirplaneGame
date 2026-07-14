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

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QMainWindow, QWidget, QPushButton, QLabel,
    QHBoxLayout, QSplitter, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt

from .config import ICON_PATHS, IMAGES_DIR
from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget
from .core import AirportRenderer


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
        
        # Lade Wallpaper.png (case-insensitive fallback für Linux)
        wallpaper_candidates = [
            IMAGES_DIR / "Wallpaper.png",
            IMAGES_DIR / "wallpaper.png",
            IMAGES_DIR / "Wallpaper.jpg",
            IMAGES_DIR / "wallpaper.jpg",
            IMAGES_DIR / "background.png",
            IMAGES_DIR / "Background.png",
        ]
        for wallpaper_path in wallpaper_candidates:
            if wallpaper_path.exists():
                self.background_pixmap = QPixmap(str(wallpaper_path))
                break

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


class GameScreenWidget(QWidget):
    """Hauptspielbildschirm mit Tower View (Renderer) und Control Panel unten."""
    
    def __init__(self, dashboard, control_panel, status_panel, renderer, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.control_panel = control_panel
        self.status_panel = status_panel
        self.renderer = renderer
        
        self.setStyleSheet("background-color: #1a1a2e;")
        self._setup_ui()
    
    def _setup_ui(self):
        """Erstellt das UI-Layout: Renderer in der Mitte, Controls unten."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Top Bar mit Dashboard
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)
        top_bar.addWidget(self.dashboard, stretch=1)
        top_bar.addWidget(self.status_panel, stretch=1)
        main_layout.addLayout(top_bar)
        
        # Mitte: Renderer (Tower View) - nimmt den meisten Platz ein
        # Wrap renderer in a styled frame
        renderer_frame = QFrame()
        renderer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        renderer_frame.setStyleSheet("""
            QFrame {
                background-color: #0d1b2a;
                border: 2px solid #1e3a5f;
                border-radius: 8px;
            }
        """)
        renderer_layout = QVBoxLayout(renderer_frame)
        renderer_layout.setContentsMargins(2, 2, 2, 2)
        renderer_layout.addWidget(self.renderer)
        main_layout.addWidget(renderer_frame, stretch=1)
        
        # Unten: Control Panel
        control_frame = QFrame()
        control_frame.setFrameShape(QFrame.Shape.StyledPanel)
        control_frame.setMaximumHeight(200)
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 2px solid #0f3460;
                border-radius: 8px;
            }
        """)
        control_layout = QVBoxLayout(control_frame)
        control_layout.setContentsMargins(15, 10, 15, 10)
        control_layout.addWidget(self.control_panel)
        main_layout.addWidget(control_frame)
        
        # Stretch ratios: top bar (small), renderer (large), controls (fixed)
        main_layout.setStretch(0, 0)  # top bar
        main_layout.setStretch(1, 1)  # renderer
        main_layout.setStretch(2, 0)  # controls


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
        self.game_screen = None

        self.setWindowTitle("AirportGame - Tower Control")
        _apply_window_icon(self)
        
        # Dark theme für die ganze App
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f1a;
            }
            QWidget {
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #1e3a5f;
                color: #e0e0e0;
                border: 1px solid #2d5a8a;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2d5a8a;
                border-color: #3d7ab8;
            }
            QPushButton:pressed {
                background-color: #162a4a;
            }
            QPushButton:disabled {
                background-color: #1a1a2e;
                color: #555;
                border-color: #333;
            }
            QLabel {
                color: #e0e0e0;
            }
            QProgressBar {
                border: 1px solid #2d5a8a;
                border-radius: 4px;
                background: #0d1b2a;
                height: 16px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00d4aa, stop:1 #00a8e8);
                border-radius: 3px;
            }
            QComboBox {
                background-color: #16213e;
                color: #e0e0e0;
                border: 1px solid #2d5a8a;
                padding: 5px 10px;
                border-radius: 4px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #3d7ab8;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #16213e;
                color: #e0e0e0;
                selection-background-color: #1e3a5f;
                border: 1px solid #2d5a8a;
            }
            QDialog {
                background-color: #16213e;
            }
            QMessageBox {
                background-color: #16213e;
            }
            QScrollBar:vertical {
                background: #0d1b2a;
                width: 10px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #2d5a8a;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3d7ab8;
            }
        """)
        
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
            self.resize(1280, 800)
        
        # Wenn Komponenten vorhanden sind, erstelle das UI
        if game_logic is not None and renderer is not None and assets is not None:
            self._create_game_ui()

    def _create_game_ui(self):
        """Erstellt das vollständige Spiel-UI."""
        self.dashboard = DashboardWidget()
        self.control_panel = ControlPanelWidget()
        self.status_panel = StatusPanelWidget()
        
        # Game Screen mit Renderer und Controls
        self.game_screen = GameScreenWidget(
            self.dashboard, self.control_panel, self.status_panel, self.renderer
        )
        
        # Hintergrund mit Overlay
        bg_widget = BackgroundWidget()
        main_layout = QVBoxLayout(bg_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.game_screen)
        
        self.setCentralWidget(bg_widget)

    def set_fullscreen(self):
        """Wechsle in den Fullscreen Mode mit Fensterleiste."""
        self.setWindowFlags(Qt.WindowType.Window)
        self.showFullScreen()

    def show(self):
        """Zeigt das Hauptfenster an."""
        super().show()
