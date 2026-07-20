"""Lokalisierung für das AirportGame mit API-basierter Übersetzung."""

from __future__ import annotations

from typing import Dict, Sequence, Optional

from PyQt6.QtCore import QThread, pyqtSignal, QObject

# ============================================================================
# BASIS-DEUTSCHES WÖRTERBUCH (Quelle für alle Übersetzungen)
# ============================================================================

BASE_GERMAN_TEXTS: Dict[str, str] = {
    # App & Loading
    "app_title": "AirplaneGame",
    "loading_initial": "Initialisiere Spiel...",
    "loading_assets": "Lade Assets...",
    "initializing_renderer": "Initialisiere Renderer...",
    "starting_logic": "Starte Spiel-Logik...",
    "finished": "Fertig!",

    # Main Menu
    "main_menu_title": "Hauptmenü",
    "new_game": "Neues Spiel",
    "load_game": "Spiel laden",
    "settings": "Einstellungen",
    "menu_instruction": "Wähle eine Option aus dem Menü:",

    # Settings
    "settings_title": "Einstellungen",
    "language_label": "Sprache",
    "select_language": "Sprache wählen:",
    "back": "Zurück",
    "settings_tab_general": "Allgemein",
    "settings_tab_audio": "Audio",
    "master_volume": "Gesamtlautstärke",
    "music_volume": "Musik",

    # Settings actions
    "save": "Speichern",
    "settings_saved": "Einstellungen gespeichert",
    "language_apply_hint": "Auf 'Speichern' klicken, um die Sprache zu aktivieren",

    # Placeholders
    "game_placeholder_new": "Neues Spiel wird gestartet...",
    "game_placeholder_load": "Spiel wird geladen...",

    # Game UI - Dashboard
    "dashboard_title": "Dashboard",
    "money_label": "Geld",
    "reputation_label": "Reputation",
    "aircraft_count_label": "Flugzeuge",
    "active_flights_label": "Aktive Flüge",
    "fuel_label": "Treibstoff",

    # Game UI - Control Panel
    "control_title": "Steuerung",
    "buy_aircraft": "Flugzeug kaufen",
    "repair_maintain": "Warten/Reparieren",
    "advertise": "Werbung schalten",
    "refuel": "Betanken",
    "schedule_flight": "Flug planen",

    # Game UI - Status Panel
    "status_title": "Live-Status",

    # Game Logic / Events
    "event_flight_departed": "Flug {flight} ist gestartet",
    "event_flight_arrived": "Flug {flight} ist angekommen - Einnahmen: {money}",
    "event_aircraft_damaged": "Flugzeug {aircraft} benötigt Wartung!",
    "event_maintenance_done": "Wartung an {aircraft} abgeschlossen",
    "event_new_aircraft": "Neues Flugzeug gekauft: {aircraft}",
    "event_cannot_afford": "Nicht genug Geld für {item}",
    "event_flight_scheduled": "Flug {flight} geplant",

    # Aircraft Status
    "status_parked": "Geparkt",
    "status_boarding": "Boarding",
    "status_taxiing": "Rollt",
    "status_takeoff": "Start",
    "status_in_flight": "Im Flug",
    "status_landing": "Landeanflug",
    "status_maintenance": "Wartung",
    "status_refueling": "Betankung",

    # Dialogs / Messages
    "confirm_quit": "Möchten Sie das Spiel wirklich beenden?",
    "confirm_new_game": "Neues Spiel starten? Ungespeicherter Fortschritt geht verloren.",
    "save_game": "Spiel speichern",
    "load_game_title": "Spielstand laden",
    "no_savegames": "Keine Spielstände gefunden",

    # Errors
    "error_save_failed": "Speichern fehlgeschlagen",
    "error_load_failed": "Laden fehlgeschlagen",
    "error_no_aircraft": "Kein Flugzeug verfügbar",
    "error_no_gate": "Kein freies Gate",
    "error_flight_cancelled": "Flug abgebrochen",
}

# ============================================================================
# SPRACH-KONFIGURATION
# ============================================================================

LANGUAGE_NAMES: Dict[str, str] = {
    "de": "Deutsch",
    "en": "English",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "pl": "Polski",
    "ru": "Русский",
    "zh-CH": "中文",
    "ja": "日本語",
    "ko": "한국어",
}

DEFAULT_LANGUAGE = "de"

# ============================================================================
# ÜBERSETZUNGS-API (Google Translate via deep-translator, batch-fähig)
# ============================================================================


class GoogleTranslateAPI:
    """Google Translate via deep-translator (kostenlos, kein API-Key nötig)."""

    def translate_batch(self, texts: Dict[str, str], target_lang: str, source_lang: str = "de") -> Dict[str, str]:
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source=source_lang, target=target_lang)
        keys = list(texts.keys())
        values = list(texts.values())

        try:
            translated = translator.translate_batch(values)
            return {keys[i]: translated[i] for i in range(len(keys))}
        except Exception as e:
            print(f"GoogleTranslate Fehler: {e}")
            return texts  # Fallback: Deutsche Texte


# ============================================================================
# ÜBERSETZUNGS-THREAD (QThread für Hintergrund-Übersetzung)
# ============================================================================


