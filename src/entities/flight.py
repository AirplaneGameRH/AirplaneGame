"""Grundmodell für Flug-Entitäten."""

from __future__ import annotations

from typing import Any, Dict, Optional


class Flight:
    """Repräsentiert einen Flug im Idle-Game."""

    def __init__(
        self,
        flight_id: Optional[str] = None,
        flight_number: str = "FLIGHT-1",
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        aircraft: Optional[Any] = None,
        passengers: int = 0,
        cargo: float = 0.0,
        distance: float = 0.0,
        duration: float = 0.0,
        status: str = "scheduled",
        departure_time: Optional[float] = None,
        arrival_time: Optional[float] = None,
        revenue: float = 0.0,
        operating_cost: float = 0.0,
        priority: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = flight_id or "flight-1"
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.aircraft = aircraft
        self.passengers = passengers
        self.cargo = cargo
        self.distance = distance
        self.duration = duration
        self.status = status
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.revenue = revenue
        self.operating_cost = operating_cost
        self.priority = priority
        self.metadata = metadata or {}

    def start(self) -> Flight:
        """Startet den Flug."""
        return self

    def cancel(self) -> Flight:
        """Bricht den Flug ab."""
        return self

    def complete(self) -> Flight:
        """Schließt den Flug ab."""
        return self

    def update_progress(self) -> Flight:
        """Aktualisiert den Fortschritt des Fluges."""
        return self

    def assign_aircraft(self, aircraft: Any) -> Flight:
        """Weist dem Flug ein Flugzeug zu."""
        self.aircraft = aircraft
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Gibt eine einfache Serienform zurück."""
        return {
            "id": self.id,
            "flight_number": self.flight_number,
            "origin": self.origin,
            "destination": self.destination,
            "aircraft": self.aircraft,
            "passengers": self.passengers,
            "cargo": self.cargo,
            "distance": self.distance,
            "duration": self.duration,
            "status": self.status,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "revenue": self.revenue,
            "operating_cost": self.operating_cost,
            "priority": self.priority,
            "metadata": self.metadata,
        }
