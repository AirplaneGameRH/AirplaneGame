"""
Render-Logik für den Flughafen.

Dieses Modul ist verantwortlich für die grafische Darstellung des Flughafens
und der Flugzeuge im Tower-Livefenster.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ..entities import Airport, Aircraft


class AirportRenderer(QWidget):
    """Render-Komponente für Flughafen und Flugzeuge."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.airport = None
        self.aircraft_list = []
        self.flights = []
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 8px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.title = QLabel("🗼 Tower View - Flughafen")
        self.title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)

        self.runway_label = QLabel("Startbahnen: 0")
        self.runway_label.setStyleSheet("color: #bbb; font-size: 13px;")
        layout.addWidget(self.runway_label)

        self.gate_label = QLabel("Gates: 0")
        self.gate_label.setStyleSheet("color: #bbb; font-size: 13px;")
        layout.addWidget(self.gate_label)

        self.aircraft_list_label = QLabel("Flugzeuge am Boden: 0")
        self.aircraft_list_label.setStyleSheet("color: #bbb; font-size: 13px;")
        layout.addWidget(self.aircraft_list_label)

        self.flight_list_label = QLabel("Aktive Flüge: 0")
        self.flight_list_label.setStyleSheet("color: #bbb; font-size: 13px;")
        layout.addWidget(self.flight_list_label)

        layout.addStretch()

    def set_airport(self, airport: Airport) -> None:
        """Setzt den anzuzeigenden Flughafen."""
        self.airport = airport
        if airport:
            self.runway_label.setText(f"Startbahnen: {airport.runways}")
            self.gate_label.setText(f"Gates: {airport.gates} (Hangars: {airport.hangars})")

    def set_aircraft(self, aircraft_list: list) -> None:
        """Setzt die Liste der anzuzeigenden Flugzeuge."""
        self.aircraft_list = aircraft_list
        self.aircraft_list_label.setText(f"Flugzeuge am Boden: {len(aircraft_list)}")

    def set_flights(self, flights: list) -> None:
        """Setzt die Liste der aktiven Flüge."""
        self.flights = flights
        active = len([f for f in flights if getattr(f, 'status', '') == 'in_progress'])
        self.flight_list_label.setText(f"Aktive Flüge: {active}")

    def update_display(self) -> None:
        """Aktualisiert die Anzeige."""
        if self.airport:
            self.runway_label.setText(f"Startbahnen: {self.airport.runways}")
            self.gate_label.setText(f"Gates: {self.airport.gates} (Hangars: {self.airport.hangars})")
        self.aircraft_list_label.setText(f"Flugzeuge am Boden: {len(self.aircraft_list)}")
        active = len([f for f in self.flights if getattr(f, 'status', '') == 'in_progress'])
        self.flight_list_label.setText(f"Aktive Flüge: {active}")
