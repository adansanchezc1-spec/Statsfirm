"""Use Case: Run Ingestion and Quality Validation Pipeline.

Implements IngestionPipelinePort.
Orchestrates Bronze storage, DAMA-BOK quality validation, DLQ routing, and Silver curation.
Normative: SWEBOK Chapter 2 / Hexagonal Application Layer.
"""

from typing import Any, Dict, List

from agrostat_app.application.dtos import IngestionSummaryDTO
from agrostat_app.domain.services.data_quality_validator import DataQualityValidator
from agrostat_app.ports.in_ingestion_port import IngestionPipelinePort
from agrostat_app.ports.out_dlq_port import DeadLetterQueuePort
from agrostat_app.ports.out_notification_port import NotificationPort
from agrostat_app.ports.out_repository_port import HarvestRepositoryPort


class RunIngestionPipelineUseCase(IngestionPipelinePort):
    """Use Case coordinating raw data ingestion, quality audits, and storage routing."""

    def __init__(
        self,
        validator: DataQualityValidator,
        repository: HarvestRepositoryPort,
        dlq: DeadLetterQueuePort,
        notifier: NotificationPort,
    ) -> None:
        self._validator = validator
        self._repository = repository
        self._dlq = dlq
        self._notifier = notifier

    def execute_ingestion(
        self, raw_records: List[Dict[str, Any]], source_tag: str = "field_manual_upload"
    ) -> Dict[str, Any]:
        """Runs the complete ingestion pipeline on incoming raw records."""
        self._notifier.send_alert(
            level="INFO",
            title="Iniciando Pipeline de Ingesta",
            message=f"Procesando lote de {len(raw_records)} registros con tag '{source_tag}'",
        )

        # 1. Almacenamiento Inmutable en Capa Bronze (Raw Storage)
        bronze_path = self._repository.save_bronze_records(raw_records, source_tag)

        # 2. Evaluación de Contratos DAMA-BOK mediante Servicio de Dominio
        valid_batches, quarantined, report = self._validator.validate_batch_stream(raw_records)

        # 3. Enrutamiento de anomalías a Dead Letter Queue (DLQ)
        if quarantined:
            self._dlq.send_to_quarantine(quarantined)
            self._notifier.send_alert(
                level="WARNING",
                title="Registros Rechazados a Cuarentena (DLQ)",
                message=f"{len(quarantined)} registros no superaron contratos DAMA-BOK",
                metadata={"quarantined_count": len(quarantined)},
            )

        # 4. Almacenamiento de Entidades Curadas en Capa Silver
        silver_saved = 0
        if valid_batches:
            silver_saved = self._repository.save_silver_batches(valid_batches)

        summary = IngestionSummaryDTO(
            source_tag=source_tag,
            total_received=len(raw_records),
            valid_count=len(valid_batches),
            quarantined_count=len(quarantined),
            bronze_storage_path=bronze_path,
            silver_records_persisted=silver_saved,
            completeness_pct=report.completeness_rate * 100,
            validity_pct=report.validity_rate * 100,
            consistency_pct=report.consistency_rate * 100,
            is_production_ready=report.is_production_ready,
            quarantine_diagnostic=quarantined[:10],  # Primeros 10 para diagnóstico
        )

        self._notifier.send_alert(
            level="INFO",
            title="Ingesta Concluida Exitosamente",
            message=f"Válidos: {len(valid_batches)} | Cuarentena: {len(quarantined)} | Silver: {silver_saved}",
            metadata=summary.to_dict(),
        )

        return summary.to_dict()
