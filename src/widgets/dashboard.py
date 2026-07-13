"""
Dashboard-Widget für Spielstatistiken.

Dieses Widget zeigt Geld, Treibstoff, Flugzeuganzahl und andere Kennzahlen an.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt


class DashboardWidget(QWidget):
    """Repräsentiert das Statistik-Dashboard der Hauptansicht."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 8px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Titel
        title = QLabel("📊 Dashboard")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Geld
        money_layout = QHBoxLayout()
        self.money_label = QLabel("💰 Geld: $0")
        self.money_label.setStyleSheet("color: #4caf50; font-size: 14px; font-weight: bold;")
        money_layout.addWidget(self.money_label)
        money_layout.addStretch()
        layout.addLayout(money_layout)

        # Reputation
        rep_layout = QHBoxLayout()
        self.rep_label = QLabel("⭐ Reputation: 0")
        self.rep_label.setStyleSheet("color: #ffd54f; font-size: 14px;")
        rep_layout.addWidget(self.rep_label)
        rep_layout.addStretch()
        layout.addLayout(rep_layout)

        # Flugzeuganzahl
        aircraft_layout = QHBoxLayout()
        self.aircraft_label = QLabel("✈️ Flugzeuge: 0")
        self.aircraft_label.setStyleSheet("color: #64b5f6; font-size: 14px;")
        aircraft_layout.addWidget(self.aircraft_label)
        aircraft_layout.addStretch()
        layout.addLayout(aircraft_layout)

        # Aktive Flüge
        flights_layout = QHBoxLayout()
        self.flights_label = QLabel("🛫 Aktive Flüge: 0")
        self.flights_label.setStyleSheet("color: #e57373; font-size: 14px;")
        flights_layout.addWidget(self.flights_label)
        flights_layout.addStretch()
        layout.addLayout(flights_layout)

        # Fuel progress bar
        fuel_layout = QHBoxLayout()
        fuel_label = QLabel("⛽ Treibstoff:")
        fuel_label.setStyleSheet("color: #fff; font-size: 13px;")
        fuel_layout.addWidget(fuel_label)
        self.fuel_bar = QProgressBar()
        self.fuel_bar.setRange(0, 100)
        self.fuel_bar.setValue(100)
        self.fuel_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 4px;
                background: #222;
                height: 16px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #ff9800;
                border-radius: 3px;
            }
        """)
        fuel_layout.addWidget(self.fuel_bar)
        layout.addLayout(fuel_layout)

        layout.addStretch()

    def update_stats(self, money: float, reputation: float, aircraft_count: int, 
                     active_flights: int, fuel_percent: float = 100.0) -> None:
        """Aktualisiert die angezeigten Statistiken."""
        self.money_label.setText(f"💰 Geld: ${money:,.0f}")
        self.rep_label.setText(f"⭐ Reputation: {reputation:.1f}")
        self.aircraft_label.setText(f"✈️ Flugzeuge: {aircraft_count}")
        self.flights_label.setText(f"🛫 Aktive Flüge: {active_flights}")
        self.fuel_bar.setValue(int(fuel_percent))
