"""Excepciones de Dominio — AgroData Intelligence Platform (AgroStats).
Jerarquía tipada con soporte RFC 7807 Problem Details para FastAPI y contratos de invariantes.
Normativas: Clean Code / SWEBOK Cap. 2 / RFC 7807 / ISO 25010.
"""

from typing import Any, Optional


class DomainException(Exception):
    """Excepción base de dominio con metadatos RFC 7807."""
    def __init__(self, title: str = "Error de Dominio", detail: str = "", status_code: int = 400):
        super().__init__(detail or title)
        self.title = title
        self.detail = detail or title
        self.status_code = status_code


class ValidationException(DomainException):
    """Falla de validación en Value Objects o parámetros de entrada."""
    def __init__(self, detail: str):
        super().__init__(title="Error de Validación de Dominio", detail=detail, status_code=422)


class InvariantViolationException(DomainException):
    """Violación de invariantes de negocio en una entidad."""
    def __init__(self, detail: str):
        super().__init__(title="Violación de Invariante de Dominio", detail=detail, status_code=422)


class EntityNotFoundException(DomainException):
    """Entidad requerida no encontrada en el catálogo o repositorio."""
    def __init__(self, detail: str):
        super().__init__(title="Recurso No Encontrado", detail=detail, status_code=404)


class CommodityNotFoundException(EntityNotFoundException):
    """Producto Agrícola No Encontrado según código CPC."""
    def __init__(self, codigo_cpc: str):
        super().__init__(detail=f"El código CPC v2.1 '{codigo_cpc}' no se encuentra catalogado.")
        self.title = "Producto Agrícola No Encontrado"


class BusinessRuleViolationException(DomainException):
    """Violación de reglas de negocio agronómicas o bioeconómicas."""
    def __init__(self, detail: str):
        super().__init__(title="Violación de Regla de Negocio", detail=detail, status_code=409)


class InvalidAgroeconomicParametersException(DomainException):
    """Parámetros bioeconómicos inválidos para el modelo de Guillermo Guerra."""
    def __init__(self, message: str):
        super().__init__(
            title="Parámetros Agroempresariales Inválidos",
            detail=message,
            status_code=400,
        )


class InsufficientDataException(DomainException):
    """Muestras insuficientes para cálculos estadísticos o econométricos."""
    def __init__(self, detail: str):
        super().__init__(title="Datos Insuficientes para el Análisis", detail=detail, status_code=422)


class InsufficientDataForSPCException(InsufficientDataException):
    """Datos insuficientes para evaluación de cartas de control Shewhart o series temporales."""
    def __init__(self, n_samples_or_msg: Any = 0, min_required: int = 10):
        if isinstance(n_samples_or_msg, (int, float)):
            detail = f"Se requieren mínimo {min_required} observaciones históricas; se recibieron {n_samples_or_msg}."
        else:
            detail = str(n_samples_or_msg)
        super().__init__(detail=detail)
        self.title = "Datos Insuficientes para Control Estadístico Shewhart"
        self.status_code = 422


class DataQualityViolationException(DomainException):
    """Violación de dimensión de calidad de datos DAMA."""
    def __init__(self, dimension: str, detail: str):
        super().__init__(
            title=f"Violación de Calidad DAMA ({dimension})",
            detail=detail,
            status_code=422,
        )


class DataQualityContractViolationException(DomainException):
    """Falla crítica en contrato de datos DAMA-BOK."""
    def __init__(self, detail: str):
        super().__init__(title="Violación de Contrato de Calidad de Datos", detail=detail, status_code=422)


class ModelNotFittedException(DomainException):
    """Intento de inferencia sin modelo entrenado o serializado."""
    def __init__(self, detail: str):
        super().__init__(title="Modelo No Entrenado", detail=detail, status_code=412)


class ModelRegistryException(DomainException):
    """Falla en almacenamiento o recuperación de artefactos en el registry."""
    def __init__(self, detail: str):
        super().__init__(title="Error en Model Registry", detail=detail, status_code=500)


class StorageException(DomainException):
    """Falla de persistencia en Lakehouse (Parquet/DuckDB)."""
    def __init__(self, detail: str):
        super().__init__(title="Error de Almacenamiento Lakehouse", detail=detail, status_code=500)


class CalculationException(DomainException):
    """Falla en cálculos numéricos, convergencia de modelos o divisiones por cero."""
    def __init__(self, detail: str):
        super().__init__(title="Error Numérico de Cálculo", detail=detail, status_code=500)
