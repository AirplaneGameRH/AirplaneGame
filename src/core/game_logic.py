"""
Kernlogik des Spiels.

Dieses Modul enthält die wirtschaftlichen Regeln, das Flug-Management und die Idle-Mechaniken.
"""

from ..entities import Airport, Player, Flight, Aircraft
from ..config import (
    STARTING_MONEY,
    STARTING_FUEL,
    DEFAULT_FUEL_CONSUMPTION,
    REPAIR_COST_PER_DAMAGE,
    AUTO_UPDATE_INTERVAL,
)
import time
import random
from typing import Dict, List, Optional, Callable, Any


class GameLogic:
    """Verwaltet den Spielzustand und die Spiellogik."""

    def __init__(self):
        self.player = Player(name="Spieler", money=STARTING_MONEY, reputation=50.0)
        self.airport = Airport(name="Hauptflughafen", city="Berlin", gates=5, runways=2, hangars=3)
        self.flights: List[Flight] = []
        self.aircraft: List[Aircraft] = []
        self.last_update = time.time()
        self.running = False
        self.game_speed = 1.0
        
        # Callbacks für UI-Updates
        self._on_state_changed: Optional[Callable[[Dict[str, Any]], None]] = None
        self._on_flight_completed: Optional[Callable[[Flight], None]] = None
        self._on_event: Optional[Callable[[str], None]] = None
        
        # Werbung
        self._advertising_multiplier = 1.0
        self._advertising_end_time: Optional[float] = None
        
        # Verfügbare Flugzeugtypen zum Kauf
        self.available_aircraft_types = self._init_aircraft_types()
        
        # Verfügbare Ziele
        self.available_destinations = self._init_destinations()

    def _init_aircraft_types(self) -> List[Dict[str, Any]]:
        """Initialisiert verfügbare Flugzeugtypen."""
        return [
            {
                "name": "Cessna 172",
                "model": "C172",
                "purchase_price": 150000,
                "max_fuel": 500,
                "passenger_capacity": 4,
                "cargo_capacity": 100,
                "speed": 200,
                "operating_cost": 50,
                "condition": 100.0,
            },
            {
                "name": "Airbus A320",
                "model": "A320",
                "purchase_price": 100000000,
                "max_fuel": 30000,
                "passenger_capacity": 180,
                "cargo_capacity": 20000,
                "speed": 850,
                "operating_cost": 5000,
                "condition": 100.0,
            },
            {
                "name": "Boeing 737",
                "model": "B737",
                "purchase_price": 120000000,
                "max_fuel": 35000,
                "passenger_capacity": 200,
                "cargo_capacity": 25000,
                "speed": 870,
                "operating_cost": 6000,
                "condition": 100.0,
            },
            {
                "name": "Airbus A380",
                "model": "A380",
                "purchase_price": 400000000,
                "max_fuel": 320000,
                "passenger_capacity": 550,
                "cargo_capacity": 150000,
                "speed": 900,
                "operating_cost": 20000,
                "condition": 100.0,
            },
        ]

    def _init_destinations(self) -> List[Dict[str, Any]]:
        """Initialisiert verfügbare Flugziele."""
        return [
            {"name": "München (MUC)", "city": "München", "distance": 500, "base_passengers": 100, "ticket_price": 150},
            {"name": "Hamburg (HAM)", "city": "Hamburg", "distance": 300, "base_passengers": 80, "ticket_price": 120},
            {"name": "Frankfurt (FRA)", "city": "Frankfurt", "distance": 550, "base_passengers": 150, "ticket_price": 200},
            {"name": "London (LHR)", "city": "London", "distance": 950, "base_passengers": 200, "ticket_price": 300},
            {"name": "Paris (CDG)", "city": "Paris", "distance": 900, "base_passengers": 180, "ticket_price": 280},
            {"name": "Madrid (MAD)", "city": "Madrid", "distance": 1800, "base_passengers": 150, "ticket_price": 350},
            {"name": "Rom (FCO)", "city": "Rom", "distance": 1200, "base_passengers": 120, "ticket_price": 300},
            {"name": "New York (JFK)", "city": "New York", "distance": 6400, "base_passengers": 250, "ticket_price": 800},
            {"name": "Dubai (DXB)", "city": "Dubai", "distance": 4500, "base_passengers": 200, "ticket_price": 600},
            {"name": "Tokyo (NRT)", "city": "Tokyo", "distance": 9000, "base_passengers": 180, "ticket_price": 1000},
        ]

    def set_callbacks(
        self,
        on_state_changed: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_flight_completed: Optional[Callable[[Flight], None]] = None,
        on_event: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Setzt Callbacks für UI-Updates."""
        self._on_state_changed = on_state_changed
        self._on_flight_completed = on_flight_completed
        self._on_event = on_event

    def _emit_event(self, message: str) -> None:
        """Sendet ein Event an das UI."""
        if self._on_event:
            self._on_event(message)

    def _notify_state_changed(self) -> None:
        """Benachrichtigt über Zustandsänderungen."""
        if self._on_state_changed:
            self._on_state_changed(self.get_game_state())

    def start_game(self) -> None:
        """Startet die Spiel-Logik."""
        self.running = True
        self.last_update = time.time()
        self._notify_state_changed()

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

        # Werbe-Timer prüfen
        if self._advertising_end_time and current_time >= self._advertising_end_time:
            self._advertising_multiplier = 1.0
            self._advertising_end_time = None
            self._emit_event("Werbung ist abgelaufen. Passagierzahlen normalisieren sich.")

        # Flugzeuge aktualisieren
        for aircraft in self.aircraft:
            aircraft.update()

        # Flüge aktualisieren
        completed_flights = []
        for flight in self.flights:
            if flight.status == "in_progress":
                flight.update_progress(delta_time)
                if flight.status == "completed":
                    completed_flights.append(flight)

        # Abgeschlossene Flüge verarbeiten
        for flight in completed_flights:
            self._complete_flight(flight)

        # Flughafen aktualisieren
        self.airport.update()

        # Einkommen generieren (idle mechanics)
        self._generate_passive_income(delta_time)

        self._notify_state_changed()

    def _generate_passive_income(self, delta_time: float) -> None:
        """Generiert passives Einkommen basierend auf Flotte und Reputation."""
        # Passives Einkommen: Reputation * Faktor + Anzahl Flugzeuge * Basis
        income_rate = self.player.reputation * 0.5 + len(self.aircraft) * 10.0
        self.player.add_money(income_rate * delta_time)

    def _complete_flight(self, flight: Flight) -> None:
        """Verarbeitet einen abgeschlossenen Flug: Einnahmen, Kosten, Reputation."""
        # Flugzeug landet
        if flight.aircraft:
            flight.aircraft.land()
        
        # Einnahmen berechnen
        revenue = flight.calculate_revenue()
        
        # Betriebskosten berechnen
        cost = flight.calculate_operating_cost()
        
        # Gewinn
        profit = revenue - cost
        
        # Spieler-Geld und Reputation aktualisieren
        self.player.add_money(profit)
        reputation_change = max(-5, min(10, profit / 10000))  # Reputation basierend auf Gewinn
        self.player.reputation = max(0, min(100, self.player.reputation + reputation_change))
        
        # Flugzeug-Kondition verschlechtern
        if flight.aircraft:
            condition_loss = flight.distance * 0.0001
            flight.aircraft.condition = max(0, flight.aircraft.condition - condition_loss)
            flight.aircraft.maintenance_level = max(0, flight.aircraft.maintenance_level - condition_loss * 2)
        
        # Event senden
        self._emit_event(
            f"Flug {flight.flight_number} ({flight.origin}→{flight.destination}) "
            f"abgeschlossen: +${profit:,.0f} (Einnahmen: ${revenue:,.0f}, Kosten: ${cost:,.0f})"
        )
        
        # Callback
        if self._on_flight_completed:
            self._on_flight_completed(flight)

    def buy_aircraft(self, aircraft_type_index: int) -> Optional[Aircraft]:
        """Kauft ein Flugzeug für den Spieler."""
        if aircraft_type_index < 0 or aircraft_type_index >= len(self.available_aircraft_types):
            return None
            
        aircraft_data = self.available_aircraft_types[aircraft_type_index]
        
        if self.player.money >= aircraft_data["purchase_price"]:
            self.player.spend_money(aircraft_data["purchase_price"])
            
            aircraft = Aircraft(
                name=aircraft_data["name"],
                model=aircraft_data["model"],
                max_fuel=aircraft_data["max_fuel"],
                fuel=aircraft_data["max_fuel"],
                passenger_capacity=aircraft_data["passenger_capacity"],
                cargo_capacity=aircraft_data["cargo_capacity"],
                speed=aircraft_data["speed"],
                condition=aircraft_data["condition"],
                maintenance_level=100.0,
                purchase_price=aircraft_data["purchase_price"],
                operating_cost=aircraft_data["operating_cost"],
            )
            
            self.player.add_aircraft(aircraft)
            self.aircraft.append(aircraft)
            self.airport.add_aircraft(aircraft)
            
            self._emit_event(f"Neues Flugzeug gekauft: {aircraft.name} für ${aircraft.purchase_price:,.0f}")
            self._notify_state_changed()
            
            return aircraft
        return None

    def refuel_aircraft(self, aircraft: Aircraft, amount: Optional[float] = None) -> bool:
        """Betankt ein Flugzeug."""
        if amount is None:
            amount = aircraft.max_fuel - aircraft.fuel
        
        fuel_cost = amount * DEFAULT_FUEL_CONSUMPTION * 0.5  # $0.5 per fuel unit
        
        if self.player.money >= fuel_cost:
            self.player.spend_money(fuel_cost)
            aircraft.refuel(amount)
            self._emit_event(f"{aircraft.name} betankt ({amount:.0f} Einheiten) für ${fuel_cost:,.0f}")
            self._notify_state_changed()
            return True
        return False

    def repair_aircraft(self, aircraft: Aircraft) -> bool:
        """Repariert ein Flugzeug."""
        damage = 100.0 - aircraft.condition
        repair_cost = damage * REPAIR_COST_PER_DAMAGE
        
        if self.player.money >= repair_cost:
            self.player.spend_money(repair_cost)
            aircraft.repair()
            self._emit_event(f"{aircraft.name} repariert für ${repair_cost:,.0f}")
            self._notify_state_changed()
            return True
        return False

    def start_advertising(self, duration_hours: float = 1.0, cost: float = 5000) -> bool:
        """Startet Werbung für mehr Passagiere."""
        if self.player.money >= cost:
            self.player.spend_money(cost)
            self._advertising_multiplier = 1.5
            self._advertising_end_time = time.time() + duration_hours * 3600
            self._emit_event(f"Werbung gestartet für {duration_hours}h (Kosten: ${cost:,.0f})")
            self._notify_state_changed()
            return True
        return False

    def schedule_flight(self, destination_index: int, aircraft_index: int) -> bool:
        """Plant einen Flug zu einem Ziel mit einem Flugzeug."""
        if destination_index < 0 or destination_index >= len(self.available_destinations):
            return False
        if aircraft_index < 0 or aircraft_index >= len(self.aircraft):
            return False
            
        destination = self.available_destinations[destination_index]
        aircraft = self.aircraft[aircraft_index]
        
        if aircraft.status != "parked":
            self._emit_event(f"{aircraft.name} ist nicht verfügbar (Status: {aircraft.status})")
            return False
            
        if aircraft.fuel < destination["distance"] * 0.1:
            self._emit_event(f"{aircraft.name} hat nicht genug Treibstoff für den Flug")
            return False
            
        if aircraft.condition < 30:
            self._emit_event(f"{aircraft.name} braucht Wartung (Kondition: {aircraft.condition:.0f}%)")
            return False
        
        # Passagiere basierend auf Reputation und Werbung
        passengers = int(destination["base_passengers"] * (self.player.reputation / 50.0) * self._advertising_multiplier)
        passengers = min(passengers, aircraft.passenger_capacity)
        
        cargo = min(aircraft.cargo_capacity * 0.5, destination["distance"] * 10)
        
        # Flugdauer basierend auf Distanz und Geschwindigkeit
        # Skaliert für Gameplay: 100km = ~1 Sekunde Spielzeit
        duration = destination["distance"] / aircraft.speed * 10.0
        
        flight = Flight(
            flight_number=f"FL{len(self.flights) + 1:03d}",
            origin=self.airport.name,
            destination=destination["name"],
            aircraft=aircraft,
            passengers=passengers,
            cargo=cargo,
            distance=destination["distance"],
            duration=duration,
            status="scheduled",
        )
        
        self.flights.append(flight)
        self.airport.add_flight(flight)
        
        self._emit_event(
            f"Flug {flight.flight_number} geplant: {self.airport.name} → {destination['name']} "
            f"({passengers} Passagiere, {cargo:.0f}kg Fracht)"
        )
        self._notify_state_changed()
        return True

    def get_available_aircraft_types(self) -> List[Dict[str, Any]]:
        """Gibt verfügbare Flugzeugtypen zurück."""
        return self.available_aircraft_types

    def get_available_destinations(self) -> List[Dict[str, Any]]:
        """Gibt verfügbare Ziele zurück."""
        return self.available_destinations

    def get_aircraft_list(self) -> List[Aircraft]:
        """Gibt die Liste der Flugzeuge des Spielers zurück."""
        return self.aircraft

    def get_flights(self) -> List[Flight]:
        """Gibt alle Flüge zurück."""
        return self.flights

    def get_game_state(self) -> dict:
        """Gibt den aktuellen Spielzustand zurück."""
        active_flights = [f for f in self.flights if f.status == "in_progress"]
        scheduled_flights = [f for f in self.flights if f.status == "scheduled"]
        completed_flights = [f for f in self.flights if f.status == "completed"]
        
        return {
            "money": self.player.money,
            "reputation": self.player.reputation,
            "aircraft_count": len(self.aircraft),
            "active_flights": len(active_flights),
            "scheduled_flights": len(scheduled_flights),
            "completed_flights": len(completed_flights),
            "airport_status": self.airport.status,
            "airport_name": self.airport.name,
            "advertising_active": self._advertising_multiplier > 1.0,
            "advertising_multiplier": self._advertising_multiplier,
            "aircraft": [
                {
                    "name": a.name,
                    "model": a.model,
                    "status": a.status,
                    "fuel": a.fuel,
                    "max_fuel": a.max_fuel,
                    "condition": a.condition,
                    "maintenance_level": a.maintenance_level,
                    "passenger_capacity": a.passenger_capacity,
                    "current_flight": a.current_flight,
                }
                for a in self.aircraft
            ],
            "flights": [
                {
                    "flight_number": f.flight_number,
                    "origin": f.origin,
                    "destination": f.destination,
                    "status": f.status,
                    "progress": getattr(f, '_progress', 0.0),
                    "passengers": f.passengers,
                    "distance": f.distance,
                }
                for f in self.flights
            ],
        }

    def save_game(self, filepath: str) -> bool:
        """Speichert den Spielstand."""
        import json
        try:
            state = {
                "player": self.player.to_dict(),
                "airport": self.airport.to_dict(),
                "aircraft": [a.to_dict() for a in self.aircraft],
                "flights": [f.to_dict() for f in self.flights],
                "game_speed": self.game_speed,
                "advertising_multiplier": self._advertising_multiplier,
                "advertising_end_time": self._advertising_end_time,
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
            return False

    def load_game(self, filepath: str) -> bool:
        """Lädt einen Spielstand."""
        import json
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.player.load_state(state["player"])
            self.airport = Airport(**state["airport"])
            self.aircraft = [Aircraft(**a) for a in state["aircraft"]]
            self.flights = [Flight(**f) for f in state["flights"]]
            self.game_speed = state.get("game_speed", 1.0)
            self._advertising_multiplier = state.get("advertising_multiplier", 1.0)
            self._advertising_end_time = state.get("advertising_end_time")
            
            self._notify_state_changed()
            return True
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
            return False
