"""Inbound Port: Model Training Pipeline Port.

Defines the contract for training, validating, and registering ML models.
Normative: Hexagonal Architecture Driving Port / SWEBOK Chapter 2.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ModelTrainingPipelinePort(ABC):
    """Driving Port defining the entry point for training Yield AI models."""

    @abstractmethod
    def train_and_register(
        self,
        lote_id: Optional[str] = None,
        test_size: float = 0.2,
        model_algorithm: str = "random_forest",
    ) -> Dict[str, Any]:
        """Trains an ML model on Silver layer data, evaluates metrics (R2, RMSE, MAPE),

        and registers in the Model Registry if thresholds are met.
        """
        pass
