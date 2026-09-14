"""Driving Adapter: REST API Server.

Provides HTTP REST endpoints for the data science pipeline.
Built with Python standard library http.server for zero external runtime dependencies,
while providing seamless compatibility with FastAPI when installed.
Normative: SWEBOK Chapter 2 / Hexagonal Driving Adapter.
"""

import json
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse
from wsgiref.simple_server import make_server

from agrostat_app.container import create_container

container = create_container()


def application(environ: Dict[str, Any], start_response: Any) -> list:
    """WSGI standard application compliant with Python HTTP ecosystem."""
    path = environ.get("PATH_INFO", "")
    method = environ.get("REQUEST_METHOD", "GET")

    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type"),
    ]

    if method == "OPTIONS":
        start_response("200 OK", headers)
        return [b""]

    try:
        # 1. Healthcheck
        if path == "/health" or path == "/":
            start_response("200 OK", headers)
            response = {
                "status": "HEALTHY",
                "service": "Agrostat Data Science & Engineering Core",
                "architecture": "Hexagonal (Ports & Adapters)",
                "endpoints": [
                    "POST /api/v1/ingest",
                    "POST /api/v1/train",
                    "POST /api/v1/predict",
                    "GET /api/v1/spc",
                    "GET /api/v1/models",
                    "POST /api/v1/pipeline/run",
                ],
            }
            return [json.dumps(response, indent=2).encode("utf-8")]

        # 2. POST /api/v1/ingest
        if path == "/api/v1/ingest" and method == "POST":
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            payload = json.loads(body.decode("utf-8"))

            records = payload.get("records", payload if isinstance(payload, list) else [])
            tag = payload.get("source_tag", "rest_api_upload") if isinstance(payload, dict) else "rest_api_upload"

            res = container.ingestion_use_case.execute_ingestion(records, source_tag=tag)
            start_response("200 OK", headers)
            return [json.dumps(res, indent=2).encode("utf-8")]

        # 3. POST /api/v1/train
        if path == "/api/v1/train" and method == "POST":
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            payload = {}
            if content_length > 0:
                body = environ["wsgi.input"].read(content_length)
                payload = json.loads(body.decode("utf-8"))

            lote = payload.get("lote_id")
            algo = payload.get("algorithm", "random_forest")

            res = container.training_use_case.train_and_register(lote_id=lote, model_algorithm=algo)
            start_response("200 OK", headers)
            return [json.dumps(res, indent=2).encode("utf-8")]

        # 4. POST /api/v1/predict
        if path == "/api/v1/predict" and method == "POST":
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            payload = json.loads(body.decode("utf-8"))

            pred = container.prediction_use_case.predict_harvest_yield(payload)
            start_response("200 OK", headers)
            return [json.dumps(pred.to_dict(), indent=2).encode("utf-8")]

        # 5. GET /api/v1/spc
        if path == "/api/v1/spc" and method == "GET":
            query = parse_qs(environ.get("QUERY_STRING", ""))
            lote = query.get("lote_id", [None])[0]
            metric = query.get("metric", ["rendimiento_kg_ha"])[0]

            limits = container.spc_use_case.analyze_process_stability(lote_id=lote, metric_name=metric)
            start_response("200 OK", headers)
            return [json.dumps(limits.to_dict(), indent=2).encode("utf-8")]

        # 6. GET /api/v1/models
        if path == "/api/v1/models" and method == "GET":
            models = container.registry.list_models()
            start_response("200 OK", headers)
            return [json.dumps({"count": len(models), "models": models}, indent=2).encode("utf-8")]

        # 7. POST /api/v1/pipeline/run
        if path == "/api/v1/pipeline/run" and method == "POST":
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            body = environ["wsgi.input"].read(content_length)
            payload = json.loads(body.decode("utf-8"))

            records = payload.get("records", [])
            tag = payload.get("source_tag", "api_e2e_run")
            sample = payload.get("sample_for_inference")

            summary = container.pipeline_use_case.run_pipeline(
                raw_dataset=records, source_tag=tag, sample_batch_for_inference=sample
            )
            start_response("200 OK", headers)
            return [json.dumps(summary.to_dict(), indent=2).encode("utf-8")]

        # Not Found
        start_response("404 Not Found", headers)
        return [json.dumps({"error": f"Endpoint '{path}' no encontrado"}).encode("utf-8")]

    except Exception as exc:
        start_response("500 Internal Server Error", headers)
        return [json.dumps({"error": str(exc), "type": type(exc).__name__}).encode("utf-8")]


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Runs standard WSGI server."""
    with make_server(host, port, application) as httpd:
        print(f"🚀 Agrostat REST API activa en http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()
