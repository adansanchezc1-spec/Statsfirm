"""Data Quality Validator Domain Service.

Enforces DAMA-BOK quality dimensions (Completeness, Validity, Consistency, Uniqueness).
Does not mutate source records silently; rejects invalid data to the Dead Letter Queue.
Normative:
- DAMA-BOK Data Quality Framework
- Clean Code (Single Responsibility Principle)
"""

from datetime import date, datetime
from typing import Any, Dict, List, Tuple

from agrostat_app.domain.entities import HarvestBatch
from agrostat_app.domain.exceptions import InvariantViolationException
from agrostat_app.domain.value_objects import DataQualityReport


class DataQualityValidator:
    """Domain service for validating agronomic harvest datasets against data contracts."""

    REQUIRED_FIELDS = [
        "batch_id",
        "lote_id",
        "fecha_cosecha",
        "hectareas_lote",
        "kilos_totales",
        "kilos_exportables",
        "calibre_promedio",
        "grados_brix",
    ]

    BRIX_RANGE = (4.0, 32.0)
    CALIBRE_RANGE = (10.0, 95.0)
    PH_RANGE = (3.5, 9.5)

    def validate_batch_stream(
        self, raw_records: List[Dict[str, Any]]
    ) -> Tuple[List[HarvestBatch], List[Dict[str, Any]], DataQualityReport]:
        """Validates a stream of raw dictionary records.

        Returns:
            Tuple containing:
            - Valid HarvestBatch entity objects.
            - Quarantined raw records with error diagnostics for the DLQ.
            - Consolidated DataQualityReport object.
        """
        valid_batches: List[HarvestBatch] = []
        quarantined_records: List[Dict[str, Any]] = []
        validation_errors: List[Dict[str, Any]] = []
        seen_batch_ids = set()

        total_records = len(raw_records)
        if total_records == 0:
            empty_report = DataQualityReport(
                total_records=0,
                valid_records=0,
                quarantined_records=0,
                completeness_rate=1.0,
                validity_rate=1.0,
                consistency_rate=1.0,
                validation_errors=[],
            )
            return [], [], empty_report

        completeness_passes = 0
        validity_passes = 0
        consistency_passes = 0

        for idx, record in enumerate(raw_records, start=1):
            errors = []

            # 1. Completitud (Required fields check)
            missing = [f for f in self.REQUIRED_FIELDS if record.get(f) is None or str(record.get(f)).strip() == ""]
            if missing:
                errors.append(f"Dimension Completitud violada: Campos obligatorios faltantes: {missing}")
            else:
                completeness_passes += 1

            # 2. Unicidad (Batch ID collision check)
            b_id = str(record.get("batch_id", ""))
            if b_id in seen_batch_ids:
                errors.append(f"Dimension Unicidad violada: batch_id '{b_id}' duplicado en este archivo")
            else:
                seen_batch_ids.add(b_id)

            # 3. Validez de Tipos y Rangos Agronómicos
            if not errors:
                try:
                    kilos_tot = float(record["kilos_totales"])
                    kilos_exp = float(record.get("kilos_exportables", 0.0))
                    brix = float(record["grados_brix"])
                    calibre = float(record["calibre_promedio"])
                    has_range_error = False

                    if not (self.BRIX_RANGE[0] <= brix <= self.BRIX_RANGE[1]):
                        errors.append(
                            f"Validez violada: grados_brix ({brix}) fuera de rango admisible {self.BRIX_RANGE}"
                        )
                        has_range_error = True

                    if not (self.CALIBRE_RANGE[0] <= calibre <= self.CALIBRE_RANGE[1]):
                        errors.append(
                            f"Validez violada: calibre ({calibre}) fuera de rango admisible {self.CALIBRE_RANGE}"
                        )
                        has_range_error = True

                    ph = record.get("ph_suelo")
                    if ph is not None and str(ph).strip() != "":
                        ph_val = float(ph)
                        if not (self.PH_RANGE[0] <= ph_val <= self.PH_RANGE[1]):
                            errors.append(
                                f"Validez violada: ph_suelo ({ph_val}) fuera de rango admisible {self.PH_RANGE}"
                            )
                            has_range_error = True

                    if not has_range_error:
                        validity_passes += 1

                    # 4. Consistencia Lógica de Dominio
                    if kilos_exp > kilos_tot:
                        errors.append(
                            f"Consistencia violada: kilos_exportables ({kilos_exp}) > kilos_totales ({kilos_tot})"
                        )
                    else:
                        consistency_passes += 1

                except (ValueError, TypeError) as exc:
                    errors.append(f"Validez violada: Formato numérico inválido: {str(exc)}")

            # Si no hay errores, se construye la entidad de dominio
            if not errors:
                try:
                    batch_entity = HarvestBatch.from_dict(record)
                    valid_batches.append(batch_entity)
                except InvariantViolationException as inv_err:
                    errors.append(f"Invariante de Dominio violada: {inv_err.message}")

            # Si hubo errores, enviar a cuarentena (DLQ)
            if errors:
                diagnostic = {
                    "row_index": idx,
                    "batch_id": record.get("batch_id"),
                    "lote_id": record.get("lote_id"),
                    "errors": errors,
                    "raw_payload": record,
                    "quarantined_at": datetime.utcnow().isoformat(),
                }
                quarantined_records.append(diagnostic)
                validation_errors.append(diagnostic)

        report = DataQualityReport(
            total_records=total_records,
            valid_records=len(valid_batches),
            quarantined_records=len(quarantined_records),
            completeness_rate=completeness_passes / total_records,
            validity_rate=validity_passes / total_records,
            consistency_rate=consistency_passes / total_records,
            validation_errors=validation_errors,
        )

        return valid_batches, quarantined_records, report
