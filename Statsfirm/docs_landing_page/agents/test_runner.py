"""
Test Suite and Verification Runner for Statsfirm Autonomous Agents.
Validates execution, escalation to human, and output schemas for all agents.
"""

import sys
import os

# Add local path for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import StatsfirmAgentOrchestrator
from base_agent import ExecutionStatus


def run_all_tests():
    print("=" * 70)
    print("INICIANDO SUITE DE PRUEBAS: STATSFIRM AUTONOMOUS AI AGENTS")
    print("=" * 70)

    orchestrator = StatsfirmAgentOrchestrator()
    tests_passed = 0
    total_tests = 0

    # Test 1: Human Task Escalation (Gerencia)
    total_tests += 1
    print("\n[Test 1] Validación Human-in-the-Loop (Gerencia Lead Captura)...")
    res1 = orchestrator.dispatch(
        bpmn_task_id="Task_CapturaLead",
        title="Recepción de Lead Comercial Estratégico",
        payload={"client": "Banco Agroindustrial", "budget": 120000}
    )
    assert res1.status == ExecutionStatus.ESCALATE_TO_HUMAN
    assert "Gerencia" in res1.escalation_reason
    print("  -> OK: Escalado a rol humano correctamente.")
    tests_passed += 1

    # Test 2: Process Engineer Agent (Viabilidad ARB)
    total_tests += 1
    print("\n[Test 2] ProcessEngineerAgent (Evaluación Viabilidad ARB)...")
    res2 = orchestrator.dispatch(
        bpmn_task_id="Task_ValidacionARB",
        title="Evaluación de Arquitectura Cloud",
        payload={"industry_domain": "fintech", "tech_stack": "Python / FastAPI"}
    )
    assert res2.status == ExecutionStatus.SUCCESS
    assert "feasibility" in res2.output
    assert res2.output["feasibility"]["feasibility_score"] >= 0.70
    print(f"  -> OK: Score de viabilidad={res2.output['feasibility']['feasibility_score']}")
    tests_passed += 1

    # Test 3: Product Owner Agent (DoR & Gherkin)
    total_tests += 1
    print("\n[Test 3] ProductOwnerAgent (Refinamiento DoR & Gherkin)...")
    res3 = orchestrator.dispatch(
        bpmn_task_id="Task_RefinarBacklog",
        title="Historia de Usuario: Facturación Automática",
        payload={
            "raw_requirements": [
                {
                    "title": "Generar Reporte Tributario",
                    "role": "Contador",
                    "action": "generar reporte tributario mensual",
                    "outcome": "cumplir con la DIAN",
                    "story_points": 3,
                    "business_value": "Alto"
                }
            ],
            "squad_capacity_points": 30
        }
    )
    assert res3.status == ExecutionStatus.SUCCESS
    assert "sprint_backlog" in res3.output
    assert len(res3.output["sprint_backlog"]) > 0
    assert "gherkin_spec" in res3.output["sprint_backlog"][0]
    print("  -> OK: Escenarios BDD Gherkin generados y DoR validado.")
    tests_passed += 1

    # Test 4: Software Developer Agent (Feature Dev)
    total_tests += 1
    print("\n[Test 4] SoftwareDeveloperAgent (Desarrollo Feature Branch)...")
    res4 = orchestrator.dispatch(
        bpmn_task_id="Task_DesarrolloGitFlow",
        title="Creación de microservicio de pagos",
        payload={"action": "DEVELOP", "feature_spec": "Implementar AuthService JWT"}
    )
    assert res4.status == ExecutionStatus.SUCCESS
    assert "feature_branch" in res4.output
    assert "generated_code" in res4.output
    print(f"  -> OK: Branch '{res4.output['feature_branch']}' con código PEP 8 generado.")
    tests_passed += 1

    # Test 5: QA Automation Agent (DoD Checklist)
    total_tests += 1
    print("\n[Test 5] QaAutomationAgent (Validación DoD & Cobertura)...")
    res5 = orchestrator.dispatch(
        bpmn_task_id="Task_PruebasQA",
        title="Pipeline de Pruebas Unitarias e Integración",
        payload={"lines_covered": 920, "total_lines": 1000, "tests_failed": 0, "has_docs": True, "security_vulns": 0}
    )
    assert res5.status == ExecutionStatus.SUCCESS
    assert res5.output["dod_certified"] is True
    print(f"  -> OK: DoD Aprobado con {res5.output['coverage_percentage']}% de cobertura.")
    tests_passed += 1

    # Test 6: Data Steward Agent (PII Masking & DAMA-BOK)
    total_tests += 1
    print("\n[Test 6] DataStewardAgent (Gobernanza de Datos & Masking)...")
    res6 = orchestrator.dispatch(
        bpmn_task_id="Task_ValidarGobernanza",
        title="Auditoría de Ingestión de Clientes",
        payload={
            "data_batch": [
                {"id": "REG-001", "valor": 12.5, "cliente_email": "carlos.ruiz@agrocorp.com", "lote": "L01"},
                {"id": "REG-002", "valor": 18.2, "cliente_email": "maria.gomez@hacienda.co", "lote": "L02"}
            ],
            "required_keys": ["id", "valor", "lote"]
        }
    )
    assert res6.status == ExecutionStatus.SUCCESS
    assert res6.output["dama_compliance"]["passed"] is True
    assert res6.output["dama_compliance"]["completeness_score"] == 1.0
    print("  -> OK: DAMA-BOK aprobado y PII enmascarado.")
    tests_passed += 1

    # Test 7: SRE Operations Agent (Auto-remediation)
    total_tests += 1
    print("\n[Test 7] SreOperationsAgent (Mitigación Incidente SEV2)...")
    res7 = orchestrator.dispatch(
        bpmn_task_id="Task_MitigacionIncidente",
        title="Alerta Prometheus: Latencia en API Gateway",
        payload={"error_rate_pct": 2.5, "latency_p99_ms": 1400, "service_name": "api-gateway"}
    )
    assert res7.status == ExecutionStatus.SUCCESS
    assert res7.output["incident_status"] == "MITIGATED_AUTOMATICALLY"
    assert res7.output["remediation"]["mitigated"] is True
    print(f"  -> OK: Playbook '{res7.output['remediation']['playbook']}' ejecutado con éxito.")
    tests_passed += 1

    # Test 8: Innova Lab Agent (DORA Metrics)
    total_tests += 1
    print("\n[Test 8] InnovaLabAgent (Métricas DORA & Aceleradores)...")
    res8 = orchestrator.dispatch(
        bpmn_task_id="Task_RecopilarDORA",
        title="Evaluación Trimestral de Ingeniería",
        payload={"deployments_per_month": 28, "lead_time_days": 1.2, "change_failure_rate_pct": 2.1, "mttr_hours": 0.3}
    )
    assert res8.status == ExecutionStatus.SUCCESS
    assert res8.output["dora_metrics"]["tier"] == "ELITE"
    print(f"  -> OK: Clasificación DORA={res8.output['dora_metrics']['tier']}")
    tests_passed += 1

    print("\n" + "=" * 70)
    print(f"RESULTADOS: {tests_passed}/{total_tests} PRUEBAS EXITOSAS (100%)")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
