"""Einfache Lokalisierung für das AirportGame."""

from __future__ import annotations

from typing import Dict, Sequence

LANGUAGE_NAMES: Dict[str, str] = {
    "de": "Deutsch",
    "en": "English",
}

DEFAULT_LANGUAGE = "de"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "de": {
        "app_title": "AirplaneGame",
        "loading_initial": "Initialisiere Spiel...",
        "loading_assets": "Lade Assets...",
        "initializing_renderer": "Initialisiere Renderer...",
        "starting_logic": "Starte Spiel-Logik...",
        "finished": "Fertig!",
        "main_menu_title": "Hauptmenü",
        "new_game": "Neues Spiel",
        "load_game": "Spiel laden",
        "settings": "Einstellungen",
        "settings_title": "Einstellungen",
        "language_label": "Sprache",
        "select_language": "Sprache wählen:",
        "back": "Zurück",
        "game_placeholder_new": "Neues Spiel wird gestartet...",
        "game_placeholder_load": "Spiel wird geladen...",
        "menu_instruction": "Wähle eine Option aus dem Menü:",
    },
    "en": {
        "app_title": "AirplaneGame",
        "loading_initial": "Initializing game...",
        "loading_assets": "Loading assets...",
        "initializing_renderer": "Initializing renderer...",
        "starting_logic": "Starting game logic...",
        "finished": "Finished!",
        "main_menu_title": "Main Menu",
        "new_game": "New Game",
        "load_game": "Load Game",
        "settings": "Settings",
        "settings_title": "Settings",
        "language_label": "Language",
        "select_language": "Select language:",
        "back": "Back",
        "game_placeholder_new": "Starting new game...",
        "game_placeholder_load": "Loading game...",
        "menu_instruction": "Please select an option:",
    },
}


class Translator:
    """Ein einfacher Übersetzer für UI-Strings."""

    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        self.language = language if language in TRANSLATIONS else DEFAULT_LANGUAGE

    def t(self, key: str) -> str:
        return TRANSLATIONS.get(self.language, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)

    def set_language(self, language: str) -> None:
        if language in TRANSLATIONS:
            self.language = language

    def available_languages(self) -> Sequence[str]:
        return list(LANGUAGE_NAMES.keys())

    def language_name(self, code: str) -> str:
        return LANGUAGE_NAMES.get(code, code)
