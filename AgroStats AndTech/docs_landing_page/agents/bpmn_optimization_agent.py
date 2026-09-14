"""
BPMN Process Optimization & Bottleneck Mitigation AI Agent for Agro Stat & Tech Co.
Responsible for:
- Auditoría de procesos de cosecha y labores de campo (Task_AuditoriaCuellosBotella).
- Detección de cuellos de botella y mermas por tiempos muertos o descalibración.
- Generación del proceso To-Be en BPMN 2.0 y matriz de acciones de valor compartido (Task_GenerarPlanMejoraBPMN).
"""

from typing import Any, Dict, List
try:
    from .base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus
except (ImportError, ValueError):
    from base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus


class BpmnOptimizationAgent(BaseAgroAgent):
    """
    Autonomous AI Agent executing Lean Six Sigma and BPMN process redesign for agro-enterprises.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente de Optimización de Procesos BPMN de Agro Stat & Tech Co. "
            "Tu misión es erradicar el desperdicio operativo y la variabilidad en labores agrícolas "
            "y de cosecha en campo. Aplicas principios Lean Six Sigma y notación BPMN 2.0. "
            "Modelas el proceso As-Is, identificas tiempos muertos, cuellos de botella en labores "
            "y diseñas el flujo To-Be con cálculo del retorno económico (Share-of-Gain)."
        )
        super().__init__(
            name="Agente_Optimizacion_BPMN_AI",
            role="Lead Process Engineer & Lean Agroindustrial Consultant",
            autonomy_level=AgroAutonomyLevel.LEVEL_4_HIGH_AUTONOMY,
            system_prompt=system_prompt
        )
        self.register_tool("bottleneck_detector", self._detect_bottlenecks)
        self.register_tool("roi_estimator", self._estimate_shared_value)

    def _detect_bottlenecks(self, steps_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical bottlenecks in agricultural and harvest processes."""
        bottlenecks: List[Dict[str, Any]] = []
        for s in steps_data:
            cycle_time = s.get("cycle_time_mins", 0)
            reject_rate = s.get("reject_rate_pct", 0.0)
            if cycle_time > 45 or reject_rate > 3.0:
                bottlenecks.append({
                    "step_name": s.get("name", "Etapa Operativa"),
                    "frictional_cause": "Demora excesiva en acopio de campo" if cycle_time > 45 else "Desincronización en cuadrilla de corte",
                    "severity": "ALTA" if reject_rate > 5.0 else "MEDIA",
                    "recommended_fix": "Optimizar rutas de recolección y estandarizar intervalos de labor"
                })
        return bottlenecks

    def _estimate_shared_value(self, hectares: float, current_loss_pct: float, target_loss_pct: float) -> Dict[str, float]:
        """Estimate financial savings under the Share-of-Gain model."""
        loss_reduction = max(0.0, current_loss_pct - target_loss_pct)
        # Assuming $12,000 USD gross margin per hectare in export crops
        gross_value = hectares * 12000.0
        projected_savings_usd = round(gross_value * (loss_reduction / 100.0), 2)
        share_of_gain_fee = round(projected_savings_usd * 0.20, 2)  # 20% success fee

        return {
            "loss_reduction_pct": round(loss_reduction, 2),
            "projected_savings_usd": projected_savings_usd,
            "share_of_gain_fee_usd": share_of_gain_fee,
            "net_gain_for_producer_usd": round(projected_savings_usd - share_of_gain_fee, 2)
        }

    def execute(self, task: AgroTask) -> AgroResult:
        """Execute process diagnostic and To-Be optimization plan generation."""
        logs = [f"Iniciando optimización BPMN para lote: {task.lote_id}"]
        payload = task.payload

        process_steps = payload.get("process_steps", [
            {"name": "Corte y Recolección en Campo", "cycle_time_mins": 30, "reject_rate_pct": 1.2},
            {"name": "Transporte a Centro de Acopio", "cycle_time_mins": 65, "reject_rate_pct": 3.8},
            {"name": "Selección y Clasificación en Finca", "cycle_time_mins": 20, "reject_rate_pct": 4.5},
            {"name": "Consolidación de Lote para Despacho", "cycle_time_mins": 40, "reject_rate_pct": 0.8}
        ])
        hectareas = payload.get("hectareas", 50.0)

        bottlenecks = self._detect_bottlenecks(process_steps)
        roi = self._estimate_shared_value(hectareas, current_loss_pct=5.5, target_loss_pct=1.8)
        logs.append(f"Cuellos de botella detectados: {len(bottlenecks)}. Ahorro proyectado: ${roi['projected_savings_usd']} USD")

        output_data = {
            "lote_id": task.lote_id or "LOTE-04-HASS",
            "as_is_bottlenecks": bottlenecks,
            "to_be_recommendations": [
                "BPMN-OPT-01: Rediseñar logística de tránsito campo-acopio a < 40 minutos.",
                "BPMN-OPT-02: Calibración estadística de criterios de cosecha según tolerancia Cp > 1.33.",
                "BPMN-OPT-03: Implementar inspección de calidad en cosecha por muestreo probabilístico."
            ],
            "financial_impact_share_of_gain": roi,
            "bpmn_deliverable": "bpmn/agrostats_procesos_analiticos.bpmn"
        }

        return AgroResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=AgroExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
