"""
Entidades del Dominio Agrícola
Clean Architecture / Rich Domain Model
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class CotizacionMayorista:
    fecha: date
    codigo_cpc: str
    nombre_producto: str
    central_abasto: str
    municipio_divipola: str
    precio_min_cop: float
    precio_max_cop: float
    precio_promedio_cop: float
    volumen_ton: float

    def es_consistente(self) -> bool:
        return self.precio_min_cop <= self.precio_promedio_cop <= self.precio_max_cop

@dataclass
class CultivoRentabilidad:
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
    bioinsumo_id: int
    nombre_comercial: str
    tipo: str
    ingrediente_activo: str
    empresa_titular: str
    registro_ica: str
    cuota_mercado_pct: float
