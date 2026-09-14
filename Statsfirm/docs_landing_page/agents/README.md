# Statsfirm Autonomous AI Agents Package

Paquete de Agentes de Inteligencia Artificial Autónomos para **Statsfirm Co.** implementados bajo el marco **PDCO**, estándares **SWEBOK / DAMA-BOK**, y principios **SOLID / Clean Code (PEP 8)**.

---

## 1. Arquitectura Híbrida: Agentes IA + Human-in-the-Loop (HITL)

Siguiendo la especificación formal del proceso BPMN (`bpmn/statsfirm_organizacion_procesos.bpmn`), todas las operaciones técnicas, de ingeniería, calidad, arquitectura y gobernanza son delegadas a **Agentes IA Autónomos**.

Las únicas funciones reservadas exclusivamente para **Humanos** son:
- **Gerencia / Ejecutivo Comercial**: Captura y negociación de leads de alto valor (`HUMAN_GERENCIA`).
- **Finanzas / FinOps**: Modelado financiero y pricing de contratos (`HUMAN_FINANZAS`).
- **Legal Counsel**: Validación y formalización legal (`HUMAN_LEGAL_FINANZAS`).
- **Recursos Humanos**: Gobernanza de talento y asignación organizacional (`HUMAN_RRHH`).

Cualquier intento del orquestador de despachar una tarea reservada a un rol humano genera de forma determinista un estado `ESCALATE_TO_HUMAN`.

---

## 2. Inventario de Agentes

| Agente | Archivo | Autonomía | Responsabilidad Principal |
|---|---|---|---|
| `ProcessEngineerAgent` | `process_engineer_agent.py` | L4 | Evaluación de viabilidad arquitectónica (ARB), modelado BPMN y diagnóstico de madurez. |
| `ProductOwnerAgent` | `product_owner_agent.py` | L3 | Refinamiento de historias de usuario, generación de criterios Gherkin BDD y validación DoR. |
| `SoftwareDeveloperAgent` | `software_developer_agent.py` | L4 | Generación de código Python/Java limpio, linter PEP 8 y revisión estricta de Pull Requests. |
| `QaAutomationAgent` | `qa_automation_agent.py` | L4 | Verificación de Definition of Done (DoD), cobertura de pruebas unitarias (>80%) y regresión. |
| `DataStewardAgent` | `data_steward_agent.py` | L4 | Enmascaramiento de PII, validación de calidad del dato (DAMA-BOK) e integridad de esquemas. |
| `SreOperationsAgent` | `sre_operations_agent.py` | L3 | Triage y autosanación de incidentes SEV1-SEV3, métricas Prometheus y runbooks. |
| `InnovaLabAgent` | `innova_lab_agent.py` | L4 | Cálculo de métricas DORA, análisis de fricción técnica y propuestas de aceleradores. |
| `StatsfirmAgentOrchestrator` | `orchestrator.py` | L4 | Orquestador central y puente con el motor BPMN Camunda. |

---

## 3. Estructura de Clases Base

- `BaseAgent`: Clase abstracta (`ABC`) que define el contrato `execute(task: AgentTask) -> AgentResult`.
- `AgentTask`: Dataclass que encapsula `task_id`, `bpmn_task_ref`, `title`, `payload` y `timestamp`.
- `AgentResult`: Dataclass estandarizada que contiene `status`, `output`, `logs`, `metrics` y `escalation_reason`.
- `AutonomyLevel`: Enumeración (`L1_ASSISTED`, `L2_DELEGATED`, `L3_CONDITIONAL_AUTONOMOUS`, `L4_HIGH_AUTONOMY`, `L5_FULL_AUTONOMY`).
- `ExecutionStatus`: Enumeración (`SUCCESS`, `FAILED`, `ESCALATE_TO_HUMAN`, `IN_PROGRESS`).

---

## 4. Modo de Uso

### Importación como Paquete:
```python
from agents import StatsfirmAgentOrchestrator

orchestrator = StatsfirmAgentOrchestrator()

# Ejecutar una tarea de desarrollo
res = orchestrator.dispatch(
    bpmn_task_id="Task_DesarrolloGitFlow",
    title="Implementar API de autenticación JWT",
    payload={"component": "AuthService", "language": "python"}
)

print(res.status)  # ExecutionStatus.SUCCESS
print(res.output)
```

### Ejecución de Pruebas Unitarias y Validación:
```bash
python test_runner.py
```
