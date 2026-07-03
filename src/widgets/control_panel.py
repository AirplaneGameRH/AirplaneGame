"""
Control-Panel-Widget für Spielaktionen.

Dieses Widget enthält Buttons und Eingabefelder für Kaufen, Reparieren,
Werbung und Flugplanung.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ControlPanelWidget(QWidget):
    """Repräsentiert das Aktionspanel der Spieloberfläche."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Control Panel"))
        self.setLayout(layout)
