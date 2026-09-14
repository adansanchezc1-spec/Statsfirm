"""Outbound Port: Medallion Lakehouse Repository Port.

Defines persistence contracts for Bronze (Raw), Silver (Curated), and Gold (Analytical Data Marts).
Normative: Hexagonal Architecture Driven Port / Dependency Inversion Principle.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from agrostat_app.domain.entities import HarvestBatch


class HarvestRepositoryPort(ABC):
    """Driven Port defining abstraction over the Medallion Lakehouse persistence."""

    @abstractmethod
    def save_bronze_records(self, raw_records: List[Dict[str, Any]], source_tag: str) -> str:
        """Stores immutable raw records in the Bronze layer."""
        pass

    @abstractmethod
    def save_silver_batches(self, batches: List[HarvestBatch]) -> int:
        """Stores clean, validated entity records in the Silver layer."""
        pass

    @abstractmethod
    def get_silver_batches(self, lote_id: Optional[str] = None) -> List[HarvestBatch]:
        """Retrieves verified harvest entities from the Silver layer."""
        pass

    @abstractmethod
    def save_gold_features(self, feature_rows: List[Dict[str, Any]], table_name: str) -> str:
        """Stores aggregated feature store / data mart metrics in the Gold layer."""
        pass
