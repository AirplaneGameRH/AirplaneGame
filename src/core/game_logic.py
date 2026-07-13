"""
Kernlogik des Spiels.

Dieses Modul enthält die wirtschaftlichen Regeln, das Flug-Management und die Idle-Mechaniken.
"""

from ..entities import Airport, Player, Flight, Aircraft
import time


class GameLogic:
    """Verwaltet den Spielzustand und die Spiellogik."""

    def __init__(self):
        self.player = Player(name="Spieler", money=100000.0, reputation=50.0)
        self.airport = Airport(name="Hauptflughafen", city="Berlin", gates=5, runways=2, hangars=3)
        self.flights = []
        self.aircraft = []
        self.last_update = time.time()
        self.running = False
        self.game_speed = 1.0

    def start_game(self) -> None:
        """Startet die Spiel-Logik."""
        self.running = True
        self.last_update = time.time()

    def stop_game(self) -> None:
        """Stoppt die Spiel-Logik."""
        self.running = False

    def update(self, delta_time: float = None) -> None:
        """Aktualisiert den Spielzustand."""
        if not self.running:
            return

        current_time = time.time()
        if delta_time is None:
            delta_time = (current_time - self.last_update) * self.game_speed
        self.last_update = current_time

        # Flugzeuge aktualisieren
        for aircraft in self.aircraft:
            aircraft.update()

        # Flüge aktualisieren
        for flight in self.flights:
            flight.update_progress()

        # Flughafen aktualisieren
        self.airport.update()

        # Einkommen generieren (idle mechanics)
        self._generate_passive_income(delta_time)

    def _generate_passive_income(self, delta_time: float) -> None:
        """Generiert passives Einkommen basierend auf Flotte und Reputation."""
        income_rate = len(self.aircraft) * 10.0 + self.player.reputation * 0.5
        self.player.add_money(income_rate * delta_time)

    def buy_aircraft(self, aircraft: Aircraft) -> bool:
        """Kauft ein Flugzeug für den Spieler."""
        if self.player.money >= aircraft.purchase_price:
            self.player.spend_money(aircraft.purchase_price)
            self.player.add_aircraft(aircraft)
            self.aircraft.append(aircraft)
            self.airport.add_aircraft(aircraft)
            return True
        return False

    def schedule_flight(self, flight: Flight) -> bool:
        """Plant einen Flug."""
        if flight.aircraft and flight.aircraft in self.aircraft:
            if flight.aircraft.status == "parked":
                flight.start()
                flight.aircraft.start_flight(flight.destination)
                self.flights.append(flight)
                self.airport.add_flight(flight)
                return True
        return False

    def get_game_state(self) -> dict:
        """Gibt den aktuellen Spielzustand zurück."""
        return {
            "money": self.player.money,
            "reputation": self.player.reputation,
            "aircraft_count": len(self.aircraft),
            "active_flights": len([f for f in self.flights if f.status == "in_progress"]),
            "airport_status": self.airport.status,
        }
