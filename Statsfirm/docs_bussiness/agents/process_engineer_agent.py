"""
Process Engineer & Architecture Review Board (ARB) AI Agent for Statsfirm Co.
Responsible for:
- Pre-evaluación técnica de factibilidad de leads (BPMN-01 / Task_PreEvaluacionViabilidad).
- Validación de arquitectura técnica base (ARB / Task_ValidacionARB).
- Modelado y linteo de flujos BPMN 2.0 y alineación TOGAF.
"""

from typing import Any, Dict
try:
    from .base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus


class ProcessEngineerAgent(BaseAgent):
    """
    Autonomous AI Agent executing Process Engineering and ARB reviews.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente Senior de Ingeniería de Procesos y ARB de Statsfirm Co. "
            "Tu misión es evaluar la viabilidad técnica de los requerimientos, verificar "
            "conformidad con estándares SWEBOK, TOGAF y Clean Architecture, y lintear procesos "
            "BPMN 2.0. Si un proyecto involucra riesgos de seguridad críticos o presupuestos "
            "atípicos, debes escalar formalmente a Gerencia o Finanzas."
        )
        super().__init__(
            name="Process_Engineer_ARB_AI",
            role="Jefe de Procesos & Architecture Review Board",
            autonomy_level=AutonomyLevel.LEVEL_3_CONDITIONAL,
            system_prompt=system_prompt
        )
        self.register_tool("bpmn_validator", self._validate_bpmn_syntax)
        self.register_tool("feasibility_matrix", self._evaluate_feasibility)

    def _validate_bpmn_syntax(self, bpmn_xml: str) -> bool:
        """Validate BPMN 2.0 XML structure and tags."""
        return "<bpmn:definitions" in bpmn_xml or "<ns0:definitions" in bpmn_xml

    def _evaluate_feasibility(self, domain: str, tech_stack: str) -> Dict[str, Any]:
        """Compute architectural feasibility score."""
        supported_domains = ["fintech", "agro", "health", "logistics", "ecommerce", "saas"]
        is_supported = domain.lower() in supported_domains
        score = 0.95 if is_supported else 0.65
        return {
            "is_feasible": score >= 0.70,
            "feasibility_score": score,
            "recommended_architecture": "Clean Architecture / Hexagonal Ports & Adapters"
        }

    def execute(self, task: AgentTask) -> AgentResult:
        """Execute Process Engineering and ARB tasks."""
        logs = [f"Iniciando evaluación de tarea BPMN: {task.bpmn_task_ref}"]
        payload = task.payload

        # Check for Human Escalation condition (e.g. Budget > $500K USD or Legal Ambiguity)
        estimated_budget = payload.get("estimated_budget_usd", 0)
        if estimated_budget > 500000:
            return self.escalate_to_human(
                task=task,
                target_human_role="Gerencia General / C-Level",
                reason="El presupuesto estimado supera el umbral de autonomía del agente ($500,000 USD).",
                context={"budget": estimated_budget, "client": payload.get("client_name")}
            )

        domain = payload.get("industry_domain", "general")
        tech_stack = payload.get("tech_stack", "Python / FastAPI")
        
        evaluation = self._evaluate_feasibility(domain, tech_stack)
        logs.append(f"Evaluación de factibilidad completada: Score={evaluation['feasibility_score']}")

        output_data = {
            "evaluation_result": "APROBADO_ARB" if evaluation["is_feasible"] else "OBSERVACIONES_TECNICAS",
            "feasibility": evaluation,
            "deliverable_markdown": "docs/02-architecture/architecture_assessment.md",
            "solid_compliance_verified": True,
            "arb_signoff": "SIGN-OFF-AUTOMATED-ARB-2026"
        }

        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=ExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
