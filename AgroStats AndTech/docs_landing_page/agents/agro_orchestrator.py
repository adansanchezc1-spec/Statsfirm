"""
AgroStats Multi-Agent Orchestrator & BPMN Workflow Bridge.
Responsible for:
- Mapping AgroStats BPMN tasks to specialized agricultural AI agents.
- Routing Management, Finance (Share-of-Gain), and Legal tasks to Human Queues.
- Coordinating end-to-end execution across the 7 lanes of agrostats_procesos_analiticos.bpmn.
"""

from typing import Any, Dict, Optional
try:
    from .base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroExecutionStatus
    from .ingestion_contracts_agent import IngestionContractsAgent
    from .lakehouse_geospatial_agent import LakehouseGeospatialAgent
    from .biostatistical_spc_agent import BiostatisticalSpcAgent
    from .yield_ai_agent import YieldAiAgent
    from .bpmn_optimization_agent import BpmnOptimizationAgent
    from .agroinnova_lab_agent import AgroInnovaLabAgent
except (ImportError, ValueError):
    from base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroExecutionStatus
    from ingestion_contracts_agent import IngestionContractsAgent
    from lakehouse_geospatial_agent import LakehouseGeospatialAgent
    from biostatistical_spc_agent import BiostatisticalSpcAgent
    from yield_ai_agent import YieldAiAgent
    from bpmn_optimization_agent import BpmnOptimizationAgent
    from agroinnova_lab_agent import AgroInnovaLabAgent


class AgroStatsAgentOrchestrator:
    """
    Central dispatcher coordinating multi-agent execution across the AgroStats BPMN process.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, BaseAgroAgent] = {
            "INGESTA_CONTRACTS": IngestionContractsAgent(),
            "LAKEHOUSE_GEO": LakehouseGeospatialAgent(),
            "BIOSTAT_SPC": BiostatisticalSpcAgent(),
            "YIELD_AI": YieldAiAgent(),
            "BPMN_OPT": BpmnOptimizationAgent(),
            "AGROINNOVA_LAB": AgroInnovaLabAgent()
        }

        # Mapping of BPMN task IDs in agrostats_procesos_analiticos.bpmn
        self._routing_table: Dict[str, str] = {
            # Human Tasks (HITL)
            "Task_EvaluarLeadAgro": "HUMAN_GERENCIA_AGRO",
            "Task_ModeladoShareOfGain": "HUMAN_FINANZAS_FINOPS",
            "Task_EmitirAcuerdoDigital": "HUMAN_LEGAL",
            "Task_CertificarIncrementoValor": "HUMAN_GERENCIA_AGRO",
            "Task_FacturacionShareOfGain": "HUMAN_FINANZAS_FINOPS",
            "Task_Prod_Solicitar": "HUMAN_PRODUCTOR",
            "Task_Prod_FirmaAcuerdo": "HUMAN_PRODUCTOR",
            "Task_Prod_CargaDatos": "HUMAN_PRODUCTOR",
            "Task_Prod_ResolverCuarentena": "HUMAN_PRODUCTOR",
            "Task_Prod_AprobarPlanBPMN": "HUMAN_PRODUCTOR",
            "Task_Prod_FirmaConformidad": "HUMAN_PRODUCTOR",

            # Autonomous AI Agent Tasks
            "Task_ValidarDataContracts": "INGESTA_CONTRACTS",
            "Task_IngestaMulticanal": "INGESTA_CONTRACTS",
            "Task_EnrutarDLQ": "INGESTA_CONTRACTS",
            "Task_CuraduriaDelta": "LAKEHOUSE_GEO",
            "Task_InterpolacionKriging": "LAKEHOUSE_GEO",
            "Task_CalculoLimitesSPC": "BIOSTAT_SPC",
            "Task_EvaluarWesternElectric": "BIOSTAT_SPC",
            "Task_AnalisisCausaRaiz": "BIOSTAT_SPC",
            "Task_EmitirAlertaSPC": "BIOSTAT_SPC",
            "Task_EntrenamientoYieldAI": "YIELD_AI",
            "Task_AuditoriaCuellosBotella": "BPMN_OPT",
            "Task_GenerarPlanMejoraBPMN": "BPMN_OPT",
            "Task_RetrospectivaAgroInnova": "AGROINNOVA_LAB"
        }

    def dispatch(self, bpmn_task_id: str, title: str, lote_id: str, payload: Dict[str, Any]) -> AgroResult:
        """
        Dispatch an agricultural process task to either an AI Agent or a Human Queue.
        """
        target = self._routing_table.get(bpmn_task_id, "BIOSTAT_SPC")
        task = AgroTask(bpmn_task_ref=bpmn_task_id, title=title, lote_id=lote_id, payload=payload)

        # Handle Human Tasks
        if target.startswith("HUMAN_"):
            human_role = target.replace("HUMAN_", "").replace("_", " ").title()
            return AgroResult(
                task_id=task.task_id,
                agent_name="BPMN_Agro_Human_Dispatcher",
                status=AgroExecutionStatus.ESCALATE_TO_HUMAN,
                escalation_reason=f"Tarea asignada a rol humano agroempresarial: [{human_role}].",
                output={"human_role": human_role, "lote_id": lote_id, "payload": payload},
                logs=[f"Enrutado a bandeja de trabajo humana: {human_role}"]
            )

        # Handle Autonomous Agent Tasks
        agent = self._agents.get(target)
        if not agent:
            raise ValueError(f"No hay agente agropecuario registrado para el target: {target}")

        return agent.execute(task)

    def get_agent(self, agent_key: str) -> Optional[BaseAgroAgent]:
        """Retrieve a direct reference to a registered AgroStats agent."""
        return self._agents.get(agent_key)
