"""
Base Agent Module for Statsfirm Co.
Defines the abstract foundation for autonomous AI engineering agents following
SWEBOK, SOLID principles, and the PDCO framework.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import datetime
import uuid


class AutonomyLevel(Enum):
    """Degrees of operational autonomy for AI agents."""
    LEVEL_1_ADVISORY = "L1_ADVISORY"  # Suggests only; human must approve every action.
    LEVEL_2_SUPERVISED = "L2_SUPERVISED"  # Executes minor steps; human approves milestones.
    LEVEL_3_CONDITIONAL = "L3_CONDITIONAL"  # Executes end-to-end; escalates on defined thresholds.
    LEVEL_4_HIGH_AUTONOMY = "L4_HIGH"  # Fully autonomous within operational bounds.


class ExecutionStatus(Enum):
    """Result status of an agent task execution."""
    SUCCESS = "SUCCESS"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    FAILURE = "FAILURE"
    WAITING_INPUT = "WAITING_INPUT"


@dataclass
class AgentTask:
    """Represents an inbound work item mapped from BPMN tasks."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bpmn_task_ref: str = ""
    title: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


@dataclass
class AgentResult:
    """Represents the outcome of an agent's execution."""
    task_id: str
    agent_name: str
    status: ExecutionStatus
    output: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    escalation_reason: Optional[str] = None
    completed_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


class BaseAgent(ABC):
    """
    Abstract Base Class for all Autonomous AI Agents in Statsfirm.
    Encapsulates role definition, system prompts, tool invocation, and human escalation.
    """

    def __init__(
        self,
        name: str,
        role: str,
        autonomy_level: AutonomyLevel = AutonomyLevel.LEVEL_3_CONDITIONAL,
        system_prompt: str = ""
    ) -> None:
        self.name = name
        self.role = role
        self.autonomy_level = autonomy_level
        self.system_prompt = system_prompt
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register_tool(self, tool_name: str, tool_callable: Callable[..., Any]) -> None:
        """Register an executable capability/tool available to this agent."""
        self._tools[tool_name] = tool_callable

    def get_registered_tools(self) -> List[str]:
        """Return the list of tool identifiers available to this agent."""
        return list(self._tools.keys())

    def escalate_to_human(
        self,
        task: AgentTask,
        target_human_role: str,
        reason: str,
        context: Dict[str, Any]
    ) -> AgentResult:
        """
        Escalate execution to a designated human role (Gerencia, Finanzas, RRHH).
        Implements the Human-in-the-Loop governance policy.
        """
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=ExecutionStatus.ESCALATE_TO_HUMAN,
            escalation_reason=f"Escalado a [{target_human_role}]: {reason}",
            output={"escalated_to": target_human_role, "context": context},
            logs=[f"[{datetime.datetime.now().isoformat()}] Escalado formal a {target_human_role}."]
        )

    @abstractmethod
    def execute(self, task: AgentTask) -> AgentResult:
        """Core execution method to be implemented by each specialized agent."""
        pass
