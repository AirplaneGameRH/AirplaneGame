"""
Zentrale Konfiguration für das Airport Game.

Dieses Modul definiert alle Spielkonstanten und Konfigurationswerte,
die über das gesamte Spiel hinweg verwendet werden.
"""

from pathlib import Path

# Projekt-Pfade
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Spielfenster
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_TITLE = "AirportGame"

# Renderer
AIRPORT_RENDERER_WIDTH = 800
AIRPORT_RENDERER_HEIGHT = 600

# Spiel-Wirtschaft
STARTING_MONEY = 10000
STARTING_FUEL = 5000

# Flugzeuge
DEFAULT_FUEL_CONSUMPTION = 10  # pro Flug
REPAIR_COST_PER_DAMAGE = 100

# Idle-Mechaniken
AUTO_UPDATE_INTERVAL = 100  # ms zwischen Game-Updates
ANIMATION_FPS = 60

# Debug / Development
DEBUG_MODE = False
LOG_LEVEL = "INFO"
