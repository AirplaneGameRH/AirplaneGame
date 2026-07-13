"""Hintergrundmusik-Verwaltung für das Spiel."""

from pathlib import Path

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

from .config import SOUNDS_DIR


class BackgroundMusic:
    """Spielt eine Hintergrundmusik-Datei in Dauerschleife ab."""

    def __init__(self, volume: float = 0.3):
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        self._player.setLoops(QMediaPlayer.Loops.Infinite)
        self._audio_output.setVolume(volume)
        self._loaded = False

        # Versuche verschiedene gängige Audioformate
        audio_files = [
            SOUNDS_DIR / "Backgroundmusic.mp3",
            SOUNDS_DIR / "Backgroundmusic.ogg",
            SOUNDS_DIR / "Backgroundmusic.wav",
            SOUNDS_DIR / "backgroundmusic.mp3",
            SOUNDS_DIR / "backgroundmusic.ogg",
            SOUNDS_DIR / "backgroundmusic.wav",
        ]

        for music_path in audio_files:
            if music_path.exists():
                self._player.setSource(QUrl.fromLocalFile(str(music_path)))
                self._loaded = True
                print(f"Audio geladen: {music_path}")
                break

        if not self._loaded:
            print("Warnung: Keine Hintergrundmusik-Datei gefunden in", SOUNDS_DIR)
            self._player = None

    def play(self) -> None:
        """Startet die Wiedergabe in Dauerschleife."""
        if self._player is not None and self._loaded:
            self._player.play()

    def stop(self) -> None:
        """Stoppt die Wiedergabe."""
        if self._player is not None:
            self._player.stop()

    def set_volume(self, volume: float) -> None:
        """Setzt die Lautstärke (0.0 - 1.0)."""
        if self._audio_output is not None:
            self._audio_output.setVolume(max(0.0, min(1.0, volume)))
