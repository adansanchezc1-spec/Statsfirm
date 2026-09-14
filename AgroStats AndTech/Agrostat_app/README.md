# Agrostat App: Hexagonal Architecture Data Science & Engineering Platform

> **AgroStats & Tech** (Unidad Agropecuaria de *Statsfirm Co.*)  
> **Normativas**: SWEBOK (Software Engineering Body of Knowledge), DAMA-BOK (Data Management Body of Knowledge), ISO/IEC 25010, Clean Code & PEP 8.  
> **Fase PDCO**: **CONTROL** / **OPERATIONS** | **Versión**: 1.0.0

---

## 1. Visión General del Sistema

**Agrostat App** es una plataforma de ingeniería y ciencia de datos construida bajo el patrón de **Arquitectura Hexagonal (Ports & Adapters)**. Su objetivo principal es resolver la necesidad de analítica avanzada y control estadístico en la agroindustria, desacoplando completamente la lógica de negocio bioestadística de cualquier framework o tecnología de almacenamiento.

### Capacidades Principales
- **Ingesta y Validación DAMA-BOK**: Evaluación en tiempo de streaming de completitud, validez de rangos agronómicos, consistencia lógica (ej. kilos exportables $\le$ kilos totales) y unicidad de lotes.
- **Lakehouse Medallion con Dead Letter Queue (DLQ)**:
  - **Bronze**: Almacenamiento inmutable en crudo (JSON / Parquet auditado).
  - **Silver**: Registros limpios, tipados y enriquecidos como entidades de dominio.
  - **Gold**: Data Mart de características para Machine Learning e inferencia.
  - **DLQ**: Archivo auditado de anomalías para trazabilidad y re-procesamiento.
- **Biostatistical Process Control (SPC)**: Líneas de control Shewhart ($\bar{X} \pm 3\sigma$), evaluación de las 4 principales **Reglas de Nelson** para detección temprana de desviaciones y cálculo de índices de capacidad $C_p$ y $C_{pk}$.
- **MLOps & Yield Forecasting**: Feature Store agronómico (ratios brix/calibre, exportabilidad, codificación cíclica sin/cos de meses), modelos Random Forest / Gradient Boosting con serialización y versionado en registro y generación de intervalos de confianza al 95%.

---

## 2. Arquitectura Hexagonal (Ports & Adapters)

