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

        music_path = SOUNDS_DIR / "Backgroundmusic.mp3"
        if music_path.exists():
            self._player.setSource(QUrl.fromLocalFile(str(music_path)))
        else:
            print(f"Warnung: Musikdatei nicht gefunden: {music_path}")
            self._player = None

    def play(self) -> None:
        """Startet die Wiedergabe in Dauerschleife."""
        if self._player is not None:
            self._player.play()

    def stop(self) -> None:
        """Stoppt die Wiedergabe."""
        if self._player is not None:
            self._player.stop()

    def set_volume(self, volume: float) -> None:
        """Setzt die Lautstärke (0.0 - 1.0)."""
        if self._audio_output is not None:
            self._audio_output.setVolume(max(0.0, min(1.0, volume)))
