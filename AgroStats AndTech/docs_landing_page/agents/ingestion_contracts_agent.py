"""
Ingestion & Data Contracts AI Agent for Agro Stat & Tech Co.
Responsible for:
- Ingesta multi-protocolo de archivos provistos por el productor (Excel, CSV, API ERP).
- Validación de esquemas y contratos de datos biofísicos (Data Contracts / DAMA-BOK).
- Aislamiento automático de inconsistencias y outliers hacia la Dead Letter Queue (DLQ).
"""

from typing import Any, Dict, List
try:
    from .base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus
except (ImportError, ValueError):
    from base_agro_agent import BaseAgroAgent, AgroTask, AgroResult, AgroAutonomyLevel, AgroExecutionStatus


class IngestionContractsAgent(BaseAgroAgent):
    """
    Autonomous AI Agent executing data ingestion and schema/range contract enforcement.
    """

    def __init__(self) -> None:
        system_prompt = (
            "Eres el Agente de Ingesta & Data Contracts de Agro Stat & Tech Co. "
            "Tu misión es verificar que ningún registro corrupto, incompleto o con valores "
            "biológicamente imposibles (ej. pH > 14, grados Brix negativos o desproporcionados) "
            "contamine el Lakehouse analítico. Validas esquemas estrictos contra Data Contracts "
            "y enrutas cualquier anomalía a la Dead Letter Queue (DLQ) para que el cliente la corrija."
        )
        super().__init__(
            name="Agente_Ingesta_DataContracts_AI",
            role="Data Contracts & Ingestion Gatekeeper",
            autonomy_level=AgroAutonomyLevel.LEVEL_4_HIGH_AUTONOMY,
            system_prompt=system_prompt
        )
        self.register_tool("contract_validator", self._validate_record)

    def _validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single record against biological and syntactic bounds."""
        errors: List[str] = []
        
        # Check required fields
        for req in ["lote_id", "fecha_cosecha", "kilos_totales", "grados_brix"]:
            if req not in record or record[req] is None:
                errors.append(f"Campo obligatorio faltante: '{req}'")

        # Range checks
        brix = record.get("grados_brix")
        if brix is not None and not (4.0 <= brix <= 32.0):
            errors.append(f"Grados Brix fuera de rango biológico (4.0 - 32.0): {brix}")

        kilos = record.get("kilos_totales")
        if kilos is not None and kilos <= 0:
            errors.append(f"Kilos cosechados debe ser mayor a 0: {kilos}")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def execute(self, task: AgroTask) -> AgroResult:
        """Execute batch ingestion and quarantine routing."""
        logs = [f"Iniciando validación de dataset para lote: {task.lote_id}"]
        payload = task.payload
        dataset = payload.get("records", [
            {"lote_id": task.lote_id or "L04-HASS", "fecha_cosecha": "2026-09-10", "kilos_totales": 12500, "grados_brix": 11.4},
            {"lote_id": task.lote_id or "L04-HASS", "fecha_cosecha": "2026-09-11", "kilos_totales": 14200, "grados_brix": 12.1},
            {"lote_id": task.lote_id or "L04-HASS", "fecha_cosecha": "2026-09-12", "kilos_totales": -50, "grados_brix": 45.0}  # Anomaly
        ])

        valid_records: List[Dict[str, Any]] = []
        quarantined_records: List[Dict[str, Any]] = []

        for idx, row in enumerate(dataset):
            val_result = self._validate_record(row)
            if val_result["valid"]:
                valid_records.append(row)
            else:
                quarantined_records.append({
                    "row_index": idx,
                    "record": row,
                    "rejection_reasons": val_result["errors"]
                })

        logs.append(f"Validación finalizada: {len(valid_records)} válidos, {len(quarantined_records)} en cuarentena DLQ.")

        output_data = {
            "total_processed": len(dataset),
            "valid_count": len(valid_records),
            "quarantined_count": len(quarantined_records),
            "valid_records_sample": valid_records[:3],
            "dlq_payload": quarantined_records,
            "status_message": "Dataset ingestando exitosamente con derivación DLQ preventiva."
        }

        # If more than 50% are anomalous, flag for review
        if len(quarantined_records) > (len(dataset) * 0.5):
            return self.escalate_to_human(
                task=task,
                target_human_role="Gerencia Agrícola / Soporte al Productor",
                reason="Más del 50% de los registros del lote están corruptos o fuera de rango biológico.",
                context=output_data
            )

        return AgroResult(
            task_id=task.task_id,
            agent_name=self.name,
            status=AgroExecutionStatus.SUCCESS if len(valid_records) > 0 else AgroExecutionStatus.FAILURE,
            output=output_data,
            logs=logs
        )
