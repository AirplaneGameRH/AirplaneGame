"""Startet die Anwendung und öffnet das Hauptfenster."""

import sys

from PyQt6.QtWidgets import QApplication

from src.main import main


def run_game():
    """Erzeugt die Qt-Anwendung und zeigt das Hauptfenster an."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("AirplaneGame")
    app.setQuitOnLastWindowClosed(True)

    window = main(app)
    window.show()
    window.raise_()
    window.activateWindow()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run_game())
