"""
Dashboard-Widget für Spielstatistiken.

Dieses Widget zeigt Geld, Treibstoff, Flugzeuganzahl und andere Kennzahlen an.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardWidget(QWidget):
    """Repräsentiert das Statistik-Dashboard der Hauptansicht."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard"))
        self.setLayout(layout)
