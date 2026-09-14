"""Driving Adapter: Command Line Interface (CLI).

Provides full terminal command interface for executing the data science pipeline
and Colombian agricultural market analytics.
Normative: SWEBOK Chapter 2 / Hexagonal Architecture Driving Adapter.
"""

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import random
import sys
from typing import Any, Dict, List

from agrostat_app.container import create_container


def generate_synthetic_harvest_data(n_records: int = 40) -> List[Dict[str, Any]]:
    """Generates a realistic agronomic dataset conforming to AgroStats DAMA-BOK contracts."""
    records = []
    base_date = date.today() - timedelta(days=n_records * 3)
    lotes = ["LOTE-PALMA-01", "LOTE-AGUACATE-02", "LOTE-CAFE-03", "LOTE-CITRICOS-04"]

    for i in range(n_records):
        lote = random.choice(lotes)
        current_date = base_date + timedelta(days=i * 3)
        hectareas = round(random.uniform(5.0, 25.0), 1)

        base_yield_kg_ha = random.uniform(8000.0, 15000.0)
        kilos_totales = round(base_yield_kg_ha * hectareas, 1)

        export_rate = random.uniform(0.72, 0.94)
        kilos_exportables = round(kilos_totales * export_rate, 1)

        calibre = round(random.uniform(32.0, 68.0), 1)
        brix = round(random.uniform(8.5, 18.0), 1)
        ph = round(random.uniform(5.2, 7.1), 2)
        humedad = round(random.uniform(60.0, 85.0), 1)
        precipitacion = round(random.uniform(5.0, 45.0), 1)
        temperatura = round(random.uniform(18.0, 28.0), 1)

        if i % 18 == 0 and i > 0:
            brix = 45.0  # Fuera de rango para probar DLQ

        record = {
            "batch_id": f"BATCH-2026-{i+1:04d}",
            "lote_id": lote,
            "fecha_cosecha": current_date.isoformat(),
            "hectareas_lote": hectareas,
            "kilos_totales": kilos_totales,
            "kilos_exportables": kilos_exportables,
            "calibre_promedio": calibre,
            "grados_brix": brix,
            "ph_suelo": ph,
            "humedad_relativa": humedad,
            "precipitacion_mm": precipitacion,
            "temperatura_celsius": temperatura,
            "responsable_registro": "Ing. Agrónomo Campo",
        }
        records.append(record)

    return records


