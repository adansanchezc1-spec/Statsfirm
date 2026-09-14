"""Driven Adapter: DuckDB Medallion Lakehouse Repository.

Implements LakehouseRepositoryPort.
Persists Bronze (raw inmutable with SHA-256), Silver (curated entities),
and Gold (Star Schema dimensional warehouse in DuckDB).
Normative: SWEBOK Chapter 2 / Medallion Architecture / Clean Code.
"""

from datetime import date, datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

import pandas as pd

from agrostat_app.domain.entities import (
    CotizacionMayorista,
    ObservacionClimatica,
    RegistroAbastecimiento,
)
from agrostat_app.domain.exceptions import RepositoryException
from agrostat_app.ports.out_lakehouse_port import LakehouseRepositoryPort


class DuckDBLakehouseRepository(LakehouseRepositoryPort):
    """Concrete adapter connecting local filesystem lakehouse and DuckDB columnar engine."""

    def __init__(
        self,
        base_data_dir: Path,
        sql_schema_path: Optional[Path] = None,
        seeds_path: Optional[Path] = None,
    ) -> None:
        self._base_dir = Path(base_data_dir)
        self._bronze_dir = self._base_dir / "bronze"
        self._silver_dir = self._base_dir / "silver"
        self._gold_dir = self._base_dir / "gold"
        self._db_path = self._gold_dir / "agro_dw.duckdb"

        self._schema_path = sql_schema_path
        self._seeds_path = seeds_path

        for d in [self._bronze_dir, self._silver_dir, self._gold_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self._init_database()

    def _init_database(self) -> None:
        """Bootstraps DuckDB schema and seeds if not present."""
        if not HAS_DUCKDB:
            return

        con = duckdb.connect(str(self._db_path))
        try:
            existing = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
            if "dim_producto" not in existing and self._schema_path and self._schema_path.exists():
                ddl = self._schema_path.read_text(encoding="utf-8")
                con.execute(ddl)

            existing = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
            if "dim_producto" in existing:
                count_prod = con.execute("SELECT COUNT(*) FROM dim_producto").fetchone()[0]
                if count_prod == 0 and self._seeds_path and self._seeds_path.exists():
                    seeds = self._seeds_path.read_text(encoding="utf-8")
                    con.execute(seeds)
        finally:
            con.close()

    def save_bronze_records(self, raw_records: List[Dict[str, Any]], source_tag: str) -> str:
        """Stores immutable raw records in Bronze layer with SHA-256 integrity hash."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        content_bytes = json.dumps(raw_records, ensure_ascii=False, default=str).encode("utf-8")
        sha256_hash = hashlib.sha256(content_bytes).hexdigest()

        filename = f"raw_{source_tag}_{timestamp}_{sha256_hash[:8]}.json"
        target_path = self._bronze_dir / filename

        try:
            payload = {
                "metadata": {
                    "source_tag": source_tag,
                    "record_count": len(raw_records),
                    "sha256": sha256_hash,
                    "ingested_at": datetime.utcnow().isoformat(),
                },
                "records": raw_records,
            }
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False, default=str)
            return str(target_path)
        except Exception as exc:
            raise RepositoryException(f"Error al escribir en Capa Bronze: {str(exc)}")

    def save_cotizaciones_silver(self, cotizaciones: List[CotizacionMayorista]) -> int:
        """Persists validated wholesale price quotations into Silver layer."""
        if not cotizaciones:
            return 0
        records = [c.to_dict() for c in cotizaciones]
        silver_json = self._silver_dir / "cotizaciones_mayoristas.json"
        silver_parquet = self._silver_dir / "cotizaciones_mayoristas.parquet"

        existing = []
        if silver_json.exists():
            try:
                with open(silver_json, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        combined_map = {r["id_cotizacion"]: r for r in existing}
        for r in records:
            combined_map[r["id_cotizacion"]] = r
        merged = list(combined_map.values())

        with open(silver_json, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False, default=str)

        try:
            flat_records = []
            for r in merged:
                flat_records.append({
                    "id_cotizacion": r["id_cotizacion"],
                    "fecha": r["fecha"],
                    "mercado_id": r["mercado_id"],
                    "codigo_cpc": r["producto_cpc"]["codigo_cpc"],
                    "nombre_producto": r["producto_cpc"]["nombre_producto"],
                    "variedad": r["producto_cpc"].get("variedad"),
                    "codigo_mpio_origen": r["municipio_origen"]["codigo_mpio"] if r.get("municipio_origen") else None,
                    "nombre_mpio_origen": r["municipio_origen"]["nombre_mpio"] if r.get("municipio_origen") else None,
                    "codigo_depto_origen": r["municipio_origen"]["codigo_depto"] if r.get("municipio_origen") else None,
                    "nombre_depto_origen": r["municipio_origen"]["nombre_depto"] if r.get("municipio_origen") else None,
                    "precio_min_kg": r["precio_min_kg"],
                    "precio_max_kg": r["precio_max_kg"],
                    "precio_prom_kg": r["precio_prom_kg"],
                    "volumen_transado_kg": r["volumen_transado_kg"],
                })
            df = pd.DataFrame(flat_records)
            df.to_parquet(silver_parquet, index=False)
        except Exception:
            pass

        return len(cotizaciones)

    def save_abastecimiento_silver(self, abastecimientos: List[RegistroAbastecimiento]) -> int:
        """Persists validated food supply records into Silver layer."""
        if not abastecimientos:
            return 0
        records = [a.to_dict() for a in abastecimientos]
        silver_json = self._silver_dir / "abastecimiento_alimentos.json"
        silver_parquet = self._silver_dir / "abastecimiento_alimentos.parquet"

        existing = []
        if silver_json.exists():
            try:
                with open(silver_json, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        combined_map = {r["id_abastecimiento"]: r for r in existing}
        for r in records:
            combined_map[r["id_abastecimiento"]] = r
        merged = list(combined_map.values())

        with open(silver_json, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False, default=str)

        try:
            flat_records = []
            for r in merged:
                flat_records.append({
                    "id_abastecimiento": r["id_abastecimiento"],
                    "fecha": r["fecha"],
                    "mercado_id": r["mercado_id"],
                    "codigo_cpc": r["producto_cpc"]["codigo_cpc"],
                    "codigo_mpio_origen": r["municipio_origen"]["codigo_mpio"],
                    "nombre_mpio_origen": r["municipio_origen"]["nombre_mpio"],
                    "volumen_toneladas": r["volumen_toneladas"],
                    "volumen_kg": r["volumen_kg"],
                    "num_vehiculos": r["num_vehiculos"],
                })
            df = pd.DataFrame(flat_records)
            df.to_parquet(silver_parquet, index=False)
        except Exception:
            pass

        return len(abastecimientos)

    def save_clima_silver(self, observaciones: List[ObservacionClimatica]) -> int:
        """Persists validated meteorological observations into Silver layer."""
        if not observaciones:
            return 0
        records = [o.to_dict() for o in observaciones]
        silver_json = self._silver_dir / "observaciones_clima.json"
        silver_parquet = self._silver_dir / "observaciones_clima.parquet"

        existing = []
        if silver_json.exists():
            try:
                with open(silver_json, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        combined_map = {r["id_observacion"]: r for r in existing}
        for r in records:
            combined_map[r["id_observacion"]] = r
        merged = list(combined_map.values())

        with open(silver_json, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False, default=str)

        try:
            flat_records = []
            for r in merged:
                flat_records.append({
                    "id_observacion": r["id_observacion"],
                    "estacion_id": r["estacion_id"],
                    "fecha": r["fecha"],
                    "codigo_mpio": r["municipio"]["codigo_mpio"],
                    "precipitacion_mm": r["precipitacion_mm"],
                    "temp_max_celsius": r.get("temp_max_celsius"),
                    "temp_min_celsius": r.get("temp_min_celsius"),
                    "temp_media_celsius": r.get("temp_media_celsius"),
                    "humedad_relativa_pct": r.get("humedad_relativa_pct"),
                    "radiacion_solar_mj": r.get("radiacion_solar_mj"),
                })
            df = pd.DataFrame(flat_records)
            df.to_parquet(silver_parquet, index=False)
        except Exception:
            pass

        return len(observaciones)

    def upsert_gold_facts(self) -> Dict[str, int]:
        """Loads and updates dimensional Gold fact tables in DuckDB from Silver datasets."""
        if not HAS_DUCKDB:
            return {"fact_precios": 0, "fact_abastecimiento": 0, "fact_clima": 0}

        counts = {"fact_precios": 0, "fact_abastecimiento": 0, "fact_clima": 0}
        self._init_database()
        con = duckdb.connect(str(self._db_path))

        try:
            # 1. Cargar Precios SIPSA en fact_precios_sipsa
            silver_p_parquet = self._silver_dir / "cotizaciones_mayoristas.parquet"
            if silver_p_parquet.exists():
                pq_p = str(silver_p_parquet).replace('\\', '/')
                # Asegurar dim_tiempo
                con.execute(f"""
                INSERT OR IGNORE INTO dim_tiempo (fecha_key, fecha_completa, anio, mes, nombre_mes, dia_mes, dia_semana, nombre_dia, semana_anio, trimestre, semestre)
                SELECT DISTINCT 
                    CAST(strftime(CAST(fecha AS DATE), '%Y%m%d') AS INTEGER) as fecha_key,
                    CAST(fecha AS DATE) as fecha_completa,
                    EXTRACT(YEAR FROM CAST(fecha AS DATE)) as anio,
                    EXTRACT(MONTH FROM CAST(fecha AS DATE)) as mes,
                    strftime(CAST(fecha AS DATE), '%B') as nombre_mes,
                    EXTRACT(DAY FROM CAST(fecha AS DATE)) as dia_mes,
                    EXTRACT(ISODOW FROM CAST(fecha AS DATE)) as dia_semana,
                    strftime(CAST(fecha AS DATE), '%A') as nombre_dia,
                    CAST(strftime(CAST(fecha AS DATE), '%W') AS INTEGER) as semana_anio,
                    EXTRACT(QUARTER FROM CAST(fecha AS DATE)) as trimestre,
                    CASE WHEN EXTRACT(MONTH FROM CAST(fecha AS DATE)) <= 6 THEN 1 ELSE 2 END as semestre
                FROM read_parquet('{pq_p}')
                """)

                # Asegurar dim_geografia
                con.execute(f"""
                INSERT OR IGNORE INTO dim_geografia (divipola_codigo, departamento_codigo, departamento_nombre, municipio_nombre, region_natural)
                SELECT DISTINCT 
                    codigo_mpio_origen as divipola_codigo,
                    SUBSTR(codigo_mpio_origen, 1, 2) as departamento_codigo,
                    COALESCE(nombre_depto_origen, 'Cundinamarca') as departamento_nombre,
                    COALESCE(nombre_mpio_origen, 'Municipio Origen') as municipio_nombre,
                    'Andina' as region_natural
                FROM read_parquet('{pq_p}')
                WHERE codigo_mpio_origen IS NOT NULL
                """)

                sql_precios = f"""
                INSERT OR REPLACE INTO fact_precios_sipsa (
                    precio_id, fecha_key, producto_cpc_codigo, mercado_id,
                    precio_minimo_kg, precio_medio_kg, precio_maximo_kg,
                    fuente_boletin
                )
                SELECT 
                    ROW_NUMBER() OVER () as precio_id,
                    CAST(strftime(CAST(fecha AS DATE), '%Y%m%d') AS INTEGER) as fecha_key,
                    codigo_cpc as producto_cpc_codigo,
                    mercado_id,
                    precio_min_kg as precio_minimo_kg,
                    precio_prom_kg as precio_medio_kg,
                    precio_max_kg as precio_maximo_kg,
                    'DANE_SIPSA_P' as fuente_boletin
                FROM read_parquet('{pq_p}')
                """
                con.execute(sql_precios)
                counts["fact_precios"] = con.execute("SELECT COUNT(*) FROM fact_precios_sipsa").fetchone()[0]

            # 2. Cargar Abastecimiento en fact_abastecimiento_sipsa
            silver_a_parquet = self._silver_dir / "abastecimiento_alimentos.parquet"
            if silver_a_parquet.exists():
                pq_a = str(silver_a_parquet).replace('\\', '/')
                sql_abast = f"""
                INSERT OR REPLACE INTO fact_abastecimiento_sipsa (
                    abastecimiento_id, fecha_key, producto_cpc_codigo, mercado_destino_id,
                    municipio_origen_divipola, volumen_toneladas, volumen_kilos
                )
                SELECT 
                    ROW_NUMBER() OVER () as abastecimiento_id,
                    CAST(strftime(CAST(fecha AS DATE), '%Y%m%d') AS INTEGER) as fecha_key,
                    codigo_cpc as producto_cpc_codigo,
                    mercado_id as mercado_destino_id,
                    codigo_mpio_origen as municipio_origen_divipola,
                    volumen_toneladas,
                    volumen_kg as volumen_kilos
                FROM read_parquet('{pq_a}')
                """
                con.execute(sql_abast)
                counts["fact_abastecimiento"] = con.execute("SELECT COUNT(*) FROM fact_abastecimiento_sipsa").fetchone()[0]

            # 3. Cargar Clima en fact_clima_diario
            silver_c_parquet = self._silver_dir / "observaciones_clima.parquet"
            if silver_c_parquet.exists():
                pq_c = str(silver_c_parquet).replace('\\', '/')
                con.execute(f"""
                INSERT OR IGNORE INTO dim_estacion_clima (estacion_codigo, nombre_estacion, divipola_municipio, tipo_estacion)
                SELECT DISTINCT 
                    estacion_id as estacion_codigo,
                    CONCAT('Estacion ', estacion_id) as nombre_estacion,
                    codigo_mpio as divipola_municipio,
                    'Climatológica' as tipo_estacion
                FROM read_parquet('{pq_c}')
                """)

                sql_clima = f"""
                INSERT OR REPLACE INTO fact_clima_diario (
                    clima_id, fecha_key, estacion_codigo, municipio_id,
                    precipitacion_mm, temperatura_max_celsius, temperatura_min_celsius,
                    temperatura_media_celsius, humedad_relativa_pct, radiacion_solar_mj_m2
                )
                SELECT 
                    ROW_NUMBER() OVER () as clima_id,
                    CAST(strftime(CAST(fecha AS DATE), '%Y%m%d') AS INTEGER) as fecha_key,
                    estacion_id as estacion_codigo,
                    codigo_mpio as municipio_id,
                    precipitacion_mm,
                    temp_max_celsius,
                    temp_min_celsius,
                    temp_media_celsius,
                    humedad_relativa_pct,
                    radiacion_solar_mj as radiacion_solar_mj_m2
                FROM read_parquet('{pq_c}')
                """
                con.execute(sql_clima)
                counts["fact_clima"] = con.execute("SELECT COUNT(*) FROM fact_clima_diario").fetchone()[0]

        except Exception as exc:
            raise RepositoryException(f"Error al cargar Capa Gold en DuckDB: {str(exc)}")
        finally:
            con.close()

        return counts

    def query_dimensional_dw(
        self, sql_query: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes vectorized SQL query on DuckDB."""
        if not HAS_DUCKDB:
            return []

        con = duckdb.connect(str(self._db_path), read_only=True)
        try:
            rel = con.execute(sql_query)
            cols = [desc[0] for desc in rel.description]
            rows = rel.fetchall()
            return [dict(zip(cols, row)) for row in rows]
        except Exception as exc:
            raise RepositoryException(f"Error ejecutando consulta SQL analítica: {str(exc)}")
        finally:
            con.close()

    def get_historical_prices(
        self, codigo_cpc: str, mercado_id: str, limit_weeks: int = 12
    ) -> List[Dict[str, Any]]:
        """Retrieves aggregated historical prices for statistical forecasting."""
        query = f"""
        SELECT 
            p.fecha_key,
            p.precio_medio_kg as precio_promedio_kg,
            p.precio_minimo_kg,
            p.precio_maximo_kg
        FROM fact_precios_sipsa p
        WHERE p.producto_cpc_codigo = '{codigo_cpc}' AND p.mercado_id = '{mercado_id}'
        ORDER BY p.fecha_key ASC
        LIMIT {limit_weeks * 7}
        """
        return self.query_dimensional_dw(query)

    def get_market_balance_view(
        self, mercado_id: Optional[str] = None, codigo_cpc: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries the market balance analytical view."""
        where_clauses = []
        if mercado_id:
            where_clauses.append(f"mercado_id = '{mercado_id}'")
        if codigo_cpc:
            where_clauses.append(f"producto_cpc_codigo = '{codigo_cpc}'")

        clause_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        query = f"""
        SELECT *
        FROM vw_balance_mercado_diario
        {clause_str}
        ORDER BY anio DESC, semana_anio DESC
        LIMIT 50
        """
        return self.query_dimensional_dw(query)
