"""Outbound Port: External Source Extractor Port.

Defines abstraction for extracting datasets from external governmental and satellite APIs.
Normative: Hexagonal Architecture Driven Port / Dependency Inversion Principle.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List, Optional


class ExternalSourceExtractorPort(ABC):
    """Driven Port defining contract for governmental and satellite data extractors."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Returns unique identifier tag for the source (e.g., 'SIPSA_P', 'IDEAM_CLIMA')."""
        pass

    @abstractmethod
    def extract_records(
        self,
        fecha_inicio: date,
        fecha_fin: Optional[date] = None,
        limit: int = 1000,
    ) -> List[Dict[str, Any]]:
        """Extracts raw record payloads for a given date range.

        Args:
            fecha_inicio: Start date.
            fecha_fin: End date (defaults to fecha_inicio if None).
            limit: Maximum records to pull in this extraction.

        Returns:
            List of raw dictionaries as received from source API or fallback generator.
        """
        pass
