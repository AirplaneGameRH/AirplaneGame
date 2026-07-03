"""
Entity-Paket für das AirportGame.

Dieses Paket fasst die Kernentitäten des Spiels zusammen: Flugzeuge, Flüge,
Flughafen und Spieler.
"""

from .aircraft import Aircraft
from .flight import Flight
from .airport import Airport
from .player import Player

__all__ = ["Aircraft", "Flight", "Airport", "Player"]
