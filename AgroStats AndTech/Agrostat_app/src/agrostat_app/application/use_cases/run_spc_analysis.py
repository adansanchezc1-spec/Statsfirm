"""Use Case: Run Statistical Process Control (SPC) Analysis.

Implements SPCAnalysisPort.
Retrieves silver batches, calculates Shewhart limits, evaluates Nelson rules, and audits stability.
Normative: SWEBOK Chapter 2 / ISO 7870.
"""

from typing import Optional

from agrostat_app.domain.entities import SPCControlLimits
from agrostat_app.domain.services.biostatistical_engine import BioStatisticalEngine
from agrostat_app.ports.in_spc_port import SPCAnalysisPort
from agrostat_app.ports.out_notification_port import NotificationPort
from agrostat_app.ports.out_repository_port import HarvestRepositoryPort


class RunSPCAnalysisUseCase(SPCAnalysisPort):
    """Use Case coordinating the Statistical Process Control analysis."""

    def __init__(
        self,
        repository: HarvestRepositoryPort,
        spc_engine: BioStatisticalEngine,
        notifier: NotificationPort,
    ) -> None:
        self._repository = repository
        self._spc_engine = spc_engine
        self._notifier = notifier

    def analyze_process_stability(
        self,
        lote_id: Optional[str] = None,
        metric_name: str = "rendimiento_kg_ha",
        usl: Optional[float] = None,
        lsl: Optional[float] = None,
    ) -> SPCControlLimits:
        """Executes the biostatistical process control analysis."""
        self._notifier.send_alert(
            level="INFO",
            title="Iniciando Auditoría Bioestadística SPC",
            message=f"Métrica: {metric_name} | Lote: {lote_id or 'Todos los lotes'}",
        )

        batches = self._repository.get_silver_batches(lote_id)

        # Cálculo matemático en el motor de dominio
        spc_limits = self._spc_engine.compute_spc_limits(
            batches=batches,
            metric_attr=metric_name,
            usl=usl,
            lsl=lsl,
        )

        if not spc_limits.is_in_statistical_control:
            self._notifier.send_alert(
                level="WARNING",
                title="Proceso Fuera de Control Estadístico",
                message=f"Se detectaron {len(spc_limits.violations)} violaciones a las Reglas de Nelson.",
                metadata={"violations": [v.to_dict() for v in spc_limits.violations]},
            )
        else:
            self._notifier.send_alert(
                level="INFO",
                title="Proceso en Control Estadístico",
                message=f"El proceso se encuentra estable (Cpk={spc_limits.cpk_index:.2f}).",
            )

        return spc_limits
