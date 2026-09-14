"""Inbound Port: Statistical Process Control (SPC) Analysis Port.

Defines the contract for running Shewhart and Nelson Rules stability analysis.
Normative: Hexagonal Architecture Driving Port / SWEBOK Chapter 2.
"""

from abc import ABC, abstractmethod
from typing import Optional

from agrostat_app.domain.entities import SPCControlLimits


class SPCAnalysisPort(ABC):
    """Driving Port defining the entry point for SPC stability assessments."""

    @abstractmethod
    def analyze_process_stability(
        self,
        lote_id: Optional[str] = None,
        metric_name: str = "rendimiento_kg_ha",
        usl: Optional[float] = None,
        lsl: Optional[float] = None,
    ) -> SPCControlLimits:
        """Executes Shewhart 3-sigma limits and evaluates Nelson Rules."""
        pass