class TranslationWorker(QThread):
    """Führt Übersetzung im Hintergrund aus und sendet Signale."""

    finished = pyqtSignal(str, dict)   # (target_lang, translated_dict)
    error = pyqtSignal(str, str)       # (target_lang, error_message)

    def __init__(self, api, texts: Dict[str, str], target_lang: str, source_lang: str = "de"):
        super().__init__()
        self._api = api
        self._texts = texts
        self._target_lang = target_lang
        self._source_lang = source_lang

    def run(self):
        try:
            translated = self._api.translate_batch(self._texts, self._target_lang, self._source_lang)
            self.finished.emit(self._target_lang, translated)
        except Exception as e:
            self.error.emit(self._target_lang, str(e))


# ============================================================================
# TRANSLATOR HAUPTKLASSE
# ============================================================================


class Translator(QObject):
    """
    Übersetzer mit API-basierter Vorübersetzung aller Texte.

    1. Basis ist das deutsche Wörterbuch (BASE_GERMAN_TEXTS)
    2. Beim Sprachwechsel: Alle Texte werden per API in Zielsprache übersetzt
    3. Ergebnis wird im Cache gespeichert (nur im Speicher)
    4. Nur die aktuelle Sprache wird in Settings persistiert
    """

    language_changed = pyqtSignal(str)

    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
        api=None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._language = language if language in LANGUAGE_NAMES else DEFAULT_LANGUAGE
        self._api = api or GoogleTranslateAPI()
        self._cache: Dict[str, Dict[str, str]] = {
            "de": BASE_GERMAN_TEXTS.copy()
        }
        self._worker: Optional[TranslationWorker] = None
        self._pending_lang: Optional[str] = None  # Wartende Sprache bei Rennbedingungen

    @property
    def language(self) -> str:
        return self._language

    @property
    def available_languages(self) -> Sequence[str]:
        return list(LANGUAGE_NAMES.keys())

    def language_name(self, code: str) -> str:
        return LANGUAGE_NAMES.get(code, code)

    def t(self, key: str, **kwargs) -> str:
        """Holt einen übersetzten Text mit optionalen Platzhaltern."""
        lang_cache = self._cache.get(self._language, self._cache["de"])
        text = lang_cache.get(key, BASE_GERMAN_TEXTS.get(key, key))

        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        return text

    def set_language(self, language: str) -> bool:
        """Setzt die Sprache und startet ggf. Übersetzung im Hintergrund."""
        if language not in LANGUAGE_NAMES:
            return False
        if language == self._language and language in self._cache:
            return True

        self._language = language

        if language not in self._cache:
            self._start_translation(language)
        else:
            self.language_changed.emit(language)

        return True

    def _start_translation(self, target_lang: str) -> None:
        """Startet Hintergrund-Übersetzung via QThread."""
        # Wenn bereits ein Worker läuft, merke die neue Sprache
        if self._worker is not None and self._worker.isRunning():
            self._pending_lang = target_lang
            return

        # Alten Worker aufräumen
        if self._worker is not None:
            try:
                self._worker.finished.disconnect(self._on_translation_finished)
                self._worker.error.disconnect(self._on_translation_error)
            except (TypeError, RuntimeError):
                pass

        self._pending_lang = None
        self._worker = TranslationWorker(self._api, BASE_GERMAN_TEXTS, target_lang)
        self._worker.finished.connect(self._on_translation_finished)
        self._worker.error.connect(self._on_translation_error)
        self._worker.start()

    def _on_translation_finished(self, target_lang: str, translated: dict) -> None:
        self._cache[target_lang] = translated

        # Wenn eine neuere Sprache angefordert wurde, starte die sofort
        if self._pending_lang is not None:
            pending = self._pending_lang
            self._pending_lang = None
            self._start_translation(pending)
        else:
            self.language_changed.emit(target_lang)

    def _on_translation_error(self, target_lang: str, error_msg: str) -> None:
        print(f"Übersetzungsfehler für {target_lang}: {error_msg}")
        self._cache[target_lang] = BASE_GERMAN_TEXTS.copy()

        if self._pending_lang is not None:
            pending = self._pending_lang
            self._pending_lang = None
            self._start_translation(pending)
        else:
            self.language_changed.emit(target_lang)

    def is_translation_ready(self, language: Optional[str] = None) -> bool:
        lang = language or self._language
        return lang in self._cache

    def is_translating(self) -> bool:
        return self._worker is not None and self._worker.isRunning()

    def get_cached_languages(self) -> Sequence[str]:
        return list(self._cache.keys())

    def preload_language(self, language: str) -> None:
        """Lädt Sprache vorab (ohne sie aktiv zu setzen)."""
        if language in LANGUAGE_NAMES and language not in self._cache:
            self._start_translation(language)


# ============================================================================
# GLOBALE INSTANZ & HILFSFUNKTIONEN
# ============================================================================

_translator_instance: Optional[Translator] = None


def get_translator() -> Translator:
    """Gibt die globale Translator-Instanz zurück."""
    global _translator_instance
    if _translator_instance is None:
        _translator_instance = Translator()
    return _translator_instance


def init_translator(
    language: str = DEFAULT_LANGUAGE,
    api=None,
    parent=None,
) -> Translator:
    """Initialisiert den globalen Translator."""
    global _translator_instance
    _translator_instance = Translator(language, api, parent)
    return _translator_instance


def t(key: str, **kwargs) -> str:
    """Kurzform für get_translator().t(key)."""
    return get_translator().t(key, **kwargs)
