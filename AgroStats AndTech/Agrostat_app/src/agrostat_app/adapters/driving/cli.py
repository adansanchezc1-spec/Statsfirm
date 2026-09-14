"""Driving Adapter: Command Line Interface (CLI).

Provides full terminal command interface for executing the data science pipeline.
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

        # Rendimiento base con variabilidad agronómica
        base_yield_kg_ha = random.uniform(8000.0, 15000.0)
        kilos_totales = round(base_yield_kg_ha * hectareas, 1)

        # Kilos exportables (70% - 95% del total)
        export_rate = random.uniform(0.72, 0.94)
        kilos_exportables = round(kilos_totales * export_rate, 1)

        calibre = round(random.uniform(32.0, 68.0), 1)
        brix = round(random.uniform(8.5, 18.0), 1)
        ph = round(random.uniform(5.2, 7.1), 2)
        humedad = round(random.uniform(60.0, 85.0), 1)
        precipitacion = round(random.uniform(5.0, 45.0), 1)
        temperatura = round(random.uniform(18.0, 28.0), 1)

        # Introducir deliberadamente un 5% de anomalías/errores para probar la DLQ
        if i % 18 == 0 and i > 0:
            brix = 45.0  # Fuera de rango para DLQ

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
        description="AgroStat & Tech Co. - Data Science & Engineering Hexagonal Pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # 1. Subcomando: pipeline (End-to-End)
    p_pipe = subparsers.add_parser("pipeline", help="Ejecuta el pipeline completo de principio a fin")
    p_pipe.add_argument("--samples", type=int, default=35, help="Número de registros de prueba (default: 35)")
    p_pipe.add_argument("--file", type=str, default=None, help="Ruta a archivo JSON con dataset real")

    # 2. Subcomando: ingest
    p_ingest = subparsers.add_parser("ingest", help="Ingesta y valida un archivo de datos crudos")
    p_ingest.add_argument("--file", type=str, required=True, help="Ruta a archivo JSON")
    p_ingest.add_argument("--tag", type=str, default="cli_upload", help="Etiqueta de origen")

    # 3. Subcomando: train
    p_train = subparsers.add_parser("train", help="Entrena modelo de regresión Yield AI")
    p_train.add_argument("--algo", type=str, default="random_forest", choices=["random_forest", "gradient_boosting"])
    p_train.add_argument("--lote", type=str, default=None, help="Filtrar por lote específico")

    # 4. Subcomando: predict
    p_pred = subparsers.add_parser("predict", help="Genera inferencia de rendimiento para un lote")
    p_pred.add_argument("--lote", type=str, required=True, help="ID del lote")
    p_pred.add_argument("--ha", type=float, default=10.0, help="Hectáreas del lote")
    p_pred.add_argument("--calibre", type=float, default=45.0, help="Calibre promedio estimado")
    p_pred.add_argument("--brix", type=float, default=12.5, help="Grados Brix estimados")

    # 5. Subcomando: spc
    p_spc = subparsers.add_parser("spc", help="Audita estabilidad bioestadística (Shewhart + Nelson)")
    p_spc.add_argument("--lote", type=str, default=None, help="ID del lote (opcional)")
    p_spc.add_argument("--metric", type=str, default="rendimiento_kg_ha", help="Métrica a auditar")

    # 6. Subcomando: models
    subparsers.add_parser("models", help="Lista modelos registrados en el Model Registry")

    # 7. Subcomando: generate-data
    p_gen = subparsers.add_parser("generate-data", help="Genera dataset sintético en JSON")
    p_gen.add_argument("--out", type=str, default="sample_harvest.json", help="Ruta de destino")
    p_gen.add_argument("--n", type=int, default=50, help="Cantidad de muestras")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    container = create_container()

    if args.command == "pipeline":
        print("\n" + "=" * 70)
        print("[AGROSTAT] AGRO STAT & TECH CO. - PIPELINE HEXAGONAL DE DATA SCIENCE")
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
        print(f"Calidad del Dato:  Completitud: {summary.ingestion.completeness_pct:.1f}% | Consistencia: {summary.ingestion.consistency_pct:.1f}%")

        if summary.training:
            print("\n[ML ENGINE] MODELO DE MACHINE LEARNING (YIELD AI):")
            print(f"Versión:           {summary.training.version}")
            print(f"Algoritmo:         {summary.training.algorithm}")
            print(f"R² Score:          {summary.training.r2_score:.4f}")
            print(f"RMSE:              {summary.training.rmse:.2f} kg/ha")
            print(f"MAPE:              {summary.training.mape:.2f}%")
            print(f"Registro:          {summary.training.registry_path}")

        if summary.spc_stability and "center_line_mean" in summary.spc_stability:
            spc = summary.spc_stability
            print("\n[SPC BIOESTADISTICA] CONTROL ESTADÍSTICO DE PROCESOS:")
            print(f"Muestras:          {spc['sample_count']}")
            print(f"Media (Línea C.):  {spc['center_line_mean']} kg/ha")
            print(f"Límite Sup (UCL):  {spc['limits']['ucl']} kg/ha")
            print(f"Límite Inf (LCL):  {spc['limits']['lcl']} kg/ha")
            print(f"Capacidad (Cpk):   {spc['capability']['cpk_index']} (Capaz: {spc['capability']['is_capable']})")
            print(f"Estable:           {'SÍ' if spc['is_in_statistical_control'] else 'NO (Anomalías detectadas)'}")
            print(f"Violaciones:       {spc['violations_count']}")

        print("=" * 70 + "\n")

    elif args.command == "ingest":
        with open(args.file, "r", encoding="utf-8") as f:
            records = json.load(f)
        res = container.ingestion_use_case.execute_ingestion(records, args.tag)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "train":
        res = container.training_use_case.train_and_register(
            lote_id=args.lote, model_algorithm=args.algo
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.command == "predict":
        payload = {
            "batch_id": "BATCH-CLI-PRED",
            "lote_id": args.lote,
            "fecha_cosecha": date.today().isoformat(),
            "hectareas_lote": args.ha,
            "kilos_totales": 1000.0,
            "kilos_exportables": 850.0,
            "calibre_promedio": args.calibre,
            "grados_brix": args.brix,
            "responsable_registro": "CLI User",
        }
        pred = container.prediction_use_case.predict_harvest_yield(payload)
        print(json.dumps(pred.to_dict(), indent=2, ensure_ascii=False))

    elif args.command == "spc":
        limits = container.spc_use_case.analyze_process_stability(
            lote_id=args.lote, metric_name=args.metric
        )
        print(json.dumps(limits.to_dict(), indent=2, ensure_ascii=False))

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
