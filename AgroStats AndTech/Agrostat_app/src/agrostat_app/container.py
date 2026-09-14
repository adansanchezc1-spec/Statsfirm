"""Dependency Injection Container (Bootstrap / Composition Root).

Assembles domain services, driven adapters, and use cases adhering to the Dependency Inversion Principle.
Normative: SWEBOK Chapter 2 (Software Design Patterns - Dependency Injection).
"""

from pathlib import Path
from typing import Optional

from agrostat_app.adapters.driven.console_notifier import ConsoleTelemetryAdapter
from agrostat_app.adapters.driven.json_dlq_adapter import JsonDeadLetterQueueAdapter
from agrostat_app.adapters.driven.parquet_repository import ParquetLakehouseRepository
from agrostat_app.adapters.driven.sklearn_registry import SklearnModelRegistryAdapter
from agrostat_app.application.use_cases.end_to_end_pipeline import EndToEndDataPipelineUseCase
from agrostat_app.application.use_cases.predict_yield import PredictYieldUseCase
from agrostat_app.application.use_cases.run_ingestion_pipeline import RunIngestionPipelineUseCase
from agrostat_app.application.use_cases.run_spc_analysis import RunSPCAnalysisUseCase
from agrostat_app.application.use_cases.train_yield_model import TrainYieldModelUseCase
from agrostat_app.config import Config
from agrostat_app.domain.services.biostatistical_engine import BioStatisticalEngine
from agrostat_app.domain.services.data_quality_validator import DataQualityValidator
from agrostat_app.domain.services.feature_engineering import FeatureEngineeringService


class Container:
    """Composition Root instantiating and wiring all hexagonal layers."""

    def __init__(self, custom_data_dir: Optional[Path] = None) -> None:
        data_dir = custom_data_dir or Config.DATA_DIR
        data_dir.mkdir(parents=True, exist_ok=True)

        # 1. Driven Adapters (Infraestructura de Salida)
        self.repository = ParquetLakehouseRepository(base_data_dir=data_dir)
        self.dlq = JsonDeadLetterQueueAdapter(dlq_dir=data_dir / "dlq")
        self.registry = SklearnModelRegistryAdapter(models_base_dir=data_dir / "models")
        self.notifier = ConsoleTelemetryAdapter()

        # 2. Domain Services (Lógica Pura de Negocio)
        self.validator = DataQualityValidator()
        self.spc_engine = BioStatisticalEngine()
        self.feature_service = FeatureEngineeringService()

        # 3. Application Use Cases (Orquestación del Pipeline)
        self.ingestion_use_case = RunIngestionPipelineUseCase(
            validator=self.validator,
            repository=self.repository,
            dlq=self.dlq,
            notifier=self.notifier,
        )

        self.training_use_case = TrainYieldModelUseCase(
            repository=self.repository,
            feature_service=self.feature_service,
            registry=self.registry,
            notifier=self.notifier,
        )

        self.prediction_use_case = PredictYieldUseCase(
            registry=self.registry,
            feature_service=self.feature_service,
            notifier=self.notifier,
        )

        self.spc_use_case = RunSPCAnalysisUseCase(
            repository=self.repository,
            spc_engine=self.spc_engine,
            notifier=self.notifier,
        )

        self.pipeline_use_case = EndToEndDataPipelineUseCase(
            ingestion_uc=self.ingestion_use_case,
            training_uc=self.training_use_case,
            prediction_uc=self.prediction_use_case,
            spc_uc=self.spc_use_case,
            notifier=self.notifier,
        )


def create_container(custom_data_dir: Optional[Path] = None) -> Container:
    """Factory helper creating an assembled hexagonal container."""
    return Container(custom_data_dir=custom_data_dir)
