"""Test fixtures and mock datasets for Agrostat DS test suite.

Normative: SWEBOK Chapter 5 (Software Testing) / Clean Code.
"""

from datetime import date, timedelta
from typing import Any, Dict, List


def get_sample_valid_batch(
    batch_id: str = "BATCH-TEST-001",
    lote_id: str = "LOTE-AGRO-01",
    kilos_totales: float = 12000.0,
    kilos_exportables: float = 10500.0,
    calibre: float = 48.0,
    brix: float = 14.5,
) -> Dict[str, Any]:
    """Returns a single valid batch dictionary matching DAMA-BOK contracts."""
    return {
        "batch_id": batch_id,
        "lote_id": lote_id,
        "fecha_cosecha": date.today().isoformat(),
        "hectareas_lote": 10.0,
        "kilos_totales": kilos_totales,
        "kilos_exportables": kilos_exportables,
        "calibre_promedio": calibre,
        "grados_brix": brix,
        "ph_suelo": 6.4,
        "humedad_relativa": 75.0,
        "precipitacion_mm": 20.0,
        "temperatura_celsius": 23.0,
        "responsable_registro": "Ing. Test Auditor",
    }


def get_sample_dataset(count: int = 25) -> List[Dict[str, Any]]:
    """Returns a list of 25 valid harvest batches with realistic variations."""
    records = []
    base_date = date.today() - timedelta(days=count * 2)

    for i in range(count):
        d = base_date + timedelta(days=i * 2)
        records.append({
            "batch_id": f"BATCH-MOCK-{i+1:03d}",
            "lote_id": "LOTE-PALMA-NORTE",
            "fecha_cosecha": d.isoformat(),
            "hectareas_lote": 12.0,
            "kilos_totales": 12000.0 + (i * 250.0),
            "kilos_exportables": 10000.0 + (i * 200.0),
            "calibre_promedio": 45.0 + (i % 5),
            "grados_brix": 12.0 + (i % 4),
            "ph_suelo": 6.2,
            "humedad_relativa": 72.0,
            "precipitacion_mm": 18.0,
            "temperatura_celsius": 22.0,
            "responsable_registro": "Auditor QA",
        })

    return records
