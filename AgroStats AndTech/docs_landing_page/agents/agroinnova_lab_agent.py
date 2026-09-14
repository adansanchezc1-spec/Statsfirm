"""
AgroInnova Lab AI Agent for Agro Stat & Tech Co.
Responsible for:
- Calibración algorítmica y mejora continua de modelos matemáticos (Task_RetrospectivaAgroInnova).
- Benchmarking de variedades agronómicas y evaluación de coeficientes de cultivo (Kc).
- Consolidación de lecciones aprendidas de fin de temporada y retroalimentación al Lakehouse.
"""

from typing import Any, Dict, List
try:
    from .base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus
except (ImportError, ValueError):
    from base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus


class AgroInnovaLabAgent(BaseAgroAgent):
    """
    Autonomous AI Agent executing bio-statistical R&D, model calibration and benchmarking.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente de AgroInnova Lab de Agro Stat & Tech Co. "
            "Tu misión es calibrar continuamente los algoritmos predictivos y las cartas SPC "
            "comparando las proyecciones de inicio de temporada contra los rendimientos consolidados de cosecha. "
            "Ajustas los coeficientes fenológicos y optimizas las fórmulas bioestadísticas sin usar sensores."
        )
        super().__init__(
            name="Agente_AgroInnova_Lab_AI",
            role="Head of AgroInnova Lab & Bio-Statistical Calibration Lead",
            autonomy_level=AgroAutonomyLevel.LEVEL_3_CONDITIONAL,
            system_prompt=system_prompt
        )
        self.register_tool("calibration_engine", self._calibrate_model_weights)

    def _calibrate_model_weights(self, predicted: float, actual: float) -> Dict[str, float]:
        """Calibrate model coefficients based on seasonal residual error."""
        error_pct = round(((actual - predicted) / actual) * 100, 2) if actual > 0 else 0.0
        # Compute correction factor
        adjustment_factor = round(actual / predicted, 4) if predicted > 0 else 1.0

        return {
            "predicted_ton_ha": predicted,
            "actual_harvested_ton_ha": actual,
            "residual_error_pct": error_pct,
            "calibration_factor_applied": adjustment_factor,
            "algorithm_accuracy_pct": round(100.0 - abs(error_pct), 2)
        }

    def execute(self, task: AgroTask) -> AgroResult:
        """Execute seasonal model calibration and retrospective benchmark."""
        logs = [f"Iniciando calibración de AgroInnova Lab para lote: {task.lote_id}"]
        payload = task.payload

        predicted = payload.get("predicted_yield", 22.8)
        actual = payload.get("actual_yield", 23.4)

        calibration = self._calibrate_model_weights(predicted, actual)
        logs.append(f"Calibración completada: Precisión={calibration['algorithm_accuracy_pct']}%. Factor={calibration['calibration_factor_applied']}")

        output_data = {
            "lote_id": task.lote_id or "LOTE-04-HASS",
            "calibration_report": calibration,
            "model_version_updated": "YieldAI-Model-v2.1-Calibrated",
            "rd_benchmark_deliverable": "docs/05-maintenance/calibracion_modelos_temporada.md"
        }

        return AgroResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=AgroExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
