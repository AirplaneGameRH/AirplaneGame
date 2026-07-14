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

    def board_passengers(self, count: int = 0) -> Aircraft:
        """Lädt Passagiere an Bord."""
        boarded = min(count, self.passenger_capacity)
        self.metadata["passengers_onboard"] = boarded
        return self

    def load_cargo(self, amount: float = 0.0) -> Aircraft:
        """Lädt Fracht auf das Flugzeug."""
        loaded = min(amount, self.cargo_capacity)
        self.metadata["cargo_onboard"] = loaded
        return self

    def refuel(self, amount: Optional[float] = None) -> Aircraft:
        """Betankt das Flugzeug."""
        if amount is None:
            amount = self.max_fuel - self.fuel
        self.fuel = min(self.max_fuel, self.fuel + max(0.0, amount))
        return self

    def start_flight(self, destination: Optional[str] = None) -> Aircraft:
        """Startet einen Flug."""
        self.status = "in_flight"
        if destination:
            self.current_airport = None
            self.current_flight = destination
            self.metadata["destination"] = destination
        return self

    def land(self) -> Aircraft:
        """Lässt das Flugzeug landen."""
        self.status = "landed"
        self.current_flight = None
        self.metadata.pop("destination", None)
        return self

    def enter_maintenance(self) -> Aircraft:
        """Versetzt das Flugzeug in Wartung."""
        self.status = "maintenance"
        self.current_flight = None
        return self

    def repair(self) -> Aircraft:
        """Repariert das Flugzeug."""
        self.condition = 100.0
        self.maintenance_level = 100.0
        if self.status == "maintenance":
            self.status = "parked"
        return self

    def update(self) -> Aircraft:
        """Aktualisiert den Zustand des Flugzeugs (z. B. Wartungsverfall)."""
        if self.status == "in_flight":
            self.condition = max(0.0, self.condition - 0.1)
            self.maintenance_level = max(0.0, self.maintenance_level - 0.05)
        elif self.status == "parked":
            self.maintenance_level = min(100.0, self.maintenance_level + 0.1)
        return self

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
