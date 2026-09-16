"""Outbound Port: Model Registry Port.

Defines persistence and versioning contracts for machine learning models.
Normative: MLOps / Hexagonal Architecture Driven Port.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class ModelRegistryPort(ABC):
    """Driven Port defining abstraction over Model Store, versioning and metadata tracking."""

    @abstractmethod
    def save_model(
        self,
        model: Any,
        model_name: str,
        version: str,
        metrics: Dict[str, float],
        feature_names: List[str],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Saves model binary artifact alongside JSON metadata."""
        pass

    @abstractmethod
    def load_model(
        self, model_name: str = "yield_forecast", version: Optional[str] = None
    ) -> Tuple[Any, Dict[str, Any]]:
        """Loads model binary artifact and its metadata dictionary."""
        pass

    @abstractmethod
    def list_models(self) -> List[Dict[str, Any]]:
        """Lists registered models with their training metrics and active status."""
        pass
