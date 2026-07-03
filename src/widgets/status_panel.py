"""
Status-Panel-Widget für Live-Informationen.

Dieses Widget zeigt laufende Flüge, Wartungsstatus und Flughafen-Events an.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class StatusPanelWidget(QWidget):
    """Repräsentiert ein Status-Panel für Live-Updates."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Status Panel"))
        self.setLayout(layout)
