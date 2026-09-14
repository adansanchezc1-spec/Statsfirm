"""
Base Agro Agent Module for Agro Stat & Tech Co. (AgroStats)
Defines the abstract base class and contract for Autonomous AI Bio-Statistical Agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import datetime
import uuid


class AgroAutonomyLevel(Enum):
    """Operational autonomy degrees for AgroStats AI agents."""
    LEVEL_1_ADVISORY = "L1_ADVISORY"
    LEVEL_2_SUPERVISED = "L2_SUPERVISED"
    LEVEL_3_CONDITIONAL = "L3_CONDITIONAL"
    LEVEL_4_HIGH_AUTONOMY = "L4_HIGH"


class AgroExecutionStatus(Enum):
    """Execution status for agricultural agent tasks."""
    SUCCESS = "SUCCESS"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    FAILURE = "FAILURE"
    QUARANTINE_DLQ = "QUARANTINE_DLQ"


@dataclass
class AgroTask:
    """Represents a work package mapped from AgroStats BPMN tasks."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    bpmn_task_ref: str = ""
    title: str = ""
    lote_id: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


@dataclass
class AgroResult:
    """Outcome produced by an AgroStats agent."""
    task_id: str
    agent_name: str
    status: AgroExecutionStatus
    output: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    escalation_reason: Optional[str] = None
    completed_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


class BaseAgroAgent(ABC):
    """
    Abstract Base Class for all AgroStats Bio-Statistical and Process AI Agents.
    Enforces pure data analysis, SPC calculations, and zero reliance on hardware/sensors.
    """

    def __init__(
        self,
        name: str,
        role: str,
        autonomy_level: AgroAutonomyLevel = AgroAutonomyLevel.LEVEL_3_CONDITIONAL,
        system_prompt: str = ""
    ) -> None:
        self.name = name
        self.role = role
        self.autonomy_level = autonomy_level
        self.system_prompt = system_prompt
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register_tool(self, tool_name: str, tool_callable: Callable[..., Any]) -> None:
        """Register an agronomic or statistical calculation tool."""
        self._tools[tool_name] = tool_callable

    def escalate_to_human(
        self,
        task: AgroTask,
        target_human_role: str,
        reason: str,
        context: Dict[str, Any]
    ) -> AgroResult:
        """Escalate to human roles (Gerencia Agroempresarial, FinOps Share-of-Gain, Legal)."""
        return AgroResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=AgroExecutionStatus.ESCALATE_TO_HUMAN,
            escalation_reason=f"Escalado a [{target_human_role}]: {reason}",
            output={"escalated_to": target_human_role, "context": context},
            logs=[f"[{datetime.datetime.now().isoformat()}] Escalado a rol humano {target_human_role}."]
        )

    @abstractmethod
    def execute(self, task: AgroTask) -> AgroResult:
        """Core execution logic for each specialized agro agent."""
        pass
