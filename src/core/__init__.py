"""
Core-Paket für zentrale Spielelemente.

Dieses Paket enthält Logik, Rendering und Asset-Verwaltung.
"""

from .game_logic import GameLogic
from .renderer import AirportRenderer
from .assets import AssetManager

__all__ = ["GameLogic", "AirportRenderer", "AssetManager"]
