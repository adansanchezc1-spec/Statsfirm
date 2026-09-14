"""
Test Suite and Verification Runner for AgroStats Autonomous AI Agents.
Validates execution, biological boundary checking, SPC limits, Kriging interpolation,
Yield AI forecasts, BPMN optimization ROI, and escalation to human roles.
"""

import sys
import os

# Add local path for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agro_orchestrator import AgroStatsAgentOrchestrator
from base_agro_agent import AgroExecutionStatus


def run_all_tests():
    print("=" * 75)
    print("INICIANDO SUITE DE PRUEBAS: AGROSTATS AUTONOMOUS BIO-STATISTICAL AI AGENTS")
    print("=" * 75)

    orchestrator = AgroStatsAgentOrchestrator()
    tests_passed = 0
    total_tests = 0

    # Test 1: Human Task Escalation (Gerencia Agrícola)
    total_tests += 1
    print("\n[Test 1] Validación Human-in-the-Loop (Gerencia Lead Agropecuario)...")
    res1 = orchestrator.dispatch(
        bpmn_task_id="Task_EvaluarLeadAgro",
        title="Evaluación de Factibilidad Productor Exportador",
        lote_id="AGRO-LEAD-001",
        payload={"client": "Agropecuaria del Sinú", "hectareas": 350, "cultivo": "Aguacate Hass"}
    )
    assert res1.status == AgroExecutionStatus.ESCALATE_TO_HUMAN
    assert "Gerencia" in res1.escalation_reason
    print("  -> OK: Escalado a rol humano reservado exitosamente.")
    tests_passed += 1

    # Test 2: Ingestion & Data Contracts Agent
    total_tests += 1
    print("\n[Test 2] IngestionContractsAgent (Validación de Esquema y Cuarentena DLQ)...")
    res2 = orchestrator.dispatch(
        bpmn_task_id="Task_ValidarDataContracts",
        title="Ingesta y Validación de Contratos de Datos",
        lote_id="LOTE-04-HASS",
        payload={
            "records": [
                {"lote_id": "LOTE-04-HASS", "fecha_cosecha": "2026-09-10", "kilos_totales": 12500, "grados_brix": 11.4},
                {"lote_id": "LOTE-04-HASS", "fecha_cosecha": "2026-09-11", "kilos_totales": 14200, "grados_brix": 12.1},
                {"lote_id": "LOTE-04-HASS", "fecha_cosecha": "2026-09-12", "kilos_totales": -50, "grados_brix": 45.0}  # Anomaly
            ]
        }
    )
    assert res2.status == AgroExecutionStatus.SUCCESS
    assert res2.output["valid_count"] == 2
    assert res2.output["quarantined_count"] == 1
    print(f"  -> OK: {res2.output['valid_count']} válidos, {res2.output['quarantined_count']} enrutados a DLQ.")
    tests_passed += 1

    # Test 3: Lakehouse & Geospatial Curation Agent (Kriging)
    total_tests += 1
    print("\n[Test 3] LakehouseGeospatialAgent (Delta Lake & Kriging)...")
    res3 = orchestrator.dispatch(
        bpmn_task_id="Task_CuraduriaDelta",
        title="Curaduría Silver Lake e Interpolación Geoespacial",
        lote_id="LOTE-04-HASS",
        payload={
            "sample_points": [
                {"x": -75.52, "y": 6.25, "val": 28.5},
                {"x": -75.53, "y": 6.26, "val": 30.1},
                {"x": -75.51, "y": 6.24, "val": 26.8},
                {"x": -75.54, "y": 6.27, "val": 29.4}
            ]
        }
    )
    assert res3.status == AgroExecutionStatus.SUCCESS
    assert "kriging_analysis" in res3.output
    assert res3.output["kriging_analysis"]["interpolated_cells"] > 0
    print(f"  -> OK: Modelo Kriging completado ({res3.output['kriging_analysis']['interpolated_cells']} celdas estimadas).")
    tests_passed += 1

    # Test 4: Biostatistical SPC Agent (Shewhart & Western Electric)
    total_tests += 1
    print("\n[Test 4] BiostatisticalSpcAgent (Cartas de Control Shewhart & Cpk)...")
    res4 = orchestrator.dispatch(
        bpmn_task_id="Task_CalculoLimitesSPC",
        title="Auditoría Bioestadística de Grados Brix",
        lote_id="LOTE-04-HASS",
        payload={
            "variable": "grados_brix",
            "observations": [
                11.2, 11.5, 11.3, 11.4, 11.6, 11.4, 11.5, 11.3, 11.7, 11.4,
                11.5, 11.6, 11.8, 11.4, 11.5, 11.3, 11.6, 11.4, 11.5, 11.5
            ],
            "usl": 13.0,
            "lsl": 10.0
        }
    )
    assert res4.status == AgroExecutionStatus.SUCCESS
    assert res4.output["process_in_control"] is True
    assert res4.output["capability_indices"]["cpk"] >= 1.33
    print(f"  -> OK: Proceso en control estadístico (Cpk={res4.output['capability_indices']['cpk']}).")
    tests_passed += 1

    # Test 5: Yield AI & Phenological Modeling Agent (GDD)
    total_tests += 1
    print("\n[Test 5] YieldAiAgent (Modelado Térmico GDD & Proyección Cosecha)...")
    res5 = orchestrator.dispatch(
        bpmn_task_id="Task_EntrenamientoYieldAI",
        title="Inferencia de Rendimiento y Ventana de Cosecha",
        lote_id="LOTE-04-HASS",
        payload={
            "crop": "Aguacate Hass",
            "hectareas": 40.0,
            "t_base": 10.0,
            "daily_temps": [{"t_max": 25.5, "t_min": 14.5}] * 100
        }
    )
    assert res5.status == AgroExecutionStatus.SUCCESS
    assert "yield_forecast" in res5.output
    assert res5.output["yield_forecast"]["projected_ton_ha"] > 0
    print(f"  -> OK: Proyección={res5.output['yield_forecast']['projected_ton_ha']} Ton/Ha.")
    tests_passed += 1

    # Test 6: BPMN Optimization & Lean Six Sigma Agent
    total_tests += 1
    print("\n[Test 6] BpmnOptimizationAgent (Diagnóstico As-Is & ROI Share-of-Gain)...")
    res6 = orchestrator.dispatch(
        bpmn_task_id="Task_AuditoriaCuellosBotella",
        title="Rediseño de Flujo Operativo y Detección de Mermas",
        lote_id="LOTE-04-HASS",
        payload={
            "hectareas": 60.0,
            "process_steps": [
                {"name": "Corte y Recolección", "cycle_time_mins": 30, "reject_rate_pct": 1.0},
                {"name": "Tránsito a Acopio", "cycle_time_mins": 55, "reject_rate_pct": 3.9},
                {"name": "Selección y Calibrado", "cycle_time_mins": 25, "reject_rate_pct": 4.2}
            ]
        }
    )
    assert res6.status == AgroExecutionStatus.SUCCESS
    assert len(res6.output["as_is_bottlenecks"]) > 0
    assert res6.output["financial_impact_share_of_gain"]["projected_savings_usd"] > 0
    print(f"  -> OK: Ahorro proyectado Share-of-Gain: ${res6.output['financial_impact_share_of_gain']['projected_savings_usd']} USD.")
    tests_passed += 1

    # Test 7: AgroInnova Lab Agent (Seasonal Residual Calibration)
    total_tests += 1
    print("\n[Test 7] AgroInnovaLabAgent (Calibración Algorítmica de Fin de Temporada)...")
    res7 = orchestrator.dispatch(
        bpmn_task_id="Task_RetrospectivaAgroInnova",
        title="Ajuste Residual de Algoritmos Predictivos",
        lote_id="LOTE-04-HASS",
        payload={"predicted_yield": 21.5, "actual_yield": 22.1}
    )
    assert res7.status == AgroExecutionStatus.SUCCESS
    assert res7.output["calibration_report"]["algorithm_accuracy_pct"] >= 95.0
    print(f"  -> OK: Calibración finalizada con {res7.output['calibration_report']['algorithm_accuracy_pct']}% de exactitud.")
    tests_passed += 1

    print("\n" + "=" * 75)
    print(f"RESULTADOS: {tests_passed}/{total_tests} PRUEBAS EXITOSAS (100%)")
    print("=" * 75)


if __name__ == "__main__":
    run_all_tests()
