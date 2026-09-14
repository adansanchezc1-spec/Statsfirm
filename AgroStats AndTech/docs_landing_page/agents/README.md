# AgroStats Autonomous Bio-Statistical AI Agents Package

Paquete de Agentes de Inteligencia Artificial Bioestadísticos y de Optimización de Procesos para **Agro Stat & Tech Co. (AgroStats)**, implementado bajo el marco **PDCO**, estándares **DAMA-BOK / ISO 29148 / SWEBOK**, y principios **SOLID / Clean Code (PEP 8)**.

---

## 1. Misión Estricta de AgroStats: Cero Hardware / Cero Sensores

AgroStats **no fabrica, no vende, no instala ni opera sensores físicos, dispositivos IoT ni gateways LoRaWAN**.
Toda la inteligencia y valor del sistema se derivan del análisis riguroso de **datasets agropecuarios existentes provistos por el cliente** (archivos Excel, CSV, ERPs agrícolas y registros agronómicos de campo).

---

## 2. Arquitectura de Agentes & Human-in-the-Loop (HITL)

Siguiendo el proceso BPMN formal (`bpmn/agrostats_procesos_analiticos.bpmn`), todas las tareas analíticas, geoestadísticas, bioestadísticas y de modelado son operadas por **Agentes IA Autónomos**.

Las únicas decisiones reservadas para **Humanos** son:
- **Gerencia Agrícola**: Evaluación estratégica de leads y certificación final de incremento de valor (`HUMAN_GERENCIA_AGRO`).
- **Finanzas / FinOps**: Modelado del esquema de éxito Share-of-Gain y facturación de comisiones (`HUMAN_FINANZAS_FINOPS`).
- **Legal Counsel**: Emisión y validación del acuerdo de confidencialidad y términos de servicio (`HUMAN_LEGAL`).
- **Productor / Agroexportador**: Carga de datos, firma digital y aprobación de planes de mejora To-Be (`HUMAN_PRODUCTOR`).

---

## 3. Inventario de Agentes Agroestadísticos

| Agente | Archivo | Autonomía | Responsabilidad Principal |
|---|---|---|---|
| `IngestionContractsAgent` | `ingestion_contracts_agent.py` | L4 | Validación de Data Contracts, chequeo de rangos biológicos (grados Brix, volúmenes) y derivación a Dead Letter Queue (DLQ). |
| `LakehouseGeospatialAgent` | `lakehouse_geospatial_agent.py` | L4 | Curaduría de datos hacia Delta Lake (Silver/Gold), particionamiento temporal y modelado espacial por Kriging ordinario. |
| `BiostatisticalSpcAgent` | `biostatistical_spc_agent.py` | L4 | Cartas de control Shewhart ($\pm 3\sigma$), evaluación algorítmica de Reglas Western Electric, cálculo de $C_p, C_{pk}$ y ANOVA. |
| `YieldAiAgent` | `yield_ai_agent.py` | L4 | Proyección de maduración por Grados-Día de Desarrollo (GDD), ventana óptima de cosecha y predicción Ton/Ha (IC 95%). |
| `BpmnOptimizationAgent` | `bpmn_optimization_agent.py` | L4 | Detección de cuellos de botella en labores de cultivo y cosecha, modelado Lean Six Sigma To-Be y ROI financiero Share-of-Gain. |
| `AgroInnovaLabAgent` | `agroinnova_lab_agent.py` | L3 | Calibración algorítmica de fin de temporada comparando proyecciones contra rendimientos reales consolidados de cosecha. |
| `AgroStatsAgentOrchestrator` | `agro_orchestrator.py` | L4 | Orquestador central de tareas BPMN y enrutador dinámico hacia agentes o roles humanos HITL. |

---

## 4. Modo de Uso

### Importación como Paquete:
```python
from agents import AgroStatsAgentOrchestrator

orchestrator = AgroStatsAgentOrchestrator()

# Ejecutar auditoría bioestadística SPC
resultado = orchestrator.dispatch(
    bpmn_task_id="Task_CalculoLimitesSPC",
    title="Control Estadístico de Calibre y Grados Brix",
    lote_id="LOTE-04-HASS",
    payload={
        "variable": "grados_brix",
        "observations": [11.2, 11.5, 11.4, 11.6, 11.5, 11.3, 11.7, 11.4, 11.5],
        "usl": 13.0,
        "lsl": 10.0
    }
)

print(resultado.status)  # AgroExecutionStatus.SUCCESS
print(resultado.output["capability_indices"])
```

### Ejecución de Pruebas Unitarias y Validación:
```bash
python test_runner.py
```
