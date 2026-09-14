"""Data Quality Validator Domain Service.

Enforces DAMA-BOK quality dimensions (Completeness, Validity, Consistency, Uniqueness).
Does not mutate source records silently; rejects invalid data to the Dead Letter Queue.
Normative:
- DAMA-BOK Data Quality Framework
- Clean Code (Single Responsibility Principle)
- IEEE 830 / ISO 29148 Requerimientos Funcionales RF-006 a RF-010
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from agrostat_app.domain.entities import (
    CotizacionMayorista,
    HarvestBatch,
    ObservacionClimatica,
    RegistroAbastecimiento,
)
from agrostat_app.domain.exceptions import InvariantViolationException
from agrostat_app.domain.value_objects import CpcProductCode, DataQualityReport, DivipolaCode


class DataQualityValidator:
    """Domain service for validating agricultural datasets against DAMA-BOK data quality dimensions."""

    # Constantes para HarvestBatch
    HARVEST_REQUIRED_FIELDS = [
        "batch_id", "lote_id", "fecha_cosecha", "hectareas_lote",
        "kilos_totales", "kilos_exportables", "calibre_promedio", "grados_brix",
    ]
    BRIX_RANGE = (4.0, 32.0)
    CALIBRE_RANGE = (10.0, 95.0)
    PH_RANGE = (3.5, 9.5)

    # Constantes para Precios Mayoristas (DANE SIPSA_P)
    SIPSA_P_REQUIRED_FIELDS = [
        "fecha", "mercado_id", "codigo_cpc", "precio_min_kg", "precio_prom_kg", "precio_max_kg"
    ]

    # Constantes para Abastecimiento (DANE SIPSA_A)
    SIPSA_A_REQUIRED_FIELDS = [
        "fecha", "mercado_id", "codigo_cpc", "codigo_mpio_origen", "volumen_toneladas"
    ]

    # Constantes para Clima (IDEAM / NASA)
    CLIMA_REQUIRED_FIELDS = [
        "fecha", "estacion_id", "codigo_mpio", "precipitacion_mm"
    ]

    def validate_batch_stream(
        self, raw_records: List[Dict[str, Any]]
    ) -> Tuple[List[HarvestBatch], List[Dict[str, Any]], DataQualityReport]:
        """Validates a stream of raw dictionary harvest records."""
        valid_batches: List[HarvestBatch] = []
        quarantined_records: List[Dict[str, Any]] = []
        validation_errors: List[Dict[str, Any]] = []
        seen_batch_ids: Set[str] = set()

        total_records = len(raw_records)
        if total_records == 0:
            return [], [], self._empty_report()

        completeness_passes = 0
        validity_passes = 0
        consistency_passes = 0

        for idx, record in enumerate(raw_records, start=1):
            errors: List[str] = []

            # 1. Completitud
            missing = [f for f in self.HARVEST_REQUIRED_FIELDS if record.get(f) is None or str(record.get(f)).strip() == ""]
            if missing:
                errors.append(f"Dimension Completitud violada: Campos obligatorios faltantes: {missing}")
            else:
                completeness_passes += 1

            # 2. Unicidad
            b_id = str(record.get("batch_id", ""))
            if b_id in seen_batch_ids:
                errors.append(f"Dimension Unicidad violada: batch_id '{b_id}' duplicado en este archivo")
            else:
                seen_batch_ids.add(b_id)

            # 3. Validez y Consistencia
            if not errors:
                try:
                    kilos_tot = float(record["kilos_totales"])
                    kilos_exp = float(record.get("kilos_exportables", 0.0))
                    brix = float(record["grados_brix"])
                    calibre = float(record["calibre_promedio"])

                    if not (self.BRIX_RANGE[0] <= brix <= self.BRIX_RANGE[1]):
                        errors.append(f"Validez violada: grados_brix ({brix}) fuera de rango {self.BRIX_RANGE}")
                    if not (self.CALIBRE_RANGE[0] <= calibre <= self.CALIBRE_RANGE[1]):
                        errors.append(f"Validez violada: calibre_promedio ({calibre}) fuera de rango {self.CALIBRE_RANGE}")

                    if record.get("ph_suelo") is not None:
                        ph = float(record["ph_suelo"])
                        if not (self.PH_RANGE[0] <= ph <= self.PH_RANGE[1]):
                            errors.append(f"Validez violada: ph_suelo ({ph}) fuera de rango agronómico {self.PH_RANGE}")

                    if not errors:
                        validity_passes += 1

                    if kilos_exp > kilos_tot:
                        errors.append(f"Consistencia violada: kilos_exportables ({kilos_exp}) > kilos_totales ({kilos_tot})")
                    else:
                        consistency_passes += 1

                except (ValueError, TypeError) as exc:
                    errors.append(f"Validez de Tipos violada: Conversión numérica falló: {str(exc)}")

            if errors:
                quarantine_entry = {
                    "record_index": idx,
                    "raw_payload": record,
                    "errors": errors,
                    "quarantined_at": datetime.utcnow().isoformat(),
                }
                quarantined_records.append(quarantine_entry)
                validation_errors.append({"record_index": idx, "errors": errors})
            else:
                try:
                    entity = HarvestBatch.from_dict(record)
                    valid_batches.append(entity)
                except InvariantViolationException as inv_exc:
                    quarantined_records.append({
                        "record_index": idx,
                        "raw_payload": record,
                        "errors": [f"Invariante de Dominio violada: {inv_exc.message}"],
                        "quarantined_at": datetime.utcnow().isoformat(),
                    })

        report = DataQualityReport(
            total_records=total_records,
            valid_records=len(valid_batches),
            quarantined_records=len(quarantined_records),
            completeness_rate=round(completeness_passes / total_records, 4),
            validity_rate=round(validity_passes / total_records, 4),
            consistency_rate=round(consistency_passes / total_records, 4),
            validation_errors=validation_errors,
        )
        return valid_batches, quarantined_records, report

    def validate_cotizaciones_stream(
        self, raw_records: List[Dict[str, Any]]
    ) -> Tuple[List[CotizacionMayorista], List[Dict[str, Any]], DataQualityReport]:
        """Validates wholesale price quotations (DANE SIPSA_P) against DAMA-BOK contracts."""
        valid_items: List[CotizacionMayorista] = []
        quarantined: List[Dict[str, Any]] = []
        validation_errors: List[Dict[str, Any]] = []
        seen_natural_keys: Set[str] = set()

        total = len(raw_records)
        if total == 0:
            return [], [], self._empty_report()

        completeness_passes = 0
        validity_passes = 0
        consistency_passes = 0

        for idx, rec in enumerate(raw_records, start=1):
            errors: List[str] = []

            # 1. Completitud
            missing = [f for f in self.SIPSA_P_REQUIRED_FIELDS if rec.get(f) is None or str(rec.get(f)).strip() == ""]
            if missing:
                errors.append(f"Completitud: Campos obligatorios faltantes: {missing}")
            else:
                completeness_passes += 1

            # 2. Unicidad natural
            natural_key = f"{rec.get('fecha')}_{rec.get('mercado_id')}_{rec.get('codigo_cpc')}_{rec.get('variedad', '')}"
            if natural_key in seen_natural_keys:
                errors.append(f"Unicidad: Registro duplicado para clave natural '{natural_key}'")
            else:
                seen_natural_keys.add(natural_key)

            # 3. Validez y Consistencia de Precios
            if not errors:
                try:
                    p_min = float(rec["precio_min_kg"])
                    p_prom = float(rec["precio_prom_kg"])
                    p_max = float(rec["precio_max_kg"])
                    vol = float(rec.get("volumen_transado_kg", 0.0))

                    if p_min <= 0 or p_prom <= 0 or p_max <= 0:
                        errors.append(f"Validez: Precios deben ser positivos. Recibido: min={p_min}, prom={p_prom}, max={p_max}")
                    if vol < 0:
                        errors.append(f"Validez: Volumen transado no puede ser negativo: {vol}")

                    if not errors:
                        validity_passes += 1

                    # Consistencia: P_min <= P_prom <= P_max
                    if not (p_min <= p_prom <= p_max):
                        errors.append(
                            f"Consistencia: Violación de jerarquía de precios ({p_min} <= {p_prom} <= {p_max} es falso)"
                        )
                    else:
                        consistency_passes += 1

                except (ValueError, TypeError) as exc:
                    errors.append(f"Validez de tipo numérico falló: {str(exc)}")

            if errors:
                quarantined.append({
                    "record_index": idx,
                    "dataset": "SIPSA_P",
                    "raw_payload": rec,
                    "errors": errors,
                    "quarantined_at": datetime.utcnow().isoformat(),
                })
                validation_errors.append({"record_index": idx, "errors": errors})
            else:
                # Construcción segura de la entidad
                try:
                    raw_f = rec["fecha"]
                    fecha_obj = date.fromisoformat(str(raw_f)[:10]) if not isinstance(raw_f, date) else raw_f

                    prod = CpcProductCode(
                        codigo_cpc=str(rec["codigo_cpc"]),
                        nombre_producto=str(rec.get("nombre_producto", "Producto Agrícola")),
                        grupo_cpc=str(rec.get("grupo_cpc", "Tubérculos / Hortalizas")),
                        variedad=str(rec.get("variedad")) if rec.get("variedad") else None,
                    )

                    mpio_origen = None
                    if rec.get("codigo_mpio_origen"):
                        mpio_origen = DivipolaCode(
                            codigo_mpio=str(rec["codigo_mpio_origen"]),
                            nombre_mpio=str(rec.get("nombre_mpio_origen", "Municipio")),
                            codigo_depto=str(rec.get("codigo_depto_origen", str(rec["codigo_mpio_origen"])[:2])),
                            nombre_depto=str(rec.get("nombre_depto_origen", "Departamento")),
                        )

                    cotizacion = CotizacionMayorista(
                        id_cotizacion=str(rec.get("id_cotizacion", f"cot_{natural_key}_{idx}")),
                        fecha=fecha_obj,
                        mercado_id=str(rec["mercado_id"]),
                        producto=prod,
                        precio_min_kg=float(rec["precio_min_kg"]),
                        precio_max_kg=float(rec["precio_max_kg"]),
                        precio_prom_kg=float(rec["precio_prom_kg"]),
                        volumen_transado_kg=float(rec.get("volumen_transado_kg", 0.0)),
                        municipio_origen=mpio_origen,
                    )
                    valid_items.append(cotizacion)
                except Exception as exc:
                    quarantined.append({
                        "record_index": idx,
                        "dataset": "SIPSA_P",
                        "raw_payload": rec,
                        "errors": [f"Error de dominio: {str(exc)}"],
                        "quarantined_at": datetime.utcnow().isoformat(),
                    })

        report = DataQualityReport(
            total_records=total,
            valid_records=len(valid_items),
            quarantined_records=len(quarantined),
            completeness_rate=round(completeness_passes / total, 4),
            validity_rate=round(validity_passes / total, 4),
            consistency_rate=round(consistency_passes / total, 4),
            validation_errors=validation_errors,
        )
        return valid_items, quarantined, report

    def validate_abastecimiento_stream(
        self, raw_records: List[Dict[str, Any]]
    ) -> Tuple[List[RegistroAbastecimiento], List[Dict[str, Any]], DataQualityReport]:
        """Validates food supply records (DANE SIPSA_A) against DAMA-BOK contracts."""
        valid_items: List[RegistroAbastecimiento] = []
        quarantined: List[Dict[str, Any]] = []
        validation_errors: List[Dict[str, Any]] = []
        seen_keys: Set[str] = set()

        total = len(raw_records)
        if total == 0:
            return [], [], self._empty_report()

        completeness_passes = 0
        validity_passes = 0
        consistency_passes = 0

        for idx, rec in enumerate(raw_records, start=1):
            errors: List[str] = []

            # 1. Completitud
            missing = [f for f in self.SIPSA_A_REQUIRED_FIELDS if rec.get(f) is None or str(rec.get(f)).strip() == ""]
            if missing:
                errors.append(f"Completitud: Campos faltantes: {missing}")
            else:
                completeness_passes += 1

            # 2. Unicidad natural
            natural_key = f"{rec.get('fecha')}_{rec.get('mercado_id')}_{rec.get('codigo_cpc')}_{rec.get('codigo_mpio_origen')}"
            if natural_key in seen_keys:
                errors.append(f"Unicidad: Clave duplicada '{natural_key}'")
            else:
                seen_keys.add(natural_key)

            # 3. Validez
            if not errors:
                try:
                    vol_ton = float(rec["volumen_toneladas"])
                    vehs = int(rec.get("num_vehiculos", 1))

                    if vol_ton < 0:
                        errors.append(f"Validez: Volumen en toneladas no puede ser negativo: {vol_ton}")
                    if vehs < 0:
                        errors.append(f"Validez: Vehículos no puede ser negativo: {vehs}")

                    if not errors:
                        validity_passes += 1
                        consistency_passes += 1
                except (ValueError, TypeError) as exc:
                    errors.append(f"Validez numérica: {str(exc)}")

            if errors:
                quarantined.append({
                    "record_index": idx,
                    "dataset": "SIPSA_A",
                    "raw_payload": rec,
                    "errors": errors,
                    "quarantined_at": datetime.utcnow().isoformat(),
                })
                validation_errors.append({"record_index": idx, "errors": errors})
            else:
                try:
                    raw_f = rec["fecha"]
                    fecha_obj = date.fromisoformat(str(raw_f)[:10]) if not isinstance(raw_f, date) else raw_f

                    prod = CpcProductCode(
                        codigo_cpc=str(rec["codigo_cpc"]),
                        nombre_producto=str(rec.get("nombre_producto", "Producto")),
                        grupo_cpc=str(rec.get("grupo_cpc", "Alimentos")),
                        variedad=str(rec.get("variedad")) if rec.get("variedad") else None,
                    )
                    mpio = DivipolaCode(
                        codigo_mpio=str(rec["codigo_mpio_origen"]),
                        nombre_mpio=str(rec.get("nombre_mpio_origen", "Municipio")),
                        codigo_depto=str(rec.get("codigo_depto_origen", str(rec["codigo_mpio_origen"])[:2])),
                        nombre_depto=str(rec.get("nombre_depto_origen", "Depto")),
                    )
                    abast = RegistroAbastecimiento(
                        id_abastecimiento=str(rec.get("id_abastecimiento", f"aba_{natural_key}_{idx}")),
                        fecha=fecha_obj,
                        mercado_id=str(rec["mercado_id"]),
                        producto=prod,
                        municipio_origen=mpio,
                        volumen_toneladas=float(rec["volumen_toneladas"]),
                        num_vehiculos=int(rec.get("num_vehiculos", 1)),
                    )
                    valid_items.append(abast)
                except Exception as exc:
                    quarantined.append({
                        "record_index": idx,
                        "dataset": "SIPSA_A",
                        "raw_payload": rec,
                        "errors": [f"Error de dominio: {str(exc)}"],
                        "quarantined_at": datetime.utcnow().isoformat(),
                    })

        report = DataQualityReport(
            total_records=total,
            valid_records=len(valid_items),
            quarantined_records=len(quarantined),
            completeness_rate=round(completeness_passes / total, 4),
            validity_rate=round(validity_passes / total, 4),
            consistency_rate=round(consistency_passes / total, 4),
            validation_errors=validation_errors,
        )
        return valid_items, quarantined, report

    def validate_clima_stream(
        self, raw_records: List[Dict[str, Any]]
    ) -> Tuple[List[ObservacionClimatica], List[Dict[str, Any]], DataQualityReport]:
        """Validates climate observation records (IDEAM / NASA POWER) against DAMA-BOK."""
        valid_items: List[ObservacionClimatica] = []
        quarantined: List[Dict[str, Any]] = []
        validation_errors: List[Dict[str, Any]] = []
        seen_keys: Set[str] = set()

        total = len(raw_records)
        if total == 0:
            return [], [], self._empty_report()

        completeness_passes = 0
        validity_passes = 0
        consistency_passes = 0

        for idx, rec in enumerate(raw_records, start=1):
            errors: List[str] = []

            # 1. Completitud
            missing = [f for f in self.CLIMA_REQUIRED_FIELDS if rec.get(f) is None or str(rec.get(f)).strip() == ""]
            if missing:
                errors.append(f"Completitud: Campos meteorológicos faltantes: {missing}")
            else:
                completeness_passes += 1

            # 2. Unicidad
            key = f"{rec.get('fecha')}_{rec.get('estacion_id')}"
            if key in seen_keys:
                errors.append(f"Unicidad: Observación climática duplicada '{key}'")
            else:
                seen_keys.add(key)

            # 3. Validez y Consistencia térmica
            if not errors:
                try:
                    precip = float(rec["precipitacion_mm"])
                    if precip < 0:
                        errors.append(f"Validez: Precipitación negativa ({precip} mm)")

                    t_min = float(rec["temp_min_celsius"]) if rec.get("temp_min_celsius") is not None else None
                    t_max = float(rec["temp_max_celsius"]) if rec.get("temp_max_celsius") is not None else None
                    t_med = float(rec["temp_media_celsius"]) if rec.get("temp_media_celsius") is not None else None
                    hr = float(rec["humedad_relativa_pct"]) if rec.get("humedad_relativa_pct") is not None else None

                    if hr is not None and not (0.0 <= hr <= 100.0):
                        errors.append(f"Validez: Humedad relativa fuera de rango 0-100%: {hr}")

                    if not errors:
                        validity_passes += 1

                    if t_min is not None and t_max is not None and t_min > t_max:
                        errors.append(f"Consistencia térmica: T_min ({t_min}) > T_max ({t_max})")
                    else:
                        consistency_passes += 1

                except (ValueError, TypeError) as exc:
                    errors.append(f"Validez de tipos meteorológicos: {str(exc)}")

            if errors:
                quarantined.append({
                    "record_index": idx,
                    "dataset": "IDEAM_CLIMA",
                    "raw_payload": rec,
                    "errors": errors,
                    "quarantined_at": datetime.utcnow().isoformat(),
                })
                validation_errors.append({"record_index": idx, "errors": errors})
            else:
                try:
                    raw_f = rec["fecha"]
                    fecha_obj = date.fromisoformat(str(raw_f)[:10]) if not isinstance(raw_f, date) else raw_f

                    mpio = DivipolaCode(
                        codigo_mpio=str(rec["codigo_mpio"]),
                        nombre_mpio=str(rec.get("nombre_mpio", "Municipio")),
                        codigo_depto=str(rec.get("codigo_depto", str(rec["codigo_mpio"])[:2])),
                        nombre_depto=str(rec.get("nombre_depto", "Depto")),
                    )
                    clima = ObservacionClimatica(
                        id_observacion=str(rec.get("id_observacion", f"cli_{key}_{idx}")),
                        estacion_id=str(rec["estacion_id"]),
                        fecha=fecha_obj,
                        municipio=mpio,
                        precipitacion_mm=float(rec["precipitacion_mm"]),
                        temp_max_celsius=float(rec["temp_max_celsius"]) if rec.get("temp_max_celsius") is not None else None,
                        temp_min_celsius=float(rec["temp_min_celsius"]) if rec.get("temp_min_celsius") is not None else None,
                        temp_media_celsius=float(rec["temp_media_celsius"]) if rec.get("temp_media_celsius") is not None else None,
                        humedad_relativa_pct=float(rec["humedad_relativa_pct"]) if rec.get("humedad_relativa_pct") is not None else None,
                        radiacion_solar_mj=float(rec["radiacion_solar_mj"]) if rec.get("radiacion_solar_mj") is not None else None,
                    )
                    valid_items.append(clima)
                except Exception as exc:
                    quarantined.append({
                        "record_index": idx,
                        "dataset": "IDEAM_CLIMA",
                        "raw_payload": rec,
                        "errors": [f"Error de dominio: {str(exc)}"],
                        "quarantined_at": datetime.utcnow().isoformat(),
                    })

        report = DataQualityReport(
            total_records=total,
            valid_records=len(valid_items),
            quarantined_records=len(quarantined),
            completeness_rate=round(completeness_passes / total, 4),
            validity_rate=round(validity_passes / total, 4),
            consistency_rate=round(consistency_passes / total, 4),
            validation_errors=validation_errors,
        )
        return valid_items, quarantined, report

    def _empty_report(self) -> DataQualityReport:
        return DataQualityReport(
            total_records=0,
            valid_records=0,
            quarantined_records=0,
            completeness_rate=1.0,
            validity_rate=1.0,
            consistency_rate=1.0,
            validation_errors=[],
        )
