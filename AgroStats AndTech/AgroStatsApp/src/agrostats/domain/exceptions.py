"""
Excepciones de Dominio Tipadas
Mapping conforme a RFC 7807 (Problem Details for HTTP APIs)
"""

class DomainException(Exception):
    """Excepción base del dominio de AgroData Platform."""
    def __init__(self, title: str, detail: str, status_code: int = 400):
        super().__init__(detail)
        self.title = title
        self.detail = detail
        self.status_code = status_code

class InsufficientDataForSPCException(DomainException):
    def __init__(self, n_samples: int, min_required: int = 10):
        super().__init__(
            title="Datos Insuficientes para Control Estadístico Shewhart",
            detail=f"Se requieren mínimo {min_required} observaciones históricas; se recibieron {n_samples}.",
            status_code=422
        )

class InvalidAgroeconomicParametersException(DomainException):
    def __init__(self, message: str):
        super().__init__(
            title="Parámetros Agroempresariales Inválidos",
            detail=message,
            status_code=400
        )

class DataQualityViolationException(DomainException):
    def __init__(self, dimension: str, detail: str):
        super().__init__(
            title=f"Violación de Calidad DAMA ({dimension})",
            detail=detail,
            status_code=422
        )

class CommodityNotFoundException(DomainException):
    def __init__(self, codigo_cpc: str):
        super().__init__(
            title="Producto Agrícola No Encontrado",
            detail=f"El código CPC v2.1 '{codigo_cpc}' no se encuentra catalogado.",
            status_code=404
        )
