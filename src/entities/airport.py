"""Grundmodell für Flughafen-Entitäten."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class Airport:
    """Repräsentiert den Flughafen mit Infrastruktur und Zustand."""

    def __init__(
        self,
        airport_id: Optional[str] = None,
        name: str = "Airport",
        city: str = "Unknown",
        gates: int = 0,
        runways: int = 0,
        hangars: int = 0,
        aircraft: Optional[List[Any]] = None,
        flights: Optional[List[Any]] = None,
        passengers: int = 0,
        cargo: float = 0.0,
        economy: float = 0.0,
        status: str = "open",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = airport_id or "airport-1"
        self.name = name
        self.city = city
        self.gates = gates
        self.runways = runways
        self.hangars = hangars
        self.aircraft = aircraft or []
        self.flights = flights or []
        self.passengers = passengers
        self.cargo = cargo
        self.economy = economy
        self.status = status
        self.metadata = metadata or {}
        self._gate_usage: Dict[int, bool] = {}
        self._runway_usage: Dict[int, bool] = {}

    def add_aircraft(self, aircraft: Any) -> Airport:
        """Fügt dem Flughafen ein Flugzeug hinzu."""
        self.aircraft.append(aircraft)
        return self

    def remove_aircraft(self, aircraft: Any) -> Airport:
        """Entfernt ein Flugzeug vom Flughafen."""
        if aircraft in self.aircraft:
            self.aircraft.remove(aircraft)
        return self

    def add_flight(self, flight: Any) -> Airport:
        """Plant einen neuen Flug für den Flughafen."""
        self.flights.append(flight)
        return self

    def remove_flight(self, flight: Any) -> Airport:
        """Entfernt einen Flug aus dem Flughafenplan."""
        if flight in self.flights:
            self.flights.remove(flight)
        return self

    def open_gate(self, gate_id: Optional[int] = None) -> Airport:
        """Öffnet einen Gate."""
        if gate_id is not None:
            self._gate_usage[gate_id] = False
        return self

    def close_gate(self, gate_id: Optional[int] = None) -> Airport:
        """Schließt einen Gate."""
        if gate_id is not None:
            self._gate_usage[gate_id] = True
        return self

    def get_available_gate(self) -> Optional[int]:
        """Gibt einen freien Gate zurück."""
        for i in range(1, self.gates + 1):
            if not self._gate_usage.get(i, False):
                return i
        return None

    def get_available_runway(self) -> Optional[int]:
        """Gibt eine freie Startbahn zurück."""
        for i in range(1, self.runways + 1):
            if not self._runway_usage.get(i, False):
                return i
        return None

    def schedule_maintenance(self, aircraft: Any) -> Airport:
        """Plant Wartung für ein Flugzeug."""
        aircraft.enter_maintenance()
        return self

    def update(self) -> Airport:
        """Aktualisiert den Flughafenstatus."""
        waiting_flights = [f for f in self.flights if getattr(f, "status", "") == "scheduled"]
        for flight in waiting_flights:
            aircraft = getattr(flight, "aircraft", None)
            if aircraft and aircraft.status == "parked" and aircraft.fuel > 0:
                gate = self.get_available_gate()
                runway = self.get_available_runway()
                if gate and runway:
                    flight.start()
                    aircraft.start_flight(flight.destination)
                    self._gate_usage[gate] = True
                    self._runway_usage[runway] = True
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Gibt eine einfache Serienform zurück."""
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "gates": self.gates,
            "runways": self.runways,
            "hangars": self.hangars,
            "aircraft": self.aircraft,
            "flights": self.flights,
            "passengers": self.passengers,
            "cargo": self.cargo,
            "economy": self.economy,
            "status": self.status,
            "metadata": self.metadata,
        }
