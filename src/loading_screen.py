"""
Ladebildschirm mit animiertem grünem Fortschrittsring.
"""

from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QIcon, QColor, QPainter, QBrush, QPen, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from .config import ICON_PATHS, IMAGES_DIR
from .i18n import Translator


class CircularProgressBar(QWidget):
    """Ein kreisförmiger Fortschrittsbalken."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0
        self._rotation = 0
        self.setMinimumSize(64, 64)
        self.setMaximumSize(64, 64)
        self.setStyleSheet("background-color: transparent;")

    def set_progress(self, value):
        """Setzt den Fortschrittwert (0-100)."""
        self._progress = max(0, min(100, value))
        self.update()

    def set_rotation(self, angle):
        """Setzt den Rotationswinkel."""
        self._rotation = angle % 360
        self.update()

    @pyqtProperty(int)
    def progress(self):
        """Fortschritt-Property."""
        return self._progress

    @progress.setter
    def progress(self, value):
        self.set_progress(value)

    @pyqtProperty(int)
    def rotation(self):
        """Rotations-Property."""
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self.set_rotation(value)

    def paintEvent(self, event):
        """Zeichnet den kreisförmigen Fortschrittsbalken."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        size = self.size()
        center_x = size.width() / 2
        center_y = size.height() / 2
        radius = min(center_x, center_y) - 6

        # Hintergrundkreis (durchgehend blau)
        painter.setBrush(QBrush(QColor(33, 150, 243, 255)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(center_x - radius), int(center_y - radius), int(radius * 2), int(radius * 2))

        # Fortschrittsring (hell/leuchtend)
        pen = QPen(QColor(120, 220, 255), 5, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Zeichne den Fortschrittsring
        start_angle = int(self._rotation * 16)  # 1/16 Grad für QPainter
        span_angle = int((self._progress / 100) * 360 * 16)

        painter.drawArc(
            int(center_x - radius),
            int(center_y - radius),
            int(radius * 2),
            int(radius * 2),
            start_angle,
            span_angle,
        )

        # Prozenttext in der Mitte
        text = f"{self._progress}%"
        painter.setPen(QPen(QColor(225, 245, 255)))
        painter.setFont(self.font())
        font_metrics = painter.fontMetrics()
        text_width = font_metrics.horizontalAdvance(text)
        text_height = font_metrics.height()
        painter.drawText(
            int(center_x - text_width / 2),
            int(center_y + text_height / 4),
            text,
        )

        painter.end()


class LoadingScreen(QWidget):
    """Ladebildschirm als Widget mit AirplaneGame.png Hintergrund."""

    def __init__(self, translator: 'Translator' = None, parent=None):
        super().__init__(parent)
        self.translator = translator or Translator()
        self.background_pixmap = None

        # Lade Hintergrundbild (case-insensitive fallback für Linux)
        airplane_candidates = [
            IMAGES_DIR / "AirplaneGame.png",
            IMAGES_DIR / "airplanegame.png",
            IMAGES_DIR / "AirplaneGameICO.png",
            IMAGES_DIR / "airplanegameico.png",
        ]
        for airplane_image in airplane_candidates:
            if airplane_image.exists():
                self.background_pixmap = QPixmap(str(airplane_image))
                break

        self.setStyleSheet("background-color: #1a1a1a;")

        # Layout für den Container
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addStretch()  # Inhalt nach oben drücken, Spinner unten

        # Untere Leiste: Spinner klein in der unteren rechten Ecke
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        corner = QVBoxLayout()
        corner.setSpacing(6)
        corner.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_label = QLabel(self.translator.t("loading_initial"))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.status_label.setStyleSheet(
            "color: #B3E5FC; font-size: 13px; font-weight: bold; background-color: transparent;"
        )
        corner.addWidget(self.status_label)

        self.progress_bar = CircularProgressBar()
        corner.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignRight)

        bottom_layout.addLayout(corner)
        layout.addLayout(bottom_layout)

        # Animationen
        self._setup_animations()

    def _setup_animations(self):
        """Stellt die Animationen auf."""
        # Rotations-Animation (kontinuierlich)
        self.rotation_animation = QPropertyAnimation(self.progress_bar, b"rotation")
        self.rotation_animation.setStartValue(0)
        self.rotation_animation.setEndValue(360)
        self.rotation_animation.setDuration(2000)
        self.rotation_animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.rotation_animation.finished.connect(lambda: self.rotation_animation.start())

        # Fortschritts-Animation
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"progress")
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(100)
        self.progress_animation.setDuration(3000)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Starte die Animationen
        self.rotation_animation.start()
        self.progress_animation.start()

    def paintEvent(self, event):
        """Zeichnet das Hintergrundbild."""
        painter = QPainter(self)
        
        # Zeichne Hintergrundfarbe
        painter.fillRect(self.rect(), QColor(26, 26, 26))
        
        # Zeichne Bild, falls vorhanden
        if self.background_pixmap is not None:
            scaled_pixmap = self.background_pixmap.scaledToHeight(
                self.height(), Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled_pixmap.width()) // 2
            painter.drawPixmap(x, 0, scaled_pixmap)
        
        painter.end()
        super().paintEvent(event)

    def set_progress(self, value):
        """Setzt den Fortschritt (0-100)."""
        self.progress_bar.set_progress(value)

    def set_status(self, text):
        """Setzt den Status-Text."""
        self.status_label.setText(text)

    def finish_loading(self):
        """Stoppt die Animationen und setzt auf 100%."""
        self.rotation_animation.stop()
        self.progress_animation.stop()
        self.progress_bar.set_progress(100)
        self.status_label.setText("")
