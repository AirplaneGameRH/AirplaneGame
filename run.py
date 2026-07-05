"""Startet die Anwendung und öffnet das Hauptfenster."""

import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.main import main


def _apply_app_icon(app):
    """Setzt das Anwendungsicon für Fenster und Taskleiste."""
    icon_paths = (
        Path(__file__).resolve().parent / "Images" / "AirplaneGameICO.ico",
        Path(__file__).resolve().parent / "Images" / "AirplaneGameICO.png",
        Path(__file__).resolve().parent / "Images" / "AirplaneGame.png",
    )
    for icon_path in icon_paths:
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                app.setWindowIcon(icon)
                return


def run_game():
    """Erzeugt die Qt-Anwendung und zeigt das Hauptfenster an."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("AirplaneGame")
    _apply_app_icon(app)
    app.setQuitOnLastWindowClosed(True)

    window = main(app)
    window.show()
    window.raise_()
    window.activateWindow()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run_game())
