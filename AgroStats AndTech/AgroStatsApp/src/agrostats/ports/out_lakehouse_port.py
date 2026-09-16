"""Outbound Port: DuckDB Medallion Lakehouse Repository Port.

Defines persistence contracts for Bronze (Raw Inmutable), Silver (Curated DAMA-BOK),
and Gold (Star Schema Data Warehouse in DuckDB).
Normative: Hexagonal Architecture Driven Port / Dependency Inversion Principle.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, List, Optional

from agrostat_app.domain.entities import (
    CotizacionMayorista,
    HarvestBatch,
    ObservacionClimatica,
    RegistroAbastecimiento,
)


class LakehouseRepositoryPort(ABC):
    """Driven Port defining persistence contracts across the Medallion architecture."""

    @abstractmethod
    def save_bronze_records(self, raw_records: List[Dict[str, Any]], source_tag: str) -> str:
        """Stores immutable raw records in the Bronze layer with audit metadata and SHA-256 hash."""
        pass

    @abstractmethod
    def save_cotizaciones_silver(self, cotizaciones: List[CotizacionMayorista]) -> int:
        """Persists validated wholesale price quotations into the Silver layer."""
        pass

    @abstractmethod
    def save_abastecimiento_silver(self, abastecimientos: List[RegistroAbastecimiento]) -> int:
        """Persists validated food supply records into the Silver layer."""
        pass

    @abstractmethod
    def save_clima_silver(self, observaciones: List[ObservacionClimatica]) -> int:
        """Persists validated meteorological observations into the Silver layer."""
        pass

    @abstractmethod
    def upsert_gold_facts(self) -> Dict[str, int]:
        """Loads and updates dimensional Gold fact tables from Silver data."""
        pass

    @abstractmethod
    def query_dimensional_dw(
        self, sql_query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes analytical SQL queries against the DuckDB Data Warehouse."""
        pass

    @abstractmethod
    def get_historical_prices(
        self, codigo_cpc: str, mercado_id: str, limit_weeks: int = 12
    ) -> List[Dict[str, Any]]:
        """Retrieves aggregated historical prices for statistical forecasting."""
        pass

    @abstractmethod
    def get_market_balance_view(
        self, mercado_id: Optional[str] = None, codigo_cpc: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries the weekly supply-demand balance analytical view."""
        pass
