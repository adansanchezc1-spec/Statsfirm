"""Value Objects de Dominio — AgroData Intelligence Platform (AgroStats).
Inmutables, autocontenidos y validados en inicialización.
Normativas: Clean Code / DDD / SWEBOK Cap. 2 / ISO 25010.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# -----------------------------------------------------------------------------
# 1. Códigos y Clasificaciones Oficiales Colombianas
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class CodigoCpc:
    codigo: str

    def __post_init__(self) -> None:
        if len(self.codigo.strip()) < 3:
            raise ValueError("El código CPC debe ser un identificador válido.")

    @property
    def valor(self) -> str:
        return self.codigo

    def to_dict(self) -> Dict[str, str]:
        return {"codigo": self.codigo}


CodigoCPC = CodigoCpc
CpcProductCode = CodigoCpc


@dataclass(frozen=True)
class CodigoDivipola:
    codigo_dane: str

    def __post_init__(self) -> None:
        if len(self.codigo_dane.strip()) != 5:
            raise ValueError("El código DIVIPOLA municipal debe tener exactamente 5 dígitos.")

    @property
    def valor(self) -> str:
        return self.codigo_dane

    @property
    def codigo_departamento(self) -> str:
        return self.codigo_dane[:2]

    @property
    def codigo_municipio(self) -> str:
        return self.codigo_dane[2:]

    def to_dict(self) -> Dict[str, str]:
        return {
            "codigo_completo": self.codigo_dane,
            "departamento": self.codigo_departamento,
            "municipio": self.codigo_municipio,
        }


DivipolaCode = CodigoDivipola


# -----------------------------------------------------------------------------
# 2. Magnitudes Económicas y Parámetros Bioeconómicos
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class DineroCOP:
    valor: float

    def __post_init__(self) -> None:
        if self.valor < 0:
            raise ValueError("El monto monetario no puede ser negativo.")

    @property
    def monto(self) -> float:
        return self.valor

    def formatear_millones(self) -> str:
        return f"${(self.valor / 1000000):.2f}M COP"

    def formatear_pesos(self) -> str:
        return f"${round(self.valor):,} COP".replace(",", ".")


@dataclass(frozen=True)
class RendimientoKgHa:
    kilos_por_hectarea: float

    def __post_init__(self) -> None:
        if self.kilos_por_hectarea <= 0:
            raise ValueError("El rendimiento físico por hectárea debe ser mayor a cero.")

    @property
    def valor(self) -> float:
        return self.kilos_por_hectarea


@dataclass(frozen=True)
class PorcentajeAdopcion:
    porcentaje: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.porcentaje <= 100.0):
            raise ValueError("El porcentaje de adopción debe estar comprendido entre 0.0 y 100.0.")

    @property
    def valor(self) -> float:
        return self.porcentaje

    @property
    def factor(self) -> float:
        return self.porcentaje / 100.0


# -----------------------------------------------------------------------------
# 3. Control Estadístico de Procesos (SPC) y Calidad
# -----------------------------------------------------------------------------
class NelsonRuleType(str, Enum):
    RULE_1 = "RULE_1"
    RULE_2 = "RULE_2"
    RULE_3 = "RULE_3"
    RULE_4 = "RULE_4"


@dataclass(frozen=True)
class NelsonViolation:
    rule_number: int
    rule_name: str
    sample_index: int
    observed_value: float
    expected_limit: float
    description: str
    detected_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_number": self.rule_number,
            "rule_name": self.rule_name,
            "sample_index": self.sample_index,
            "observed_value": round(self.observed_value, 2),
            "expected_limit": round(self.expected_limit, 2),
            "description": self.description,
            "detected_at": self.detected_at.isoformat(),
        }


@dataclass(frozen=True)
class SpcAnalysisResult:
    metric_name: str
    sample_count: int
    mean: float
    std_dev: float
    ucl: float
    lcl: float
    violations: List[NelsonViolation]
    is_in_control: bool
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "sample_count": self.sample_count,
            "mean": round(self.mean, 2),
            "std_dev": round(self.std_dev, 2),
            "ucl": round(self.ucl, 2),
            "lcl": round(self.lcl, 2),
            "is_in_control": self.is_in_control,
            "violations_count": len(self.violations),
            "violations": [v.to_dict() for v in self.violations],
            "calculated_at": self.calculated_at.isoformat(),
        }


# -----------------------------------------------------------------------------
# 4. Machine Learning, Inferencia y Calidad de Datos
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class YieldPrediction:
    predicted_yield_kg_ha: float
    confidence_lower_95: float
    confidence_upper_95: float
    model_version: str
    inference_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicted_yield_kg_ha": round(self.predicted_yield_kg_ha, 2),
            "confidence_lower_95": round(self.confidence_lower_95, 2),
            "confidence_upper_95": round(self.confidence_upper_95, 2),
            "model_version": self.model_version,
            "inference_id": self.inference_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True)
class MarketForecastResult:
    codigo_cpc: str
    mercado_id: str
    fechas: List[str]
    precios_proyectados: List[float]
    banda_inferior_95: List[float]
    banda_superior_95: List[float]
    volatilidad_historica_pct: float
    tendencia: str
    generado_en: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "codigo_cpc": self.codigo_cpc,
            "mercado_id": self.mercado_id,
            "fechas": self.fechas,
            "precios_proyectados": [round(p, 2) for p in self.precios_proyectados],
            "banda_inferior_95": [round(b, 2) for b in self.banda_inferior_95],
            "banda_superior_95": [round(b, 2) for b in self.banda_superior_95],
            "volatilidad_historica_pct": round(self.volatilidad_historica_pct, 2),
            "tendencia": self.tendencia,
            "generado_en": self.generado_en.isoformat(),
        }


@dataclass(frozen=True)
class DataQualityReport:
    total_records: int
    valid_records: int
    quarantined_records: int
    completeness_rate: float
    validity_rate: float
    consistency_rate: float
    uniqueness_rate: float
    evaluated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_production_grade(self) -> bool:
        return self.completeness_rate >= 0.95 and self.validity_rate >= 0.95

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "quarantined_records": self.quarantined_records,
            "completeness_pct": round(self.completeness_rate * 100, 2),
            "validity_pct": round(self.validity_rate * 100, 2),
            "consistency_pct": round(self.consistency_rate * 100, 2),
            "uniqueness_pct": round(self.uniqueness_rate * 100, 2),
            "is_production_grade": self.is_production_grade,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


@dataclass(frozen=True)
class BatchQualityMetric:
    dimension: str
    passed: bool
    field_name: str
    error_message: Optional[str] = None