```
                            PUERTOS DE ENTRADA (Driving Ports)
                ┌────────────────────────────────────────────────────────┐
                │   • IngestionPipelinePort   • ModelTrainingPipelinePort│
                │   • YieldInferencePort      • SPCAnalysisPort          │
                └───────────────────────────▲────────────────────────────┘
                                            │
   ADAPTADORES DE ENTRADA                   │
  ┌───────────────────────┐                 │
  │ • CLI Adapter         │─────────────────┤
  │   (agrostat_app/cli)  │                 │
  │ • REST API Server     │─────────────────┤
  │   (http.server 8000)  │                 │
  └───────────────────────┘                 ▼
                             ┌───────────────────────────────┐
                             │       CAPA DE APLICACIÓN      │
                             │  • RunIngestionPipelineUC     │
                             │  • TrainYieldModelUC          │
                             │  • PredictYieldUC             │
                             │  • RunSPCAnalysisUC           │
                             │  • EndToEndDataPipelineUC     │
                             └──────────────┬────────────────┘
                                            │
                                            ▼
                             ┌───────────────────────────────┐
                             │       NÚCLEO DE DOMINIO       │
                             │  • Entidades: HarvestBatch,   │
                             │    SPCControlLimits           │
                             │  • Value Objects: Nelson,     │
                             │    YieldPrediction, Quality   │
                             │  • Servicios de Dominio:      │
                             │    - DataQualityValidator     │
                             │    - BioStatisticalEngine     │
                             │    - FeatureEngineeringService│
                             └──────────────┬────────────────┘
                                            │
                ┌───────────────────────────▼────────────────────────────┐
                │   • HarvestRepositoryPort   • DeadLetterQueuePort      │
                │   • ModelRegistryPort       • NotificationPort         │
                └───────────────────────────┬────────────────────────────┘
                            PUERTOS DE SALIDA (Driven Ports)
                                            │
                                            ▼
   ADAPTADORES DE SALIDA
  ┌──────────────────────────────────────────────────────────────────────┐
  │ • ParquetLakehouseRepository (Bronze, Silver, Gold Parquet/JSON)     │
  │ • JsonDeadLetterQueueAdapter (DLQ persistent audit log)              │
  │ • SklearnModelRegistryAdapter (PKL binaries + model metadata index)  │
  │ • ConsoleTelemetryAdapter (ASCII safe structured logging)            │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Estructura del Código Fuente

```
AgroStats AndTech/Agrostat_app/
├── config.py                     <- Configuración central y resolución de rutas
├── container.py                  <- Composition Root (Inyección de Dependencias)
├── pyproject.toml                <- Configuración estándar PEP 517/518
├── requirements.txt              <- Dependencias de producción y desarrollo
├── README.md                     <- Este documento técnico
├── src/
│   └── agrostat_app/
│       ├── domain/               <- Lógica Pura (Cero dependencias externas)
│       │   ├── entities.py       <- HarvestBatch, SPCControlLimits
│       │   ├── value_objects.py  <- YieldPrediction, NelsonViolation, DataQualityReport
│       │   ├── exceptions.py     <- Excepciones de dominio tipadas
│       │   └── services/         <- Validadores y motores matemáticos
│       │       ├── data_quality_validator.py
│       │       ├── biostatistical_engine.py
│       │       └── feature_engineering.py
│       ├── ports/                <- Contratos de interfaz (abc.ABC)
│       │   ├── in_ingestion_port.py
│       │   ├── in_training_port.py
│       │   ├── in_prediction_port.py
│       │   ├── in_spc_port.py
│       │   ├── out_repository_port.py
│       │   ├── out_dlq_port.py
│       │   ├── out_registry_port.py
│       │   └── out_notification_port.py
│       ├── application/          <- Casos de uso y orquestación
│       │   ├── dtos.py           <- Objetos de transferencia de datos
│       │   └── use_cases/
│       │       ├── run_ingestion_pipeline.py
│       │       ├── train_yield_model.py
│       │       ├── predict_yield.py
│       │       ├── run_spc_analysis.py
│       │       └── end_to_end_pipeline.py
│       └── adapters/             <- Implementaciones de infraestructura
│           ├── driving/          <- CLI y Servidor HTTP REST
│           │   ├── cli.py
│           │   └── api/
│           │       └── server.py
│           └── driven/           <- Almacenamiento, DLQ, Model Registry, Telemetría
│               ├── parquet_repository.py
│               ├── json_dlq_adapter.py
│               ├── sklearn_registry.py
│               └── console_notifier.py
└── tests/
    ├── conftest.py               <- Fixtures y generadores de datos sintéticos
    ├── run_tests.py              <- Runner automatizado de pruebas ISO/IEC 25010
    ├── unit/                     <- Pruebas unitarias de dominio
    │   ├── test_data_quality_validator.py
    │   ├── test_biostatistical_engine.py
    │   └── test_feature_engineering.py
    └── integration/              <- Pruebas de integración de casos de uso
        └── test_pipeline_use_cases.py
