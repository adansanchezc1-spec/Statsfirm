"""Inbound Port: Ingestion Pipeline Port.

Defines the contract for ingesting raw harvest datasets into the system.
Normative: Hexagonal Architecture Driving Port / SWEBOK Chapter 2.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IngestionPipelinePort(ABC):
    """Driving Port defining the entry point for dataset ingestion and quality validation."""

    @abstractmethod
    def execute_ingestion(
        self, raw_records: List[Dict[str, Any]], source_tag: str = "field_manual_upload"
    ) -> Dict[str, Any]:
        """Executes ingestion, applies DAMA-BOK contracts, routes valid records to Bronze/Silver,

        and routes invalid records to the Dead Letter Queue.
        """
        pass
