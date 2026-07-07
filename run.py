"""Startet die Anwendung und öffnet das Hauptfenster."""

import os
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.config import ICON_PATHS
from src.main import main


def _apply_app_icon(app):
    """Setzt das Anwendungsicon für Fenster und Taskleiste."""
    for icon_path in ICON_PATHS:
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                app.setWindowIcon(icon)
                return


def _launch_with_pythonw():
    """Startet die GUI auf Windows über pythonw, damit die Taskleiste das eigene Icon nutzt."""
    if os.name != "nt":
        return False

    python_exe = sys.executable
    if not python_exe.lower().endswith("python.exe"):
        return False

    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    if not Path(pythonw_exe).exists():
        return False

    os.execv(pythonw_exe, [pythonw_exe, str(Path(__file__).resolve()), *sys.argv[1:]])
    return True


def run_game():
    """Erzeugt die Qt-Anwendung und zeigt das Hauptfenster an."""
    if _launch_with_pythonw():
        return 0

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
