"""Use Case: End-to-End Integrated Data Science & Engineering Pipeline.

Master coordinator orchestrating the entire lifecycle:
Ingest (Bronze) -> Validate (DLQ/Silver) -> Train ML (Gold) -> Predict -> SPC Stability.
Normative: SWEBOK Chapter 2 / Data Engineering Pipeline Pattern.
"""

from datetime import datetime
import time
from typing import Any, Dict, List, Optional

from agrostat_app.application.dtos import EndToEndPipelineSummaryDTO, IngestionSummaryDTO, TrainingSummaryDTO
from agrostat_app.application.use_cases.predict_yield import PredictYieldUseCase
from agrostat_app.application.use_cases.run_ingestion_pipeline import RunIngestionPipelineUseCase
from agrostat_app.application.use_cases.run_spc_analysis import RunSPCAnalysisUseCase
from agrostat_app.application.use_cases.train_yield_model import TrainYieldModelUseCase
from agrostat_app.ports.out_notification_port import NotificationPort


class EndToEndDataPipelineUseCase:
    """Master pipeline orchestrator uniting ingestion, machine learning, and biostatistics."""

    def __init__(
        self,
        ingestion_uc: RunIngestionPipelineUseCase,
        training_uc: TrainYieldModelUseCase,
        prediction_uc: PredictYieldUseCase,
        spc_uc: RunSPCAnalysisUseCase,
        notifier: NotificationPort,
    ) -> None:
        self._ingestion_uc = ingestion_uc
        self._training_uc = training_uc
        self._prediction_uc = prediction_uc
        self._spc_uc = spc_uc
        self._notifier = notifier

    def run_pipeline(
        self,
        raw_dataset: List[Dict[str, Any]],
        source_tag: str = "farm_consolidated_batch",
        sample_batch_for_inference: Optional[Dict[str, Any]] = None,
    ) -> EndToEndPipelineSummaryDTO:
        """Executes the end-to-end data pipeline."""
        start_time = time.time()
        run_id = f"RUN-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

        self._notifier.send_alert(
            level="INFO",
            title="Iniciando Pipeline End-to-End",
            message=f"Ejecutando Run ID: {run_id} con {len(raw_dataset)} registros brutos.",
        )

        # FASE 1: Ingesta, Calidad y Almacenamiento Medallion
        ingestion_dict = self._ingestion_uc.execute_ingestion(raw_dataset, source_tag)
        ingestion_dto = IngestionSummaryDTO(
            source_tag=ingestion_dict["source_tag"],
            total_received=ingestion_dict["total_received"],
            valid_count=ingestion_dict["valid_count"],
            quarantined_count=ingestion_dict["quarantined_count"],
            bronze_storage_path=ingestion_dict["bronze_storage_path"],
            silver_records_persisted=ingestion_dict["silver_records_persisted"],
            completeness_pct=float(ingestion_dict["quality_rates"]["completeness"].replace("%", "")),
            validity_pct=float(ingestion_dict["quality_rates"]["validity"].replace("%", "")),
            consistency_pct=float(ingestion_dict["quality_rates"]["consistency"].replace("%", "")),
            is_production_ready=ingestion_dict["is_production_ready"],
        )

        # FASE 2: Entrenamiento y Registro de Modelo de Machine Learning
        training_dto = None
        if ingestion_dto.valid_count >= TrainYieldModelUseCase.MIN_TRAINING_SAMPLES:
            try:
                training_dict = self._training_uc.train_and_register(model_algorithm="random_forest")
                training_dto = TrainingSummaryDTO(
                    model_name=training_dict["model_name"],
                    version=training_dict["version"],
                    algorithm=training_dict["algorithm"],
                    total_samples=training_dict["sample_counts"]["total"],
                    train_samples=training_dict["sample_counts"]["train"],
                    test_samples=training_dict["sample_counts"]["test"],
                    r2_score=training_dict["evaluation_metrics"]["r2_score"],
                    rmse=training_dict["evaluation_metrics"]["rmse"],
                    mae=training_dict["evaluation_metrics"]["mae"],
                    mape=float(training_dict["evaluation_metrics"]["mape"].replace("%", "")),
                    is_registered=training_dict["is_registered"],
                    registry_path=training_dict["registry_path"],
                    feature_importances=training_dict["feature_importances"],
                )
            except Exception as exc:
                self._notifier.send_alert("WARNING", "Fallo en Entrenamiento ML", str(exc))

        # FASE 3: Inferencia de Prueba (si se suministra muestra o sobre el primer registro válido)
        predictions_count = 0
        if sample_batch_for_inference and training_dto:
            try:
                self._prediction_uc.predict_harvest_yield(sample_batch_for_inference)
                predictions_count = 1
            except Exception as exc:
                self._notifier.send_alert("WARNING", "Fallo en Inferencia", str(exc))

        # FASE 4: Auditoría Bioestadística SPC (Shewhart + Nelson)
        spc_summary = {}
        if ingestion_dto.valid_count >= 10:
            try:
                spc_limits = self._spc_uc.analyze_process_stability(metric_name="rendimiento_kg_ha")
                spc_summary = spc_limits.to_dict()
            except Exception as exc:
                spc_summary = {"error": str(exc)}

        duration = time.time() - start_time

        summary = EndToEndPipelineSummaryDTO(
            run_id=run_id,
            status="SUCCESS",
            ingestion=ingestion_dto,
            training=training_dto,
            spc_stability=spc_summary,
            predictions_generated=predictions_count,
            execution_duration_sec=duration,
        )

        self._notifier.send_alert(
            level="INFO",
            title="Pipeline End-to-End Finalizado",
            message=f"Run {run_id} completado en {duration:.2f} segundos.",
            metadata=summary.to_dict(),
        )

        return summary
