"""Grundmodell für den Spielerzustand."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class Player:
    """Repräsentiert den Spieler und dessen Ressourcen."""

    def __init__(
        self,
        player_id: Optional[str] = None,
        name: str = "Player",
        money: float = 0.0,
        reputation: float = 0.0,
        fleet: Optional[List[Any]] = None,
        airports: Optional[List[Any]] = None,
        unlocked_aircraft: Optional[List[str]] = None,
        stats: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.id = player_id or "player-1"
        self.name = name
        self.money = money
        self.reputation = reputation
        self.fleet = fleet or []
        self.airports = airports or []
        self.unlocked_aircraft = unlocked_aircraft or []
        self.stats = stats or {}
        self.metadata = metadata or {}

    def add_money(self, amount: float = 0.0) -> Player:
        """Erhöht das Geld des Spielers."""
        self.money += amount
        return self

    def spend_money(self, amount: float = 0.0) -> Player:
        """Verringert das Geld des Spielers."""
        self.money = max(0.0, self.money - amount)
        return self

    def add_aircraft(self, aircraft: Any) -> Player:
        """Fügt der Flotte ein Flugzeug hinzu."""
        self.fleet.append(aircraft)
        return self

    def remove_aircraft(self, aircraft: Any) -> Player:
        """Entfernt ein Flugzeug aus der Flotte."""
        if aircraft in self.fleet:
            self.fleet.remove(aircraft)
        return self

    def unlock_aircraft(self, aircraft_name: str) -> Player:
        """Schaltet ein Flugzeug frei."""
        if aircraft_name not in self.unlocked_aircraft:
            self.unlocked_aircraft.append(aircraft_name)
        return self

    def add_airport(self, airport: Any) -> Player:
        """Fügt dem Spieler einen Flughafen hinzu."""
        self.airports.append(airport)
        return self

    def remove_airport(self, airport: Any) -> Player:
        """Entfernt einen Flughafen vom Spieler."""
        if airport in self.airports:
            self.airports.remove(airport)
        return self

    def update_stats(self, **kwargs: Any) -> Player:
        """Aktualisiert Spielerstatistiken."""
        self.stats.update(kwargs)
        return self

    def save_state(self) -> Dict[str, Any]:
        """Erstellt einen gespeicherten Zustand."""
        return self.to_dict()

    def load_state(self, state: Dict[str, Any]) -> Player:
        """Lädt einen gespeicherten Zustand."""
        self.id = state.get("id", self.id)
        self.name = state.get("name", self.name)
        self.money = state.get("money", self.money)
        self.reputation = state.get("reputation", self.reputation)
        self.fleet = state.get("fleet", self.fleet)
        self.airports = state.get("airports", self.airports)
        self.unlocked_aircraft = state.get("unlocked_aircraft", self.unlocked_aircraft)
        self.stats = state.get("stats", self.stats)
        self.metadata = state.get("metadata", self.metadata)
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Gibt eine einfache Serienform zurück."""
        return {
            "id": self.id,
            "name": self.name,
            "money": self.money,
            "reputation": self.reputation,
            "fleet": [a.to_dict() if hasattr(a, "to_dict") else str(a) for a in self.fleet],
            "airports": [a.to_dict() if hasattr(a, "to_dict") else str(a) for a in self.airports],
            "unlocked_aircraft": self.unlocked_aircraft,
            "stats": self.stats,
            "metadata": self.metadata,
        }
