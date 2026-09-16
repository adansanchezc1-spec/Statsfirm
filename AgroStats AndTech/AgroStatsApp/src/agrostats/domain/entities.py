"""Entidades de Dominio — AgroData Intelligence Platform (AgroStats).
Modelos de dominio ricos con comportamiento e invariantes de negocio no anémicas.
Normativas: Clean Code / SWEBOK Cap. 2 / ISO 25010 / Metodología Guillermo Guerra (IICA).
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from src.agrostats.domain.exceptions import InvariantViolationException
from src.agrostats.domain.value_objects import (
    CodigoCPC,
    CodigoDivipola,
    CpcProductCode,
    DivipolaCode,
    NelsonViolation,
)


# -----------------------------------------------------------------------------
# 1. Entidades de Mercado, Econometría y Bioinsumos
# -----------------------------------------------------------------------------
@dataclass
class CotizacionMayorista:
    """Cotización diaria de precios mayoristas en centrales de abastos (SIPSA / DANE)."""
    fecha: date
    codigo_cpc: str
    nombre_producto: str
    central_abasto: str
    municipio_divipola: str
    precio_min_cop: float
    precio_max_cop: float
    precio_promedio_cop: float
    volumen_ton: float = 0.0
    id_cotizacion: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.id_cotizacion is None:
            self.id_cotizacion = f"{self.fecha.isoformat()}_{self.codigo_cpc}_{self.central_abasto}"

    def es_consistente(self) -> bool:
        """Verifica la coherencia del rango: precio_min <= precio_promedio <= precio_max."""
        return self.precio_min_cop <= self.precio_promedio_cop <= self.precio_max_cop

    @property
    def amplitud_precios_cop(self) -> float:
        return round(self.precio_max_cop - self.precio_min_cop, 2)

    @property
    def dispersion_pct(self) -> float:
        if self.precio_promedio_cop == 0:
            return 0.0
        return round((self.amplitud_precios_cop / self.precio_promedio_cop) * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_cotizacion": self.id_cotizacion,
            "fecha": self.fecha.isoformat(),
            "codigo_cpc": self.codigo_cpc,
            "nombre_producto": self.nombre_producto,
            "central_abasto": self.central_abasto,
            "municipio_divipola": self.municipio_divipola,
            "precio_min_cop": self.precio_min_cop,
            "precio_max_cop": self.precio_max_cop,
            "precio_promedio_cop": self.precio_promedio_cop,
            "volumen_ton": self.volumen_ton,
            "amplitud_precios_cop": self.amplitud_precios_cop,
            "dispersion_pct": self.dispersion_pct,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class CultivoRentabilidad:
    """Modelo de costos, márgenes y rentabilidad según Guillermo Guerra (IICA)."""
    codigo_cpc: str
    nombre_producto: str
    rendimiento_kg_ha: float
    precio_base_cop_kg: float
    costos_fijos_ha: float
    costos_variables_quimicos_ha: float
    costos_variables_otros_ha: float
    tasa_ahorro_max_bio_pct: float = 0.261
    prima_verde_max_pct: float = 0.180

    @property
    def costos_variables_totales_convencional(self) -> float:
        return self.costos_variables_quimicos_ha + self.costos_variables_otros_ha

    @property
    def margen_bruto_convencional(self) -> float:
        ingreso = self.rendimiento_kg_ha * self.precio_base_cop_kg
        return ingreso - self.costos_variables_totales_convencional


@dataclass
class BioinsumoComercial:
    """Catálogo de insumo biológico con registro ICA para sustitución de síntesis química."""
    bioinsumo_id: int
    nombre_comercial: str
    tipo: str
    ingrediente_activo: str
    empresa_titular: str
    registro_ica: str
    cuota_mercado_pct: float


@dataclass
class RegistroAbastecimiento:
    """Registro de ingreso de alimentos a mercados mayoristas (DANE SIPSA_A)."""
    id_abastecimiento: str
    fecha: date
    mercado_id: str
    codigo_cpc: str
    municipio_origen_divipola: str
    volumen_toneladas: float
    num_vehiculos: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.volumen_toneladas < 0:
            raise InvariantViolationException(
                f"El volumen de abastecimiento no puede ser negativo: {self.volumen_toneladas}"
            )
        if self.num_vehiculos < 0:
            raise InvariantViolationException(
                f"El número de vehículos no puede ser negativo: {self.num_vehiculos}"
            )

    @property
    def volumen_kg(self) -> float:
        return round(self.volumen_toneladas * 1000.0, 2)


@dataclass
class ObservacionClimatica:
    """Observación meteorológica diaria en nodo agrícola (IDEAM DHIME)."""
    id_observacion: str
    estacion_id: str
    fecha: date
    municipio_divipola: str
    precipitacion_mm: float
    temp_max_celsius: Optional[float] = None
    temp_min_celsius: Optional[float] = None
    temp_media_celsius: Optional[float] = None


# -----------------------------------------------------------------------------
# 2. Entidades de Cosecha en Finca y Control Estadístico (SPC)
# -----------------------------------------------------------------------------
@dataclass
class HarvestBatch:
    """Representa un lote cosechado validado dentro de una unidad productiva (lote)."""
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
        return round(self.kilos_totales / self.hectareas_lote, 2)

    @property
    def tasa_exportabilidad(self) -> float:
        if self.kilos_totales == 0:
            return 0.0
        return round(self.kilos_exportables / self.kilos_totales, 4)

    @property
    def ratio_brix_calibre(self) -> float:
        return round(self.grados_brix / self.calibre_promedio, 4)

    def to_dict(self) -> Dict[str, Any]:
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
    """Límites de control estadístico Shewhart (X-bar +- 3 sigma) y evaluación de capacidad."""
    metric_name: str
    center_line: float
    upper_control_limit: float
    lower_control_limit: float
    sigma: float
    sample_size: int
    upper_spec_limit: Optional[float] = None
    lower_spec_limit: Optional[float] = None
    cp_index: Optional[float] = None
    cpk_index: Optional[float] = None
    nelson_violations: List[NelsonViolation] = field(default_factory=list)
    calculated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.upper_control_limit < self.lower_control_limit:
            raise InvariantViolationException("UCL no puede ser menor a LCL.")
        if self.sigma < 0:
            raise InvariantViolationException("Sigma no puede ser negativo.")

    @property
    def is_in_statistical_control(self) -> bool:
        return len(self.nelson_violations) == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "center_line": round(self.center_line, 2),
            "upper_control_limit": round(self.upper_control_limit, 2),
            "lower_control_limit": round(self.lower_control_limit, 2),
            "sigma": round(self.sigma, 4),
            "sample_size": self.sample_size,
            "is_in_statistical_control": self.is_in_statistical_control,
            "nelson_violations": [v.to_dict() for v in self.nelson_violations],
            "cp_index": round(self.cp_index, 3) if self.cp_index is not None else None,
            "cpk_index": round(self.cpk_index, 3) if self.cpk_index is not None else None,
            "calculated_at": self.calculated_at.isoformat(),
        }
