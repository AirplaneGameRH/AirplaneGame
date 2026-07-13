"""Startet die Anwendung und öffnet das Hauptfenster."""

import ctypes
import os
import platform
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.config import ICON_PATHS
from src.main import main


def _set_windows_taskbar_icon():
    """Setzt das AppUserModelId auf Windows für die korrekte Taskbar-Anzeige."""
    if platform.system() != "Windows":
        return
    
    try:
        # Set AppUserModelId für die Taskbar auf Windows
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AirplaneGame.AirplaneGame")
    except (AttributeError, OSError):
        # Fehlerbehandlung falls SetCurrentProcessExplicitAppUserModelID nicht verfügbar ist
        pass


def _apply_app_icon(app):
    """Setzt das Anwendungsicon für Fenster und Taskleiste."""
    for icon_path in ICON_PATHS:
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                app.setWindowIcon(icon)
                return


def _configure_qt():
    """Konfiguriert Qt für plattformübergreifendes Verhalten."""
    if QApplication.instance() is None:
        from PyQt6.QtCore import Qt
        import os

        # High DPI Scaling (Qt6 hat dies standardmäßig aktiviert, aber explizit setzen schadet nicht)
        if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

        # Linux/Wayland: Force X11 backend falls Wayland Probleme macht
        if platform.system() == "Linux":
            if os.environ.get("XDG_SESSION_TYPE") == "wayland":
                # Qt auf Wayland kann Probleme mit Fullscreen haben
                os.environ.setdefault("QT_QPA_PLATFORM", "xcb")


def _launch_with_pythonw():
    """Startet die GUI auf Windows über pythonw, damit die Taskleiste das eigene Icon nutzt."""
    if platform.system() != "Windows":
        return False

    python_exe = Path(sys.executable)
    if python_exe.name.lower() != "python.exe":
        return False

    pythonw_exe = python_exe.with_name("pythonw.exe")
    if not pythonw_exe.exists():
        return False

    os.execv(str(pythonw_exe), [str(pythonw_exe), str(Path(__file__).resolve()), *sys.argv[1:]])
    return True


def run_game():
    """Erzeugt die Qt-Anwendung und zeigt das Hauptfenster an."""
    _set_windows_taskbar_icon()
    if _launch_with_pythonw():
        return 0

    _configure_qt()
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("AirplaneGame")
    app.setApplicationVersion("1.0")
    _apply_app_icon(app)
    app.setQuitOnLastWindowClosed(True)

    window = main(app)
    window.show()
    window.raise_()
    window.activateWindow()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run_game())
