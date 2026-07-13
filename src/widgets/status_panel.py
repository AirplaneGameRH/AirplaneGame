"""
Status-Panel-Widget für Live-Informationen.

Dieses Widget zeigt laufende Flüge, Wartungsstatus und Flughafen-Events an.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt


class StatusPanelWidget(QWidget):
    """Repräsentiert ein Status-Panel für Live-Updates."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("📋 Live-Status")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Scrollbereich für Flüge/Events
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.content)

        layout.addWidget(self.scroll)

        self.flight_labels = []
        self.event_labels = []

    def add_flight(self, flight_number: str, status: str, progress: float = 0.0) -> None:
        """Fügt einen Flug zur Anzeige hinzu oder aktualisiert ihn."""
        label_text = f"{flight_number}: {status} ({progress:.0%})"
        if len(self.flight_labels) < len(self.content_layout.children()) - 1:
            self.flight_labels[len(self.flight_labels) - 1].setText(label_text)
        else:
            label = QLabel(label_text)
            label.setStyleSheet("color: #e0e0e0; font-size: 12px; padding: 2px;")
            self.content_layout.addWidget(label)
            self.flight_labels.append(label)

    def add_event(self, message: str) -> None:
        """Fügt ein Event/Log-Eintrag hinzu."""
        label = QLabel(f"📍 {message}")
        label.setStyleSheet("color: #ffd54f; font-size: 12px; padding: 2px;")
        self.content_layout.addWidget(label)
        self.event_labels.append(label)
        # Behalte nur die letzten 20 Events
        if len(self.event_labels) > 20:
            old = self.event_labels.pop(0)
            old.deleteLater()

    def clear_flights(self) -> None:
        """Löscht alle Fluganzeigen."""
        for label in self.flight_labels:
            label.deleteLater()
        self.flight_labels.clear()
