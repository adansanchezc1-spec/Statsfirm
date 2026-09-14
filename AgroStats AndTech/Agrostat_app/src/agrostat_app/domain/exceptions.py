"""Domain Exceptions for Agrostat Data Science Core.

Normative:
- Clean Code (Robert C. Martin) - Error Handling as Domain Logic
- SWEBOK Chapter 2 - Software Design Exceptions
"""

from typing import Any, Dict, Optional


class DomainException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DataContractViolationException(DomainException):
    """Raised when an ingested record violates DAMA-BOK data contract dimensions."""
    pass


class InvariantViolationException(DomainException):
    """Raised when an entity invariant is violated (e.g. kilos_exportables > kilos_totales)."""
    pass


class InsufficientDataForSPCException(DomainException):
    """Raised when sample size is insufficient to compute statistical control limits."""
    pass


class ModelDriftDetectedException(DomainException):
    """Raised when monitored model performance metrics decay beyond the established threshold."""
    pass


class ModelNotTrainedException(DomainException):
    """Raised when an inference is attempted on an uninitialized or unregistered model."""
    pass


class RepositoryException(DomainException):
    """Raised when an error occurs during persistence in the Medallion lakehouse."""
    pass


class SourceExtractionException(DomainException):
    """Raised when an error occurs while extracting data from an external governmental or satellite API."""
    pass


class UnsupportedSourceException(DomainException):
    """Raised when an extraction source type is not registered or supported."""
    pass
