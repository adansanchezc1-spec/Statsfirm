"""Application Data Transfer Objects (DTOs).

Structures crossing application boundary without domain logic.
Normative: SWEBOK Chapter 2 / Clean Architecture Application Layer.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class IngestionSummaryDTO:
    """Summary of data ingestion, validation, and storage routing."""
    source_tag: str
    total_received: int
    valid_count: int
    quarantined_count: int
    bronze_storage_path: str
    silver_records_persisted: int
    completeness_pct: float
    validity_pct: float
    consistency_pct: float
    is_production_ready: bool
    quarantine_diagnostic: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_tag": self.source_tag,
            "total_received": self.total_received,
            "valid_count": self.valid_count,
            "quarantined_count": self.quarantined_count,
            "bronze_storage_path": self.bronze_storage_path,
            "silver_records_persisted": self.silver_records_persisted,
            "quality_rates": {
                "completeness": f"{self.completeness_pct:.1f}%",
                "validity": f"{self.validity_pct:.1f}%",
                "consistency": f"{self.consistency_pct:.1f}%",
            },
            "is_production_ready": self.is_production_ready,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TrainingSummaryDTO:
    """Summary of model training, evaluation, and registry tracking."""
    model_name: str
    version: str
    algorithm: str
    total_samples: int
    train_samples: int
    test_samples: int
    r2_score: float
    rmse: float
    mae: float
    mape: float
    is_registered: bool
    registry_path: str
    feature_importances: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "version": self.version,
            "algorithm": self.algorithm,
            "sample_counts": {
                "total": self.total_samples,
                "train": self.train_samples,
                "test": self.test_samples,
            },
            "evaluation_metrics": {
                "r2_score": round(self.r2_score, 4),
                "rmse": round(self.rmse, 2),
                "mae": round(self.mae, 2),
                "mape": f"{self.mape:.2f}%",
            },
            "is_registered": self.is_registered,
            "registry_path": self.registry_path,
            "feature_importances": self.feature_importances,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class EndToEndPipelineSummaryDTO:
    """Summary of the complete end-to-end data science pipeline run."""
    run_id: str
    status: str
    ingestion: IngestionSummaryDTO
    training: Optional[TrainingSummaryDTO]
    spc_stability: Dict[str, Any]
    predictions_generated: int
    execution_duration_sec: float
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "execution_duration_seconds": round(self.execution_duration_sec, 3),
            "ingestion": self.ingestion.to_dict(),
            "training": self.training.to_dict() if self.training else None,
            "spc_stability": self.spc_stability,
            "predictions_generated": self.predictions_generated,
            "timestamp": self.timestamp.isoformat(),
        }
