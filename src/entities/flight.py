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
        self._progress: float = 0.0
        self._elapsed_time: float = 0.0

    def start(self) -> Flight:
        """Startet den Flug."""
        self.status = "in_progress"
        self._progress = 0.0
        self._elapsed_time = 0.0
        if self.aircraft:
            self.aircraft.start_flight(self.destination)
        return self

    def cancel(self) -> Flight:
        """Bricht den Flug ab."""
        self.status = "cancelled"
        if self.aircraft:
            self.aircraft.land()
        return self

    def complete(self) -> Flight:
        """Schließt den Flug ab."""
        self.status = "completed"
        self._progress = 1.0
        if self.aircraft:
            self.aircraft.land()
        return self

    def update_progress(self, dt: float = 1.0) -> Flight:
        """Aktualisiert den Fortschritt des Fluges."""
        if self.status != "in_progress" or self.duration <= 0:
            return self

        self._elapsed_time += dt
        self._progress = min(1.0, self._elapsed_time / self.duration)

        if self._progress >= 1.0:
            self.complete()

        return self

    def assign_aircraft(self, aircraft: Any) -> Flight:
        """Weist dem Flug ein Flugzeug zu."""
        self.aircraft = aircraft
        return self

    def calculate_revenue(self, ticket_price: float = 100.0, cargo_rate: float = 10.0) -> float:
        """Berechnet die Einnahmen basierend auf Passagieren und Fracht."""
        passenger_revenue = self.passengers * ticket_price
        cargo_revenue = self.cargo * cargo_rate
        self.revenue = passenger_revenue + cargo_revenue
        return self.revenue

    def calculate_operating_cost(self, fuel_cost_per_unit: float = 5.0, maintenance_factor: float = 0.1) -> float:
        """Berechnet die Betriebskosten (Treibstoff + Wartung)."""
        if self.aircraft:
            fuel_used = min(self.aircraft.fuel, self.distance * 0.1)
            self.aircraft.fuel -= fuel_used
            fuel_cost = fuel_used * fuel_cost_per_unit
            maintenance_cost = self.distance * maintenance_factor
            self.operating_cost = fuel_cost + maintenance_cost
        return self.operating_cost

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
            "progress": self._progress,
        }
