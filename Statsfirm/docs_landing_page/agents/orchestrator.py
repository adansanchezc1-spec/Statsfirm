"""
Multi-Agent Orchestrator & BPMN Engine Bridge for Statsfirm Co.
Responsible for:
- Mapping BPMN task references to the corresponding Autonomous AI Agent.
- Enforcing Human-in-the-Loop policies for Management, Finance, and HR tasks.
- Dispatching execution payloads and tracking end-to-end task results.
"""

from typing import Any, Dict, Optional
try:
    from .base_agent import BaseAgent, AgentTask, AgentResult, ExecutionStatus
    from .process_engineer_agent import ProcessEngineerAgent
    from .product_owner_agent import ProductOwnerAgent
    from .software_developer_agent import SoftwareDeveloperAgent
    from .qa_automation_agent import QaAutomationAgent
    from .data_steward_agent import DataStewardAgent
    from .sre_operations_agent import SreOperationsAgent
    from .innova_lab_agent import InnovaLabAgent
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentTask, AgentResult, ExecutionStatus
    from process_engineer_agent import ProcessEngineerAgent
    from product_owner_agent import ProductOwnerAgent
    from software_developer_agent import SoftwareDeveloperAgent
    from qa_automation_agent import QaAutomationAgent
    from data_steward_agent import DataStewardAgent
    from sre_operations_agent import SreOperationsAgent
    from innova_lab_agent import InnovaLabAgent


class StatsfirmAgentOrchestrator:
    """
    Central dispatcher coordinating multi-agent execution across the BPMN lifecycle.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgent] = {
            "PROCESS_ARB": ProcessEngineerAgent(),
            "PRODUCT_OWNER": ProductOwnerAgent(),
            "DEVELOPER": SoftwareDeveloperAgent(),
            "QA_AUTOMATION": QaAutomationAgent(),
            "DATA_STEWARD": DataStewardAgent(),
            "SRE_OPS": SreOperationsAgent(),
            "INNOVA_LAB": InnovaLabAgent()
        }

        # Mapping of BPMN task IDs to Agent keys or Human Roles
        self._bpmn_routing_table: Dict[str, str] = {
            # Human Tasks (HITL)
            "Task_CapturaLead": "HUMAN_GERENCIA",
            "Task_FormalizarContrato": "HUMAN_LEGAL_FINANZAS",
            "Task_ModeladoFinOps": "HUMAN_FINANZAS",
            "Task_Cli_Solicitud": "HUMAN_CLIENTE",
            "Task_Cli_FirmaContrato": "HUMAN_CLIENTE",
            "Task_Cli_FirmaEntrega": "HUMAN_CLIENTE",

            # Autonomous Agent Tasks
            "Task_PreEvaluacionViabilidad": "PROCESS_ARB",
            "Task_ValidacionARB": "PROCESS_ARB",
            "Task_SesionesDiscover": "PROCESS_ARB",
            "Task_InformeMadurezOKRs": "PROCESS_ARB",
            "Task_RefinarBacklog": "PRODUCT_OWNER",
            "Task_SprintPlanningDoR": "PRODUCT_OWNER",
            "Task_PlanificarAjusteSprint": "PRODUCT_OWNER",
            "Task_DesarrolloGitFlow": "DEVELOPER",
            "Task_PullRequestReview": "DEVELOPER",
            "Task_FixCodeQuality": "DEVELOPER",
            "Task_PruebasQA": "QA_AUTOMATION",
            "Task_ValidarGobernanza": "DATA_STEWARD",
            "Task_ValidarEsquema": "DATA_STEWARD",
            "Task_MitigacionIncidente": "SRE_OPS",
            "Task_TelemetriaPrometheus": "SRE_OPS",
            "Task_SprintReviewDemo": "PRODUCT_OWNER",
            "Task_RetrospectivaSquad": "INNOVA_LAB",
            "Task_PropuestaAcelerador": "INNOVA_LAB",
            "Task_RecopilarDORA": "INNOVA_LAB"
        }

    def dispatch(self, bpmn_task_id: str, title: str, payload: Dict[str, Any]) -> AgentResult:
        """
        Dispatch a BPMN task to either an AI Agent or a Human Queue.
        """
        target = self._bpmn_routing_table.get(bpmn_task_id, "PROCESS_ARB")
        task = AgentTask(bpmn_task_ref=bpmn_task_id, title=title, payload=payload)

        # Handle Human Tasks
        if target.startswith("HUMAN_"):
            human_role = target.replace("HUMAN_", "").replace("_", " ").title()
            return AgentResult(
                task_id=task.task_id,
                agent_name="BPMN_Human_Dispatcher",
                status=ExecutionStatus.ESCALATE_TO_HUMAN,
                escalation_reason=f"Tarea asignada a rol humano reservado: [{human_role}].",
                output={"human_role": human_role, "task_title": title, "payload": payload},
                logs=[f"Enrutado a bandeja de entrada humana: {human_role}"]
            )

        # Handle Autonomous AI Agent Tasks
        agent = self._agents.get(target)
        if not agent:
            raise ValueError(f"No hay agente registrado para el target: {target}")

        return agent.execute(task)

    def get_agent(self, agent_key: str) -> Optional[BaseAgent]:
        """Retrieve a direct reference to a registered agent."""
        return self._agents.get(agent_key)
