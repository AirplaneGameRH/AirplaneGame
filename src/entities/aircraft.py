"""Grundmodell für Flugzeug-Entitäten."""

from __future__ import annotations

from typing import Any, Dict, Optional


class Aircraft:
    """Repräsentiert ein Flugzeug im Spiel."""

    def __init__(
        self,
        aircraft_id: Optional[str] = None,
        name: str = "Aircraft",
        model: str = "Unknown",
        airline: str = "Unknown",
        status: str = "parked",
        current_airport: Optional[str] = None,
        current_flight: Optional[str] = None,
        fuel: float = 0.0,
        max_fuel: float = 0.0,
        passenger_capacity: int = 0,
        cargo_capacity: float = 0.0,
        speed: float = 0.0,
        condition: float = 100.0,
        maintenance_level: float = 100.0,
        purchase_price: float = 0.0,
        operating_cost: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = aircraft_id or "aircraft-1"
        self.name = name
        self.model = model
        self.airline = airline
        self.status = status
        self.current_airport = current_airport
        self.current_flight = current_flight
        self.fuel = fuel
        self.max_fuel = max_fuel
        self.passenger_capacity = passenger_capacity
        self.cargo_capacity = cargo_capacity
        self.speed = speed
        self.condition = condition
        self.maintenance_level = maintenance_level
        self.purchase_price = purchase_price
        self.operating_cost = operating_cost
        self.metadata = metadata or {}

    def board_passengers(self, count: int = 0) -> None:
        """Lädt Passagiere an Bord."""
        return None

    def load_cargo(self, amount: float = 0.0) -> None:
        """Lädt Fracht auf das Flugzeug."""
        return None

    def refuel(self, amount: Optional[float] = None) -> None:
        """Betankt das Flugzeug."""
        return None

    def start_flight(self, destination: Optional[str] = None) -> None:
        """Startet einen Flug."""
        return None

    def land(self) -> None:
        """Lässt das Flugzeug landen."""
        return None

    def enter_maintenance(self) -> None:
        """Versetzt das Flugzeug in Wartung."""
        return None

    def repair(self) -> None:
        """Repariert das Flugzeug."""
        return None

    def update(self) -> None:
        """Aktualisiert den Zustand des Flugzeugs."""
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Gibt eine einfache Serienform zurück."""
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "airline": self.airline,
            "status": self.status,
            "current_airport": self.current_airport,
            "current_flight": self.current_flight,
            "fuel": self.fuel,
            "max_fuel": self.max_fuel,
            "passenger_capacity": self.passenger_capacity,
            "cargo_capacity": self.cargo_capacity,
            "speed": self.speed,
            "condition": self.condition,
            "maintenance_level": self.maintenance_level,
            "purchase_price": self.purchase_price,
            "operating_cost": self.operating_cost,
            "metadata": self.metadata,
        }
