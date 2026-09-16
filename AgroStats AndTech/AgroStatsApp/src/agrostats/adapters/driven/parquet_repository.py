"""Driven Adapter: Medallion Lakehouse Repository.

Implements HarvestRepositoryPort.
Persists Bronze (Raw inmutable), Silver (Curated entities), and Gold (Feature marts).
Supports Parquet and JSON storage for resilience.
Normative: Medallion Architecture / Dependency Inversion Principle.
"""

from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from agrostat_app.domain.entities import HarvestBatch
from agrostat_app.domain.exceptions import RepositoryException
from agrostat_app.ports.out_repository_port import HarvestRepositoryPort


class ParquetLakehouseRepository(HarvestRepositoryPort):
    """Adapter storing lakehouse layers in local file system."""

    def __init__(self, base_data_dir: Path) -> None:
        self._base_dir = Path(base_data_dir)
        self._bronze_dir = self._base_dir / "bronze"
        self._silver_dir = self._base_dir / "silver"
        self._gold_dir = self._base_dir / "gold"

        self._bronze_ingestion_dir = self._bronze_dir / "ingestion"
        self._bronze_limpieza_dir = self._bronze_dir / "limpieza"
        self._silver_integracion_dir = self._silver_dir / "integracion"
        self._silver_modelado_dir = self._silver_dir / "modelado"
        self._gold_resultados_dir = self._gold_dir / "resultados_modelos"

        self._silver_file_parquet = self._silver_dir / "harvest_batches.parquet"
        self._silver_file_json = self._silver_dir / "harvest_batches.json"

        for d in [
            self._bronze_dir, self._silver_dir, self._gold_dir,
            self._bronze_ingestion_dir, self._bronze_limpieza_dir,
            self._silver_integracion_dir, self._silver_modelado_dir,
            self._gold_resultados_dir
        ]:
            d.mkdir(parents=True, exist_ok=True)

    def save_bronze_records(self, raw_records: List[Dict[str, Any]], source_tag: str) -> str:
        """Saves immutable raw payload into Bronze layer (ingestion subfolder and root)."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"raw_{source_tag}_{timestamp}.json"
        target_path = self._bronze_dir / filename
        target_ingestion_path = self._bronze_ingestion_dir / filename

        try:
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(raw_records, f, indent=2, ensure_ascii=False)
            with open(target_ingestion_path, "w", encoding="utf-8") as f:
                json.dump(raw_records, f, indent=2, ensure_ascii=False)
            return str(target_path)
        except Exception as exc:
            raise RepositoryException(f"Error al escribir en Capa Bronze: {str(exc)}")

    def save_silver_batches(self, batches: List[HarvestBatch]) -> int:
        """Appends or overwrites verified entity batches into Silver layer."""
        if not batches:
            return 0

        existing_batches = self.get_silver_batches()
        batch_map = {b.batch_id: b for b in existing_batches}

        # Actualiza o agrega nuevos lotes
        for b in batches:
            batch_map[b.batch_id] = b

        merged_list = list(batch_map.values())
        records = [b.to_dict() for b in merged_list]

        # Guardar en formato JSON auditado en silver raíz y silver/integracion
        with open(self._silver_file_json, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        with open(self._silver_integracion_dir / "harvest_batches.json", "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        # Guardar en formato Parquet
        try:
            df = pd.DataFrame(records)
            df.to_parquet(self._silver_file_parquet, index=False)
            df.to_parquet(self._silver_integracion_dir / "harvest_batches.parquet", index=False)
        except Exception:
            # Fallback seguro si pyarrow/fastparquet tiene problemas de compatibilidad
            pass

        return len(batches)

    def get_silver_batches(self, lote_id: Optional[str] = None) -> List[HarvestBatch]:
        """Loads entities from Silver layer, optionally filtering by lote_id."""
        records: List[Dict[str, Any]] = []

        if self._silver_file_parquet.exists():
            try:
                df = pd.read_parquet(self._silver_file_parquet)
                records = df.to_dict(orient="records")
            except Exception:
                records = []

        if not records and self._silver_file_json.exists():
            try:
                with open(self._silver_file_json, "r", encoding="utf-8") as f:
                    records = json.load(f)
            except Exception:
                records = []

        batches = []
        for r in records:
            if lote_id and str(r.get("lote_id")) != str(lote_id):
                continue
            batches.append(HarvestBatch.from_dict(r))

        # Ordenar cronológicamente por fecha de cosecha
        batches.sort(key=lambda b: b.fecha_cosecha)
        return batches

    def save_gold_features(self, feature_rows: List[Dict[str, Any]], table_name: str) -> str:
        """Stores analytical features in Gold layer."""
        json_path = self._gold_dir / f"{table_name}.json"
        parquet_path = self._gold_dir / f"{table_name}.parquet"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(feature_rows, f, indent=2, ensure_ascii=False)

        try:
            df = pd.DataFrame(feature_rows)
            df.to_parquet(parquet_path, index=False)
            return str(parquet_path)
        except Exception:
            return str(json_path)
