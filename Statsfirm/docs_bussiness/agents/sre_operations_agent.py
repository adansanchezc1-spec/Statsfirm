"""
SRE On-Call & Incident Mitigation AI Agent for Statsfirm Co.
Responsible for:
- Monitoreo de telemetría y alertas operativas (Task_TelemetriaPrometheus).
- Gestión técnica de incidentes con SLA < 15 min y Post-Mortem (Task_MitigacionIncidente).
- Remediación automatizada de incidencias (reinicio de pods, rollback, escalamiento).
"""

from typing import Any, Dict
try:
    from .base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentTask, AgentResult, AutonomyLevel, ExecutionStatus


class SreOperationsAgent(BaseAgent):
    """
    Autonomous AI Agent executing 24/7 SRE monitoring, automated triaging and self-healing playbooks.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente SRE On-Call & Observabilidad 24/7 de Statsfirm Co. "
            "Tu misión es preservar la alta disponibilidad (SLA 99.9%) y el rendimiento de los "
            "servicios cloud. Cuando ocurre un incidente, ejecutas triaging en menos de 15 minutos, "
            "aplicas playbooks automatizados de autorreparación y redactas el post-mortem técnico. "
            "Si el incidente es SEV-1 con impacto generalizado, ejecutas contención y escalas a Gerencia y CISO."
        )
        super().__init__(
            name="SRE_OnCall_Mitigation_AI",
            role="Site Reliability Engineer & Incident Mitigation Lead",
            autonomy_level=AutonomyLevel.LEVEL_3_CONDITIONAL,
            system_prompt=system_prompt
        )
        self.register_tool("playbook_engine", self._execute_playbook)
        self.register_tool("incident_triager", self._triage_incident)

    def _triage_incident(self, alert_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Classify severity and identify remediation target."""
        error_rate = alert_payload.get("error_rate_pct", 0.0)
        latency_p99 = alert_payload.get("latency_p99_ms", 100)

        if error_rate > 5.0 or latency_p99 > 3000:
            severity = "SEV-1"
        elif error_rate > 1.0 or latency_p99 > 1000:
            severity = "SEV-2"
        else:
            severity = "SEV-3"

        return {
            "severity": severity,
            "root_cause_hypothesis": "Agotamiento de memoria en worker pods" if error_rate > 5.0 else "Degradación transitoria de red",
            "recommended_playbook": "scale_horizontal_and_restart" if severity in ["SEV-1", "SEV-2"] else "monitor_trend"
        }

    def _execute_playbook(self, playbook_name: str, target_service: str) -> Dict[str, Any]:
        """Simulate autonomous remediation playbook execution."""
        return {
            "playbook": playbook_name,
            "target": target_service,
            "actions_taken": [
                f"K8s deployment '{target_service}' scaled to 5 replicas.",
                f"Graceful restart executed on unhealthy pods in '{target_service}'.",
                "Traffic rerouted through healthy cluster endpoints."
            ],
            "mitigated": True
        }

    def execute(self, task: AgentTask) -> AgentResult:
        """Execute automated incident response and self-healing."""
        logs = [f"Alerta SRE recibida para: {task.title}"]
        payload = task.payload

        triaging = self._triage_incident(payload)
        logs.append(f"Triaje completado. Severidad={triaging['severity']}")

        target_svc = payload.get("service_name", "lakehouse-ingestion-api")
        playbook_result = self._execute_playbook(triaging["recommended_playbook"], target_svc)
        logs.append(f"Playbook '{triaging['recommended_playbook']}' ejecutado con éxito.")

        # If SEV-1, trigger escalation notification to Board/CISO
        if triaging["severity"] == "SEV-1":
            return self.escalate_to_human(
                task=task,
                target_human_role="CISO & Gerencia de Operaciones",
                reason=f"Incidente crítico SEV-1 en servicio '{target_svc}'. Remediación automática aplicada; requiere validación de CISO.",
                context={"triaging": triaging, "remediation": playbook_result}
            )

        output_data = {
            "incident_status": "MITIGATED_AUTOMATICALLY",
            "triaging": triaging,
            "remediation": playbook_result,
            "post_mortem_draft": f"Post-mortem preliminar para {target_svc}: Mitigado en < 5 minutos por SRE AI Agent."
        }

        return AgentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=ExecutionStatus.SUCCESS,
            output=output_data,
            logs=logs
        )
