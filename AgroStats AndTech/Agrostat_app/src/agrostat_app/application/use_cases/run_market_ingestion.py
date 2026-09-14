"""Application Use Case: Run Market & Climate Ingestion Pipeline.

Orchestrates the ingestion, DAMA-BOK curation, Dead Letter Queue quarantine,
Silver persistence, and Gold DuckDB refresh for Colombian agricultural markets.
Normative: SWEBOK Chapter 2 / Clean Code / ISO/IEC 25010.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from agrostat_app.domain.services.data_quality_validator import DataQualityValidator
from agrostat_app.domain.value_objects import DataQualityReport
from agrostat_app.ports.out_dlq_port import DeadLetterQueuePort
from agrostat_app.ports.out_lakehouse_port import LakehouseRepositoryPort
from agrostat_app.ports.out_notification_port import NotificationPort
from agrostat_app.ports.out_source_extractor_port import ExternalSourceExtractorPort


@dataclass
class MarketIngestionResult:
    """Consolidated summary of the daily market ingestion execution."""
    execution_id: str
    target_date: str
    bronze_paths: List[str]
    sipsa_prices_curated: int
    ideam_climate_curated: int
    quarantined_total: int
    gold_facts_updated: Dict[str, int]
    prices_quality_report: Dict[str, Any]
    climate_quality_report: Dict[str, Any]
    duration_seconds: float
    completed_at: str


class RunMarketIngestionUseCase:
    """Use case coordinating multi-source ingestion and Medallion Lakehouse loading."""

    def __init__(
        self,
        sipsa_extractor: ExternalSourceExtractorPort,
        ideam_extractor: ExternalSourceExtractorPort,
        lakehouse_repo: LakehouseRepositoryPort,
        dlq_adapter: DeadLetterQueuePort,
        validator: DataQualityValidator,
        notifier: NotificationPort,
    ) -> None:
        self._sipsa = sipsa_extractor
        self._ideam = ideam_extractor
        self._repo = lakehouse_repo
        self._dlq = dlq_adapter
        self._validator = validator
        self._notifier = notifier

    def execute(self, target_date: Optional[date] = None, record_limit: int = 100) -> MarketIngestionResult:
        """Executes full ingestion and curation pipeline for a target date."""
        start_time = datetime.utcnow()
        t_date = target_date or start_time.date()
        exec_id = f"exec_mkt_{t_date.strftime('%Y%m%d')}_{int(start_time.timestamp())}"

        self._notifier.notify_info(
            f"Iniciando Ingesta y Curaduría de Mercado para {t_date.isoformat()} (ID: {exec_id})"
        )

        bronze_files: List[str] = []

        # 1. Extracción e Ingesta Capa Bronze
        raw_sipsa = self._sipsa.extract_records(t_date, t_date, limit=record_limit)
        bronze_sipsa_path = self._repo.save_bronze_records(raw_sipsa, "SIPSA_P")
        bronze_files.append(bronze_sipsa_path)

        raw_ideam = self._ideam.extract_records(t_date, t_date, limit=record_limit // 2)
        bronze_ideam_path = self._repo.save_bronze_records(raw_ideam, "IDEAM_CLIMA")
        bronze_files.append(bronze_ideam_path)

        # 2. Curaduría DAMA-BOK Precios SIPSA
        valid_cotizaciones, sipsa_quarantined, sipsa_report = self._validator.validate_cotizaciones_stream(raw_sipsa)
        if sipsa_quarantined:
            self._dlq.send_to_quarantine(sipsa_quarantined)

        # 3. Curaduría DAMA-BOK Clima IDEAM
        valid_clima, clima_quarantined, clima_report = self._validator.validate_clima_stream(raw_ideam)
        if clima_quarantined:
            self._dlq.send_to_quarantine(clima_quarantined)

        # 4. Persistencia en Capa Silver
        sipsa_saved = self._repo.save_cotizaciones_silver(valid_cotizaciones)
        clima_saved = self._repo.save_clima_silver(valid_clima)

        # 5. Carga y refresco dimensional en Capa Gold (DuckDB)
        gold_counts = self._repo.upsert_gold_facts()

        duration = (datetime.utcnow() - start_time).total_seconds()
        total_quarantined = len(sipsa_quarantined) + len(clima_quarantined)

        result = MarketIngestionResult(
            execution_id=exec_id,
            target_date=t_date.isoformat(),
            bronze_paths=bronze_files,
            sipsa_prices_curated=sipsa_saved,
            ideam_climate_curated=clima_saved,
            quarantined_total=total_quarantined,
            gold_facts_updated=gold_counts,
            prices_quality_report=sipsa_report.to_dict(),
            climate_quality_report=clima_report.to_dict(),
            duration_seconds=round(duration, 3),
            completed_at=datetime.utcnow().isoformat(),
        )

        self._notifier.notify_info(
            f"Ingesta completada en {result.duration_seconds}s. Precios Silver: {sipsa_saved}, "
            f"Clima Silver: {clima_saved}, Cuarentena DLQ: {total_quarantined} registros."
        )

        return result
