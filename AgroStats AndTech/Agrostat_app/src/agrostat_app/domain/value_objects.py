"""Domain Value Objects for Agrostat Data Science Core.

Immutable objects defining domain concepts without identity.
Normative:
- SWEBOK Chapter 2 (Software Design)
- Clean Code (Value Objects & Invariants)
- PEP 8 & Python Type Annotations
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class NelsonViolation:
    """Represents a statistical process anomaly detected by Nelson Rules."""
    rule_number: int
    rule_name: str
    sample_index: int
    observed_value: float
    expected_limit: float
    description: str
    detected_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, object]:
        return {
            "rule_number": self.rule_number,
            "rule_name": self.rule_name,
            "sample_index": self.sample_index,
            "observed_value": round(self.observed_value, 4),
            "expected_limit": round(self.expected_limit, 4),
            "description": self.description,
            "detected_at": self.detected_at.isoformat(),
        }


@dataclass(frozen=True)
class YieldPrediction:
    """Represents an inferenced harvest yield forecast with confidence intervals."""
    lote_id: str
    predicted_yield_kg: float
    predicted_yield_kg_ha: float
    lower_bound_95: float
    upper_bound_95: float
    r2_score: float
    mape_score: float
    model_version: str
    feature_contributions: Dict[str, float] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, object]:
        return {
            "lote_id": self.lote_id,
            "predicted_yield_kg": round(self.predicted_yield_kg, 2),
            "predicted_yield_kg_ha": round(self.predicted_yield_kg_ha, 2),
            "interval_95": {
                "lower": round(self.lower_bound_95, 2),
                "upper": round(self.upper_bound_95, 2),
            },
            "metrics": {
                "r2_score": round(self.r2_score, 4),
                "mape_score": round(self.mape_score, 4),
            },
            "model_version": self.model_version,
            "feature_contributions": self.feature_contributions,
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass(frozen=True)
class DataQualityReport:
    """Audit report reflecting DAMA-BOK data quality dimensions."""
    total_records: int
    valid_records: int
    quarantined_records: int
    completeness_rate: float
    validity_rate: float
    consistency_rate: float
    validation_errors: List[Dict[str, object]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_production_ready(self) -> bool:
        """Determines if the dataset meets threshold for analytical model consumption."""
        return (
            self.completeness_rate >= 0.95
            and self.validity_rate >= 0.95
            and self.consistency_rate >= 0.98
        )

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "quarantined_records": self.quarantined_records,
            "rates": {
                "completeness": round(self.completeness_rate * 100, 2),
                "validity": round(self.validity_rate * 100, 2),
                "consistency": round(self.consistency_rate * 100, 2),
            },
            "is_production_ready": self.is_production_ready,
            "errors_count": len(self.validation_errors),
            "generated_at": self.generated_at.isoformat(),
        }
