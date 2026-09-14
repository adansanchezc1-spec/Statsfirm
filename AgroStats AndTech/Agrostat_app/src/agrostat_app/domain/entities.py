"""Domain Entities for Agrostat Data Science Core.

Rich Domain Model with business invariants and computational capabilities.
Normative:
- Clean Code (Entities with Behavior, Anti-Anemic Domain Model)
- SWEBOK Chapter 2 (Software Design)
- ISO/IEC 25010 (Functional Suitability & Reliability)
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from agrostat_app.domain.exceptions import InvariantViolationException
from agrostat_app.domain.value_objects import NelsonViolation


@dataclass
class HarvestBatch:
    """Represents a validated harvest batch entity within an agricultural plot (lote)."""
    batch_id: str
    lote_id: str
    fecha_cosecha: date
    hectareas_lote: float
    kilos_totales: float
    kilos_exportables: float
    calibre_promedio: float
    grados_brix: float
    responsable_registro: str
    ph_suelo: Optional[float] = None
    humedad_relativa: Optional[float] = None
    precipitacion_mm: Optional[float] = None
    temperatura_celsius: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        self.validate_invariants()

    def validate_invariants(self) -> None:
        """Validates fundamental domain invariants (pre-conditions)."""
        if self.hectareas_lote <= 0:
            raise InvariantViolationException(
                f"Las hectáreas del lote deben ser positivas. Valor recibido: {self.hectareas_lote}"
            )
        if self.kilos_totales <= 0:
            raise InvariantViolationException(
                f"Los kilos totales deben ser mayores a cero. Valor recibido: {self.kilos_totales}"
            )
        if self.kilos_exportables < 0:
            raise InvariantViolationException(
                f"Los kilos exportables no pueden ser negativos. Valor recibido: {self.kilos_exportables}"
            )
        if self.kilos_exportables > self.kilos_totales:
            raise InvariantViolationException(
                f"Invariante violada: kilos exportables ({self.kilos_exportables}) "
                f"supera los kilos totales cosechados ({self.kilos_totales})"
            )
        if self.calibre_promedio <= 0:
            raise InvariantViolationException(
                f"El calibre promedio debe ser mayor a cero. Valor recibido: {self.calibre_promedio}"
            )
        if self.grados_brix < 0:
            raise InvariantViolationException(
                f"Los grados brix no pueden ser negativos. Valor recibido: {self.grados_brix}"
            )

    @property
    def rendimiento_kg_ha(self) -> float:
        """Calculates harvest yield in kg per hectare."""
        return round(self.kilos_totales / self.hectareas_lote, 2)

    @property
    def tasa_exportabilidad(self) -> float:
        """Calculates exportable ratio percentage (0.0 to 1.0)."""
        if self.kilos_totales == 0:
            return 0.0
        return round(self.kilos_exportables / self.kilos_totales, 4)

    @property
    def ratio_brix_calibre(self) -> float:
        """Agronomic maturity index: soluble solids / fruit caliber."""
        return round(self.grados_brix / self.calibre_promedio, 4)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes entity to dictionary."""
        return {
            "batch_id": self.batch_id,
            "lote_id": self.lote_id,
            "fecha_cosecha": self.fecha_cosecha.isoformat(),
            "hectareas_lote": self.hectareas_lote,
            "kilos_totales": self.kilos_totales,
            "kilos_exportables": self.kilos_exportables,
            "calibre_promedio": self.calibre_promedio,
            "grados_brix": self.grados_brix,
            "ph_suelo": self.ph_suelo,
            "humedad_relativa": self.humedad_relativa,
            "precipitacion_mm": self.precipitacion_mm,
            "temperatura_celsius": self.temperatura_celsius,
            "responsable_registro": self.responsable_registro,
            "rendimiento_kg_ha": self.rendimiento_kg_ha,
            "tasa_exportabilidad": self.tasa_exportabilidad,
            "ratio_brix_calibre": self.ratio_brix_calibre,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HarvestBatch":
        """Constructs an entity instance from dictionary representation."""
        raw_date = data["fecha_cosecha"]
        if isinstance(raw_date, str):
            parsed_date = date.fromisoformat(raw_date)
        elif isinstance(raw_date, datetime):
            parsed_date = raw_date.date()
        else:
            parsed_date = raw_date

        return cls(
            batch_id=str(data["batch_id"]),
            lote_id=str(data["lote_id"]),
            fecha_cosecha=parsed_date,
            hectareas_lote=float(data["hectareas_lote"]),
            kilos_totales=float(data["kilos_totales"]),
            kilos_exportables=float(data.get("kilos_exportables", 0.0)),
            calibre_promedio=float(data["calibre_promedio"]),
            grados_brix=float(data["grados_brix"]),
            responsable_registro=str(data.get("responsable_registro", "Operario Agronómico")),
            ph_suelo=float(data["ph_suelo"]) if data.get("ph_suelo") is not None else None,
            humedad_relativa=float(data["humedad_relativa"]) if data.get("humedad_relativa") is not None else None,
            precipitacion_mm=float(data["precipitacion_mm"]) if data.get("precipitacion_mm") is not None else None,
            temperatura_celsius=float(data["temperatura_celsius"]) if data.get("temperatura_celsius") is not None else None,
        )


@dataclass
class SPCControlLimits:
    """Represents calculated Shewhart statistical process control limits."""
    metric_name: str
    sample_count: int
    mean_center_line: float
    standard_deviation: float
    ucl: float  # Upper Control Limit (mu + 3 sigma)
    lcl: float  # Lower Control Limit (max(0, mu - 3 sigma))
    one_sigma_upper: float
    one_sigma_lower: float
    two_sigma_upper: float
    two_sigma_lower: float
    cp_index: float
    cpk_index: float
    is_in_statistical_control: bool
    violations: List[NelsonViolation] = field(default_factory=list)
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_capable_process(self) -> bool:
        """Process is capable if Cpk >= 1.33 (Industrial quality benchmark)."""
        return self.cpk_index >= 1.33

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "sample_count": self.sample_count,
            "center_line_mean": round(self.mean_center_line, 4),
            "standard_deviation": round(self.standard_deviation, 4),
            "limits": {
                "ucl": round(self.ucl, 4),
                "lcl": round(self.lcl, 4),
                "one_sigma": {"upper": round(self.one_sigma_upper, 4), "lower": round(self.one_sigma_lower, 4)},
                "two_sigma": {"upper": round(self.two_sigma_upper, 4), "lower": round(self.two_sigma_lower, 4)},
            },
            "capability": {
                "cp_index": round(self.cp_index, 4),
                "cpk_index": round(self.cpk_index, 4),
                "is_capable": self.is_capable_process,
            },
            "is_in_statistical_control": self.is_in_statistical_control,
            "violations_count": len(self.violations),
            "violations": [v.to_dict() for v in self.violations],
            "calculated_at": self.calculated_at.isoformat(),
        }