def main() -> None:
    """Main CLI entry point."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="AgroStat & Tech Co. - Colombian Agricultural Market & Data Science Pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # 1. Pipeline End-to-End Local
    p_pipe = subparsers.add_parser("pipeline", help="Ejecuta el pipeline de cosecha completo de principio a fin")
    p_pipe.add_argument("--samples", type=int, default=35, help="Número de registros de prueba (default: 35)")
    p_pipe.add_argument("--file", type=str, default=None, help="Ruta a archivo JSON con dataset real")

    # 2. Ingesta Local
    p_ingest = subparsers.add_parser("ingest", help="Ingesta y valida un archivo de datos de cosecha")
    p_ingest.add_argument("--file", type=str, required=True, help="Ruta a archivo JSON")
    p_ingest.add_argument("--tag", type=str, default="cli_upload", help="Etiqueta de origen")

    # 3. Ingesta Nacional de Mercado & Clima (SIPSA / IDEAM / DuckDB)
    p_mkt_ingest = subparsers.add_parser("ingest-market", help="Ingesta diaria de SIPSA Precios + IDEAM Clima a DuckDB Gold")
    p_mkt_ingest.add_argument("--date", type=str, default=None, help="Fecha en formato YYYY-MM-DD (default: hoy)")
    p_mkt_ingest.add_argument("--limit", type=int, default=100, help="Límite de registros por fuente")

    # 4. Pronóstico de Mercado
    p_mkt_fore = subparsers.add_parser("forecast-market", help="Pronóstico semanal de precios y demanda agrícola (1-12 semanas)")
    p_mkt_fore.add_argument("--cpc", type=str, default="01211", help="Código CPC del producto (default: 01211 Papa Pastusa)")
    p_mkt_fore.add_argument("--mercado", type=str, default="CORABASTOS", help="ID del mercado mayorista (default: CORABASTOS)")
    p_mkt_fore.add_argument("--weeks", type=int, default=4, help="Horizonte en semanas (1 a 12)")

    # 5. SPC de Precios de Mercado
    p_mkt_spc = subparsers.add_parser("spc-market", help="Control estadístico Shewhart 3-sigma y Nelson sobre precios de mercado")
    p_mkt_spc.add_argument("--cpc", type=str, default="01211", help="Código CPC del producto")
    p_mkt_spc.add_argument("--mercado", type=str, default="CORABASTOS", help="ID del mercado mayorista")

    # 6. Consulta SQL Directa a DuckDB DW
    p_sql = subparsers.add_parser("query-dw", help="Ejecuta consulta analítica SQL directa sobre el Data Warehouse en DuckDB")
    p_sql.add_argument("--sql", type=str, required=True, help="Consulta SQL a ejecutar")

    # 7. Balance Oferta-Demanda
    p_bal = subparsers.add_parser("balance-market", help="Consulta la vista de balance de oferta vs demanda semanal")
    p_bal.add_argument("--mercado", type=str, default=None, help="Filtrar por central de abastos")
    p_bal.add_argument("--cpc", type=str, default=None, help="Filtrar por código CPC de producto")

    # 8. Modelos y Utilidades
    subparsers.add_parser("models", help="Lista modelos registrados en el Model Registry")

    p_gen = subparsers.add_parser("generate-data", help="Genera dataset de cosecha sintético en JSON")
    p_gen.add_argument("--out", type=str, default="sample_harvest.json", help="Ruta de destino")
    p_gen.add_argument("--n", type=int, default=50, help="Cantidad de muestras")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    container = create_container()

    if args.command == "ingest-market":
        print("\n" + "=" * 70)
        print("[AGROSTAT] INGESTA NACIONAL DE MERCADO Y CLIMA (SIPSA + IDEAM)")
        print("=" * 70)
        t_date = date.fromisoformat(args.date) if args.date else date.today()
        res = container.market_ingestion_use_case.execute(target_date=t_date, record_limit=args.limit)

        print(f"Ejecución ID:          {res.execution_id}")
        print(f"Fecha:                 {res.target_date}")
        print(f"Archivos Bronze:       {len(res.bronze_paths)} almacenados")
        print(f"Cotizaciones Silver:   {res.sipsa_prices_curated} registros validados")
        print(f"Clima Silver:          {res.ideam_climate_curated} observaciones validadas")
        print(f"Cuarentena DLQ:        {res.quarantined_total} registros anómalos")
        print(f"DuckDB Gold Hechos:    Precios={res.gold_facts_updated.get('fact_precios', 0)}, "
              f"Abastecimiento={res.gold_facts_updated.get('fact_abastecimiento', 0)}, "
              f"Clima={res.gold_facts_updated.get('fact_clima', 0)}")
        print(f"Tiempo de Ejecución:   {res.duration_seconds:.3f} segundos")
        print("=" * 70 + "\n")

    elif args.command == "forecast-market":
        print("\n" + "=" * 70)
        print(f"[AGROSTAT FORECAST] PRONÓSTICO DE PRECIOS Y DEMANDA: CPC {args.cpc} EN {args.mercado}")
        print("=" * 70)
        res = container.market_forecast_use_case.execute(
            codigo_cpc=args.cpc,
            mercado_id=args.mercado,
            horizonte_semanas=args.weeks,
        )
        print(f"Producto:              CPC {res.producto_cpc}")
        print(f"Mercado Destino:       {res.mercado_id}")
        print(f"Tendencia General:     {res.tendencia_general}")
        print(f"Semanas Proyectadas:   {res.horizonte_semanas}")
        print("\nProyecciones Semanales:")
        for p in res.proyecciones:
            print(f" - Sem {p['horizonte_semanas']} ({p['fecha_proyeccion']}): "
                  f"${p['valor_proyectado']:.2f}/kg [IC 95%: ${p['intervalo_95']['inferior']:.2f} - ${p['intervalo_95']['superior']:.2f}] Tendencia: {p['tendencia']}")
        print("=" * 70 + "\n")

    elif args.command == "spc-market":
        print("\n" + "=" * 70)
        print(f"[AGROSTAT SPC] CONTROL ESTADÍSTICO DE PROCESOS: CPC {args.cpc} EN {args.mercado}")
        print("=" * 70)
        res = container.market_spc_use_case.execute(codigo_cpc=args.cpc, mercado_id=args.mercado)
        lim = res.control_limits
        print(f"En Control Estadístico:{' SÍ (Proceso Estable)' if res.is_in_statistical_control else ' NO (Anomalías detectadas)'}")
        print(f"Media Línea Central:   ${lim['center_line_mean']:.2f}/kg")
        print(f"Límite Sup (UCL 3σ):   ${lim['limits']['ucl']:.2f}/kg")
        print(f"Límite Inf (LCL 3σ):   ${lim['limits']['lcl']:.2f}/kg")
        print(f"Violaciones Nelson:    {len(res.violations_detected)}")
        for v in res.violations_detected:
            print(f"  * Regla {v['rule_number']} ({v['rule_name']}): {v['description']}")
        print("=" * 70 + "\n")

    elif args.command == "query-dw":
        try:
            rows = container.duckdb_repository.query_dimensional_dw(args.sql)
            print(json.dumps(rows, indent=2, ensure_ascii=False, default=str))
        except Exception as exc:
            print(f"[ERROR SQL] {str(exc)}", file=sys.stderr)

    elif args.command == "balance-market":
        rows = container.duckdb_repository.get_market_balance_view(
            mercado_id=args.mercado, codigo_cpc=args.cpc
        )
        print(json.dumps(rows, indent=2, ensure_ascii=False, default=str))

    elif args.command == "pipeline":
        print("\n" + "=" * 70)
        print("[AGROSTAT] AGRO STAT & TECH CO. - PIPELINE HEXAGONAL DE COSECHA")
        print("=" * 70)

        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                dataset = json.load(f)
        else:
            print(f">> Generando dataset agroindustrial sintético con {args.samples} lotes...")
            dataset = generate_synthetic_harvest_data(args.samples)

        sample_for_infer = dataset[0].copy()
        sample_for_infer["batch_id"] = "BATCH-INFER-PROSPECT"

        summary = container.pipeline_use_case.run_pipeline(
            raw_dataset=dataset,
            source_tag="cli_e2e_run",
            sample_batch_for_inference=sample_for_infer,
        )

        print("\n" + "-" * 70)
        print("[METRICAS] RESUMEN EJECUTIVO DE EJECUCIÓN (END-TO-END)")
        print("-" * 70)
        print(f"Run ID:            {summary.run_id}")
        print(f"Estado:            {summary.status}")
        print(f"Tiempo Total:      {summary.execution_duration_sec:.3f} segundos")
        print(f"Ingesta Recibida:  {summary.ingestion.total_received} registros")
        print(f"Válidos (Silver):  {summary.ingestion.valid_count}")
        print(f"Cuarentena (DLQ):  {summary.ingestion.quarantined_count}")
        print("=" * 70 + "\n")

    elif args.command == "models":
        models = container.registry.list_models()
        print(json.dumps(models, indent=2, ensure_ascii=False))

    elif args.command == "generate-data":
        data = generate_synthetic_harvest_data(args.n)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ {args.n} registros generados en: {args.out}")


if __name__ == "__main__":
    main()
