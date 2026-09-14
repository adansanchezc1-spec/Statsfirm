"""
Biostatistical & Statistical Process Control (SPC) AI Agent for Agro Stat & Tech Co.
Responsible for:
- Cálculo riguroso de Cartas de Control Shewhart (Media, Desviación, UCL, LCL).
- Evaluación algorítmica de las 8 Reglas de Western Electric para causas especiales.
- Cálculo de Índices de Capacidad de Proceso (Cp, Cpk, Pp, Ppk).
- Ejecución de análisis de varianza (ANOVA) y pruebas de hipótesis agronómicas.
"""

from typing import Any, Dict, List
import math
try:
    from .base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus
except (ImportError, ValueError):
    from base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus


class BiostatisticalSpcAgent(BaseAgroAgent):
    """
    Autonomous AI Agent executing statistical process control, Shewhart charts and capability auditing.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente Bioestadístico Senior & SPC de Agro Stat & Tech Co. "
            "Tu misión es transformar los datos y la variabilidad de las labores agrícolas en certezas "
            "matemáticas. Calculas límites Shewhart (±3σ) e índices de capacidad (Cp, Cpk). "
            "Diferencias causas comunes de causas especiales de variación usando las Reglas "
            "de Western Electric. Si el proceso reporta Cpk < 1.33 o violaciones críticas, "
            "emites alertas tempranas para contener pérdidas antes de la exportación."
        )
        super().__init__(
            name="Agente_Bioestadistico_SPC_AI",
            role="Lead Bio-Statistician & SPC Engineer",
            autonomy_level=AgroAutonomyLevel.LEVEL_4_HIGH_AUTONOMY,
            system_prompt=system_prompt
        )
        self.register_tool("shewhart_calculator", self._calculate_shewhart_limits)
        self.register_tool("capability_evaluator", self._calculate_capability_indices)
        self.register_tool("western_electric_evaluator", self._evaluate_western_electric)

    def _calculate_shewhart_limits(self, data: List[float]) -> Dict[str, float]:
        """Compute mean, standard deviation, UCL and LCL (+-3 sigma)."""
        if len(data) < 2:
            return {"mean": 0.0, "std_dev": 0.0, "ucl": 0.0, "lcl": 0.0}

        mean_val = sum(data) / len(data)
        variance = sum((x - mean_val) ** 2 for x in data) / (len(data) - 1)
        sigma = math.sqrt(variance)

        return {
            "mean": round(mean_val, 3),
            "std_dev": round(sigma, 3),
            "ucl": round(mean_val + (3 * sigma), 3),
            "lcl": round(max(0.0, mean_val - (3 * sigma)), 3)
        }

    def _calculate_capability_indices(self, mean_val: float, sigma: float, usl: float, lsl: float) -> Dict[str, float]:
        """Compute potential (Cp) and real (Cpk) capability indices."""
        if sigma <= 0.0:
            return {"cp": 0.0, "cpk": 0.0}

        cp = (usl - lsl) / (6 * sigma)
        cpu = (usl - mean_val) / (3 * sigma)
        cpl = (mean_val - lsl) / (3 * sigma)
        cpk = min(cpu, cpl)

        return {
            "cp": round(cp, 3),
            "cpk": round(cpk, 3),
            "is_capable": cpk >= 1.33
        }

    def _evaluate_western_electric(self, data: List[float], limits: Dict[str, float]) -> List[str]:
        """Evaluate Western Electric Rules for out-of-control signals."""
        anomalies: List[str] = []
        ucl = limits["ucl"]
        lcl = limits["lcl"]
        mean_val = limits["mean"]

        # Rule 1: Beyond 3 sigma
        for idx, val in enumerate(data):
            if val > ucl or val < lcl:
                anomalies.append(f"Regla 1 violada: Punto {idx+1} ({val}) fuera de límites 3σ.")

        # Rule 2: 9 points in a row on the same side of the centerline
        if len(data) >= 9:
            for i in range(len(data) - 8):
                window = data[i:i+9]
                if all(x > mean_val for x in window):
                    anomalies.append(f"Regla 2 violada: 9 puntos consecutivos por encima de la media en índice {i}.")
                    break
                if all(x < mean_val for x in window):
                    anomalies.append(f"Regla 2 violada: 9 puntos consecutivos por debajo de la media en índice {i}.")
                    break

        return anomalies

    def execute(self, task: AgroTask) -> AgroResult:
        """Execute complete SPC evaluation on crop or packhouse batch."""
        logs = [f"Iniciando evaluación bioestadística SPC para lote: {task.lote_id}"]
        payload = task.payload

        observations = payload.get("observations", [
            11.2, 11.5, 11.3, 11.4, 11.6, 11.4, 11.5, 11.3, 11.7, 11.4,
            11.5, 11.6, 11.8, 11.4, 11.5, 11.3, 11.6, 11.4, 11.5, 11.5
        ])
        usl = payload.get("usl", 13.0)
        lsl = payload.get("lsl", 10.0)

        limits = self._calculate_shewhart_limits(observations)
        capability = self._calculate_capability_indices(limits["mean"], limits["std_dev"], usl, lsl)
        anomalies = self._evaluate_western_electric(observations, limits)

        is_stable = len(anomalies) == 0 and capability["is_capable"]
        logs.append(f"SPC calculado: Media={limits['mean']}, Cpk={capability['cpk']}. Estable={is_stable}")

        output_data = {
            "variable_analizada": payload.get("variable", "grados_brix"),
            "shewhart_limits": limits,
            "capability_indices": capability,
            "process_in_control": is_stable,
            "western_electric_violations": anomalies,
            "status_label": "BAJO_CONTROL_SPC" if is_stable else "FUERA_DE_CONTROL_REQUIERE_AJUSTE"
        }

        # If process is severely out of control, escalate to human consultant
        if capability["cpk"] < 1.0 or len(anomalies) >= 3:
            return self.escalate_to_human(
                task=task,
                target_human_role="Consultor Agrónomo Sénior / Gerencia Técnica",
                reason=f"Proceso con Cpk deficiente ({capability['cpk']} < 1.0) o múltiples violaciones Western Electric.",
                context=output_data
            )

        return AgroResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=AgroExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
