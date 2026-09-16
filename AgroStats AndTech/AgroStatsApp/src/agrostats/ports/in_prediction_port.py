"""Inbound Port: Yield Inference Port.

Defines the contract for scoring lots and predicting yields.
Normative: Hexagonal Architecture Driving Port / SWEBOK Chapter 2.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from agrostat_app.domain.value_objects import YieldPrediction


class YieldInferencePort(ABC):
    """Driving Port defining the entry point for generating harvest yield forecasts."""

    @abstractmethod
    def predict_harvest_yield(self, batch_payload: Dict[str, Any]) -> YieldPrediction:
        """Generates an inference prediction with 95% confidence intervals

        using the currently active model from the registry.
        """
        pass
