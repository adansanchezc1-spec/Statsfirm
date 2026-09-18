"""
Product Owner & Agile Coach AI Agent for Statsfirm Co.
Responsible for:
- Refinamiento de Backlog y Criterios Gherkin (Task_RefinarBacklog).
- Sprint Planning y Verificación del Definition of Ready (Task_SprintPlanningDoR).
- Demostración en Sprint Review y orquestación de ceremonias ágiles (Task_SprintReviewDemo).
- Repriorización y gestión de ajustes de sprint (Task_PlanificarAjusteSprint).
"""

from typing import Any, Dict, List
try:
    from .base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus


class ProductOwnerAgent(BaseAgent):
    """
    Autonomous AI Agent executing Product Ownership and Agile Coaching responsibilities.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente Product Owner & Agile Coach de Statsfirm Co. "
            "Tu responsabilidad es transformar requerimientos de alto nivel en historias de usuario "
            "computables bajo estándar Gherkin (Given-When-Then), asegurar el cumplimiento del "
            "Definition of Ready (DoR) antes del sprint y orquestar el Sprint Backlog. "
            "Si el alcance excede la capacidad del squad en más de 20%, debes negociar con Gerencia."
        )
        super().__init__(
            name="Product_Owner_Agile_AI",
            role="Product Owner & Agile Coach",
            autonomy_level=AutonomyLevel.LEVEL_4_HIGH_AUTONOMY,
            system_prompt=system_prompt
        )
        self.register_tool("gherkin_generator", self._generate_gherkin_scenario)
        self.register_tool("dor_validator", self._validate_dor)

    def _generate_gherkin_scenario(self, feature_title: str, user_role: str, action: str, outcome: str) -> str:
        """Generate formatted Gherkin user story."""
        return (
            f"Feature: {feature_title}\n"
            f"  As a {user_role}\n"
            f"  I want to {action}\n"
            f"  So that {outcome}\n\n"
            f"  Scenario: Successful execution of {feature_title}\n"
            f"    Given that the system prerequisites for {feature_title} are satisfied\n"
            f"    When the user triggers {action}\n"
            f"    Then the system ensures {outcome}\n"
            f"    And logs the transaction in the audit trail."
        )

    def _validate_dor(self, story: Dict[str, Any]) -> bool:
        """Validate Definition of Ready checklist."""
        required_fields = ["title", "acceptance_criteria", "story_points", "business_value"]
        return all(f in story and story[f] for f in required_fields)

    def execute(self, task: AgentTask) -> AgentResult:
        """Execute Agile Backlog refinement and DoR verification."""
        logs = [f"Iniciando tarea de Gestión Ágil: {task.title}"]
        payload = task.payload

        raw_stories = payload.get("raw_requirements", [
            {
                "title": "Carga de Datasets de Clientes",
                "role": "Analista de Operaciones",
                "action": "cargar archivos CSV y Excel",
                "outcome": "el sistema valide esquemas y active el análisis estadístico",
                "story_points": 5,
                "business_value": "Alto"
            }
        ])

        refined_backlog: List[Dict[str, Any]] = []
        for item in raw_stories:
            gherkin = self._generate_gherkin_scenario(
                item["title"], item["role"], item["action"], item["outcome"]
            )
            item["acceptance_criteria"] = gherkin
            dor_passed = self._validate_dor(item)
            refined_backlog.append({
                "story": item,
                "dor_compliant": dor_passed,
                "gherkin_spec": gherkin
            })
            logs.append(f"Historia '{item['title']}' refinada. DoR={dor_passed}")

        total_points = sum(s["story"]["story_points"] for s in refined_backlog)
        squad_capacity = payload.get("squad_capacity_points", 40)

        # Escalation rule if overloaded
        if total_points > (squad_capacity * 1.25):
            return self.escalate_to_human(
                task=task,
                target_human_role="Gerencia / Ejecutivo Comercial",
                reason=f"El backlog refinado ({total_points} pts) supera la capacidad del squad ({squad_capacity} pts). Requiere repriorización de alcance.",
                context={"total_points": total_points, "capacity": squad_capacity}
            )

        output_data = {
            "sprint_backlog": refined_backlog,
            "total_story_points": total_points,
            "dor_certified": all(s["dor_compliant"] for s in refined_backlog),
            "sprint_goal": payload.get("sprint_goal", "Entrega de Incremento de Valor Computable")
        }

        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=ExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
