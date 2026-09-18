"""
Innova Lab & R&D Accelerator AI Agent for Statsfirm Co.
Responsible for:
- Recopilación de Métricas DORA y Velocidad de Squads (Task_RecopilarDORA).
- Retrospectivas de ingeniería e identificación de fricción técnica (Task_RetrospectivaSquad).
- Incubación de aceleradores técnicos y actualización metodológica STF (Task_PropuestaAcelerador).
"""

from typing import Any, Dict, List
try:
    from .base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus


class InnovaLabAgent(BaseAgent):
    """
    Autonomous AI Agent executing engineering R&D, DORA analytics and accelerator incubation.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente de Innova Lab & Aceleración de I+D de Statsfirm Co. "
            "Tu objetivo es impulsar la mejora continua del ecosistema de ingeniería. "
            "Monitoreas las 4 métricas DORA (Deployment Frequency, Lead Time for Changes, "
            "Change Failure Rate, Time to Restore Service). Detectas cuellos de botella en los "
            "squads y empaquetas soluciones recurrentes en aceleradores técnicos reutilizables."
        )
        super().__init__(
            name="Innova_Lab_Accelerator_AI",
            role="Head of Innova Lab & R&D Transformation Lead",
            autonomy_level=AutonomyLevel.LEVEL_3_CONDITIONAL,
            system_prompt=system_prompt
        )
        self.register_tool("dora_calculator", self._calculate_dora_metrics)
        self.register_tool("friction_analyzer", self._analyze_friction_points)

    def _calculate_dora_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute standard DevOps Research and Assessment (DORA) metrics."""
        deployments_per_month = data.get("deployments_per_month", 24)
        lead_time_days = data.get("lead_time_days", 2.5)
        cfr_pct = data.get("change_failure_rate_pct", 3.2)
        mttr_hours = data.get("mttr_hours", 0.4)

        # Classification based on DORA benchmarks
        performance_tier = "ELITE" if (deployments_per_month >= 20 and cfr_pct < 5.0 and mttr_hours < 1.0) else "HIGH"
        return {
            "tier": performance_tier,
            "deployment_frequency": f"{deployments_per_month} deploys/mes",
            "lead_time_for_changes": f"{lead_time_days} días",
            "change_failure_rate": f"{cfr_pct}%",
            "mean_time_to_restore": f"{mttr_hours} horas"
        }

    def _analyze_friction_points(self, retrospective_notes: List[str]) -> List[str]:
        """Extract recurrent friction points from engineering retrospectives."""
        accelerators_needed: List[str] = []
        full_text = " ".join(retrospective_notes).lower()
        if "ingesta" in full_text or "csv" in full_text:
            accelerators_needed.append("Acelerador STF: Multi-Format Ingestion Template")
        if "despliegue" in full_text or "k8s" in full_text:
            accelerators_needed.append("Acelerador STF: One-Click Helm Deployer")
        return accelerators_needed or ["Acelerador STF: Generic Microservice Boilerplate"]

    def execute(self, task: AgentTask) -> AgentResult:
        """Execute DORA evaluation and accelerator generation."""
        logs = [f"Iniciando evaluación de Innova Lab para: {task.title}"]
        payload = task.payload

        dora = self._calculate_dora_metrics(payload)
        notes = payload.get("retro_notes", ["La ingesta de CSV manual genera retrasos", "El pipeline CI es lento"])
        accelerators = self._analyze_friction_points(notes)

        logs.append(f"Métricas DORA calculadas: Nivel={dora['tier']}. Aceleradores propuestos={len(accelerators)}")

        output_data = {
            "dora_metrics": dora,
            "friction_mitigation": accelerators,
            "rd_deliverable": "docs/08-bpmn-engineering/catalogo_aceleradores.md",
            "ready_for_incubation": True
        }

        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=ExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
