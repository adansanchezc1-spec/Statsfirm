"""
Validador de Calidad de Datos según DAMA-DMBOK 2
6 Dimensiones: Completitud, Validez, Consistencia, Unicidad, Exactitud, Oportunidad
"""
from typing import Dict, Any, List
from datetime import datetime

class DataQualityValidator:
    REQUIRED_FIELDS = ["fecha", "codigo_cpc", "precio_min", "precio_max", "precio_promedio", "central_abasto"]

    @classmethod
    def evaluate_cotizacion_stream(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        valid_records = []
        quarantine_records = []
        seen_keys = set()

        for rec in records:
            reasons = []

            # 1. Completitud: Presencia de campos requeridos
            for field in cls.REQUIRED_FIELDS:
                if field not in rec or rec[field] is None or str(rec[field]).strip() == "":
                    reasons.append(f"Falla Completitud: Campo obligatorio '{field}' ausente o nulo.")

            # 2. Validez: Rangos de precios positivos
            try:
                p_min = float(rec.get("precio_min", 0))
                p_max = float(rec.get("precio_max", 0))
                p_prom = float(rec.get("precio_promedio", 0))

                if p_min <= 0 or p_max <= 0 or p_prom <= 0:
                    reasons.append("Falla Validez: Los precios deben ser estrictamente positivos.")
            except (ValueError, TypeError):
                reasons.append("Falla Validez: Formato numérico de precios no convertible.")
                p_min, p_max, p_prom = 0, 0, 0

            # 3. Consistencia: Jerarquía p_min <= p_prom <= p_max
            if p_min > p_max or p_prom < p_min or p_prom > p_max:
                reasons.append(f"Falla Consistencia: Inconsistencia en jerarquía de precios (min: {p_min}, prom: {p_prom}, max: {p_max}).")

            # 4. Unicidad: Duplicados por clave natural
            natural_key = f"{rec.get('fecha')}_{rec.get('codigo_cpc')}_{rec.get('central_abasto')}"
            if natural_key in seen_keys:
                reasons.append(f"Falla Unicidad: Registro duplicado para clave natural '{natural_key}'.")
            else:
                seen_keys.add(natural_key)

            if reasons:
                quarantine_records.append({
                    "record": rec,
                    "reasons": reasons,
                    "quarantined_at": datetime.utcnow().isoformat()
                })
            else:
                valid_records.append(rec)

        total = len(records)
        val_count = len(valid_records)
        completeness_rate = round((val_count / total) * 100.0, 1) if total > 0 else 100.0

        return {
            "total_evaluated": total,
            "valid_count": val_count,
            "quarantine_count": len(quarantine_records),
            "quality_rate_pct": completeness_rate,
            "valid_records": valid_records,
            "quarantine_records": quarantine_records,
            "is_production_ready": len(quarantine_records) == 0
        }