```

---

## 4. Guía de Uso del CLI

El módulo `agrostat_app` expone una interfaz de línea de comandos rica y modular.

### 1. Ejecutar el Pipeline Completo End-to-End
Genera datos sintéticos, los ingesta en Bronze, valida contratos DAMA-BOK, filtra hacia Silver y DLQ, extrae features a Gold, entrena un modelo Random Forest, genera una inferencia con IC 95% y audita el proceso con límites SPC y Reglas de Nelson:
```bash
$env:PYTHONPATH = "src"
python -m agrostat_app pipeline --samples 30
```

### 2. Generar Lotes Sintéticos Crudos
```bash
python -m agrostat_app generate-data --count 25 --output data/raw_batch.json
```

### 3. Ingestar y Validar Datos Crudos
```bash
python -m agrostat_app ingest --file data/raw_batch.json --tag "cosecha_semana_37"
```

### 4. Entrenar y Registrar un Modelo
```bash
python -m agrostat_app train --algorithm random_forest --test-size 0.25
```

### 5. Inferencia de Rendimiento con Intervalo de Confianza
```bash
python -m agrostat_app predict --lote LOTE-PALMA-01 --hectareas 10.5 --kilos 12500 --brix 14.5 --calibre 48
```

### 6. Auditoría Bioestadística SPC
Calcula límites Shewhart ($\bar{X} \pm 3\sigma$) y analiza las Reglas de Nelson:
```bash
python -m agrostat_app spc --metric rendimiento_kg_ha --usl 1600 --lsl 800
```

### 7. Listar Modelos Registrados
```bash
python -m agrostat_app models
```

---

## 5. API REST HTTP

El adaptador HTTP de entrada proporciona un servicio REST sin dependencias externas:

### Iniciar el Servidor REST
```bash
$env:PYTHONPATH = "src"
python -m agrostat_app.adapters.driving.api.server --port 8000
```

### Endpoints Disponibles
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Chequeo de salud del servicio y rutas del Lakehouse |
| `POST` | `/api/v1/ingest` | Ingesta de payload JSON crudo con validación DAMA-BOK |
| `POST` | `/api/v1/train` | Disparo del pipeline de reentrenamiento de modelos |
| `POST` | `/api/v1/predict` | Inferencia en tiempo real con intervalos de confianza al 95% |
| `GET` | `/api/v1/spc` | Auditoría de estabilidad y capacidad de proceso |
| `POST` | `/api/v1/pipeline/run` | Ejecución orquestada del pipeline End-to-End |

---

## 6. Aseguramiento de Calidad y Pruebas (QA)

Conforme a la norma **ISO/IEC 25010** y el capítulo 5 del **SWEBOK**, el sistema cuenta con una suite completa de pruebas unitarias y de integración que se ejecutan sin dependencias externas mediante el runner nativo:

```bash
$env:PYTHONPATH = "src"
python tests/run_tests.py
```

### Cobertura de Pruebas
- **`test_data_quality_validator.py`** (5 pruebas):
  - Completitud (detección de campos obligatorios faltantes).
  - Validez de rangos (grados Brix, pH del suelo, calibres).
  - Consistencia lógica (kilos exportables vs kilos totales).
  - Unicidad en stream de ingestión.
- **`test_biostatistical_engine.py`** (5 pruebas):
  - Umbrales de tamaño muestral mínimo ($N \ge 10$).
  - Proceso bajo control estadístico y cálculo de $\bar{X} \pm 3\sigma$.
  - Regla de Nelson 1 (puntos a más de $3\sigma$).
  - Regla de Nelson 2 (sesgo sistemático de 9 puntos del mismo lado de la media).
  - Regla de Nelson 3 (tendencia sostenida de 6 puntos crecientes/decrecientes).
- **`test_feature_engineering.py`** (2 pruebas):
  - Extracción y dimensiones exactas de matrices $X$ e $y$.
  - Imputación agronómica de valores nulos o ambientales faltantes.
- **`test_pipeline_use_cases.py`** (5 pruebas de integración):
  - Enrutamiento simultáneo a Silver y DLQ en ambiente aislado temporal.
  - Ajuste de modelo, cálculo de $R^2$, RMSE, MAE y registro en Registry.
  - Inferencia con modelo activo y bandas de confianza.
  - Auditoría SPC sobre lotes reales almacenados.
  - Orquestación End-to-End completa (`EndToEndDataPipelineUseCase`).

**Resultado**: **17 pruebas ejecutadas, 17 exitosas (100% aprobación)** en 1.31 s.
