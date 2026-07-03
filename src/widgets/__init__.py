"""
Widgets-Paket für UI-Komponenten.

Dieses Paket enthält wiederverwendbare Widgets und UI-Elemente für das Spiel.
"""

from .dashboard import DashboardWidget
from .control_panel import ControlPanelWidget
from .status_panel import StatusPanelWidget

__all__ = ["DashboardWidget", "ControlPanelWidget", "StatusPanelWidget"]
