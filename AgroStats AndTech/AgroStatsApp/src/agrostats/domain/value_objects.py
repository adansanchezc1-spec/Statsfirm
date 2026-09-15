"""
Objetos de Valor Inmutables del Dominio Agrícola
Clean Architecture / DDD
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class DineroCOP:
    valor: float

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El monto monetario no puede ser negativo.")

    def formatear_millones(self) -> str:
        return f"${(self.valor / 1000000):.2f}M COP"

    def formatear_pesos(self) -> str:
        return f"${round(self.valor):,} COP".replace(",", ".")

@dataclass(frozen=True)
class RendimientoKgHa:
    kilos_por_hectarea: float

    def __post_init__(self):
        if self.kilos_por_hectarea <= 0:
            raise ValueError("El rendimiento físico por hectárea debe ser mayor a cero.")

@dataclass(frozen=True)
class PorcentajeAdopcion:
    porcentaje: float

    def __post_init__(self):
        if not (0.0 <= self.porcentaje <= 100.0):
            raise ValueError("El porcentaje de adopción debe estar comprendido entre 0.0 y 100.0.")

    @property
    def factor(self) -> float:
        return self.porcentaje / 100.0

@dataclass(frozen=True)
class CodigoCpc:
    codigo: str

    def __post_init__(self):
        if len(self.codigo.strip()) < 3:
            raise ValueError("El código CPC debe ser un identificador válido.")

@dataclass(frozen=True)
class CodigoDivipola:
    codigo_dane: str

    def __post_init__(self):
        if len(self.codigo_dane.strip()) != 5:
            raise ValueError("El código DIVIPOLA municipal debe tener exactamente 5 dígitos.")
