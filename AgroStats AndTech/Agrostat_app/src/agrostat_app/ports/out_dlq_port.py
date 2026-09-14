"""Outbound Port: Dead Letter Queue (DLQ) Port.

Defines persistence contract for quarantined invalid records.
Normative: DAMA-BOK / Hexagonal Architecture Driven Port.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DeadLetterQueuePort(ABC):
    """Driven Port defining persistence for rejected payloads requiring producer remediation."""

    @abstractmethod
    def send_to_quarantine(self, quarantined_records: List[Dict[str, Any]]) -> int:
        """Appends quarantined error records to the DLQ audit log."""
        pass

    @abstractmethod
    def get_quarantined_records(self) -> List[Dict[str, Any]]:
        """Retrieves quarantined items for remediation dashboards."""
        pass
