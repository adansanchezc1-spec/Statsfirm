"""Outbound Port: Notification and Telemetry Port.

Defines contracts for dispatching alerts, audit logs, and anomaly warnings.
Normative: Hexagonal Architecture Driven Port / Observer Pattern.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class NotificationPort(ABC):
    """Driven Port defining abstraction for telemetry, alerts and logging."""

    @abstractmethod
    def send_alert(
        self,
        level: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Dispatches structured notification (INFO, WARNING, CRITICAL)."""
        pass

    def notify_info(self, message: str, title: str = "PIPELINE") -> None:
        """Helper to dispatch INFO alert."""
        self.send_alert("INFO", title, message)

    def notify_warning(self, message: str, title: str = "PIPELINE") -> None:
        """Helper to dispatch WARNING alert."""
        self.send_alert("WARNING", title, message)

    def notify_error(self, message: str, title: str = "PIPELINE") -> None:
        """Helper to dispatch CRITICAL alert."""
        self.send_alert("CRITICAL", title, message)
