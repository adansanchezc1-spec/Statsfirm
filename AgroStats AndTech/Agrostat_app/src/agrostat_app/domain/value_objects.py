"""Domain Value Objects for Agrostat Data Science Core.

Immutable objects defining domain concepts without identity.
Normative:
- SWEBOK Chapter 2 (Software Design)
- Clean Code (Value Objects & Invariants)
- PEP 8 & Python Type Annotations
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DivipolaCode:
    """Represents an official DANE DIVIPOLA geographical classification."""
    codigo_mpio: str
    nombre_mpio: str
    codigo_depto: str
    nombre_depto: str

    def __post_init__(self) -> None:
        if not (self.codigo_mpio and len(str(self.codigo_mpio).strip()) >= 4):
            raise ValueError(f"Código DIVIPOLA de municipio inválido: {self.codigo_mpio}")

    def to_dict(self) -> Dict[str, str]:
        return {
            "codigo_mpio": self.codigo_mpio,
            "nombre_mpio": self.nombre_mpio,
            "codigo_depto": self.codigo_depto,
            "nombre_depto": self.nombre_depto,
        }


@dataclass(frozen=True)
class CpcProductCode:
    """Represents a product under Central Product Classification (CPC Ver. 2.1 A.C.)."""
    codigo_cpc: str
    nombre_producto: str
    grupo_cpc: str
    variedad: Optional[str] = None

    def __post_init__(self) -> None:
        if not (self.codigo_cpc and len(str(self.codigo_cpc).strip()) >= 3):
            raise ValueError(f"Código CPC inválido: {self.codigo_cpc}")

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "codigo_cpc": self.codigo_cpc,
            "nombre_producto": self.nombre_producto,
            "grupo_cpc": self.grupo_cpc,
            "variedad": self.variedad,
        }


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a single record against DAMA-BOK quality rules."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    rule_tag: str = "DAMA_BOK"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "rule_tag": self.rule_tag,
        }


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
class MarketForecastResult:
    """Represents a market price or demand forecast for agricultural planning."""
    codigo_cpc: str
    mercado_id: str
    horizonte_semanas: int
    fecha_proyeccion: date
    valor_proyectado: float
    intervalo_inferior_95: float
    intervalo_superior_95: float
    modelo_utilizado: str
    confianza_pct: float = 95.0
    tendencia: str = "ESTABLE"
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo_cpc": self.codigo_cpc,
            "mercado_id": self.mercado_id,
            "horizonte_semanas": self.horizonte_semanas,
            "fecha_proyeccion": self.fecha_proyeccion.isoformat(),
            "valor_proyectado": round(self.valor_proyectado, 2),
            "intervalo_95": {
                "inferior": round(self.intervalo_inferior_95, 2),
                "superior": round(self.intervalo_superior_95, 2),
            },
            "modelo_utilizado": self.modelo_utilizado,
            "confianza_pct": self.confianza_pct,
            "tendencia": self.tendencia,
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
