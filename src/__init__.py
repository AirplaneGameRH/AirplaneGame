"""
AirportGame package.

Dieses Paket fasst die Hauptmodule und Subpakete des 2D-Flughafen-Idle-Games zusammen.
"""

from .main import main
from .core import GameLogic, AirportRenderer, AssetManager
from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget
from .entities import Aircraft, Flight, Airport, Player

__all__ = [
    "main",
    "GameLogic",
    "AirportRenderer",
    "AssetManager",
    "DashboardWidget",
    "ControlPanelWidget",
    "StatusPanelWidget",
    "Aircraft",
    "Flight",
    "Airport",
    "Player",
]
