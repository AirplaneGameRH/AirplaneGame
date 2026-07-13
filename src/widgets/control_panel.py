"""
Control-Panel-Widget für Spielaktionen.

Dieses Widget enthält Buttons und Eingabefelder für Kaufen, Reparieren,
Werbung und Flugplanung.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class ControlPanelWidget(QWidget):
    """Repräsentiert das Aktionspanel der Spieloberfläche."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("🎮 Steuerung")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Buttons für Aktionen
        self.buy_aircraft_btn = QPushButton("🛒 Flugzeug kaufen")
        self.repair_btn = QPushButton("🔧 Warten/Reparieren")
        self.advertise_btn = QPushButton("📢 Werbung schalten")
        self.refuel_btn = QPushButton("⛽ Betanken")
        self.schedule_flight_btn = QPushButton("📅 Flug planen")

        for btn in (self.buy_aircraft_btn, self.repair_btn, self.advertise_btn, 
                    self.refuel_btn, self.schedule_flight_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976d2;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """)
            layout.addWidget(btn)

        layout.addStretch()
