"""Persistente Einstellungen für das Airport Game (plattformübergreifend)."""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class SettingsManager:
    """Verwaltet persistente Benutzereinstellungen."""

    def __init__(self, app_name: str = "AirplaneGame"):
        self.app_name = app_name
        self._settings: Dict[str, Any] = {}
        self._settings_file = self._get_settings_path()
        self._load()

    def _get_settings_path(self) -> Path:
        """Ermittelt den plattformspezifischen Pfad für Einstellungen."""
        system = os.name
        
        if system == "nt":  # Windows
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif system == "posix":
            if sys.platform == "darwin":  # macOS
                base = Path.home() / "Library" / "Application Support"
            else:  # Linux/Unix
                base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        else:
            base = Path.home()
        
        config_dir = base / self.app_name
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "settings.json"

    def _load(self) -> None:
        """Lädt Einstellungen aus der JSON-Datei."""
        if self._settings_file.exists():
            try:
                with open(self._settings_file, "r", encoding="utf-8") as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, OSError):
                self._settings = {}

    def _save(self) -> None:
        """Speichert Einstellungen in die JSON-Datei."""
        try:
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2, ensure_ascii=False)
        except OSError:
            pass  # Stillschweigend fehlschlagen bei Schreibfehlern

    def get(self, key: str, default: Any = None) -> Any:
        """Holt einen Einstellungswert."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Setzt einen Einstellungswert und speichert sofort."""
        self._settings[key] = value
        self._save()

    def get_int(self, key: str, default: int = 0) -> int:
        """Holt einen Integer-Wert."""
        try:
            return int(self.get(key, default))
        except (ValueError, TypeError):
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Holt einen Float-Wert."""
        try:
            return float(self.get(key, default))
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Holt einen Boolean-Wert."""
        val = self.get(key, default)
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() in ("true", "1", "yes", "on")
        return bool(val)


# Globale Instanz
_settings_instance: Optional[SettingsManager] = None


def get_settings() -> SettingsManager:
    """Gibt die globale SettingsManager-Instanz zurück."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = SettingsManager()
    return _settings_instance


def save_settings(settings_dict: Dict[str, Any]) -> None:
    """Hilfsfunktion zum direkten Speichern eines Settings-Dicts."""
    settings = get_settings()
    for key, value in settings_dict.items():
        settings.set(key, value)