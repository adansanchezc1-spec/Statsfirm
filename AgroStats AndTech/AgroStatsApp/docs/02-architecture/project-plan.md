# Plan de Proyecto y Hoja de Ruta de Implementación (WBS)
**Plataforma**: Agrostat Data Intelligence Platform  
**Entidad**: Agro Stat & Tech Co. (División Agroindustrial de Statsfirm Co.)  
**Versión**: 1.0.0  
**Fecha**: 2026-09-14  
**Fase PDCO**: **PLAN → DEVELOPMENT**  
**Active Skill**: `02-architecture`  
**SDLC Stage**: Design / Planning  
**Estándares**: SWEBOK (Software Engineering Management & Construction), DAMA-BOK, ISO/IEC 25010  

---

## 1. Estructura de Desglose del Trabajo (WBS - Work Breakdown Structure)

El proyecto se estructura en 5 paquetes de trabajo principales para transicionar de la fase **PLAN** a **DEVELOPMENT** (Skill 03) y **CONTROL** (Skill 04):

```
1.0 AGROSTAT DATA INTELLIGENCE PLATFORM
│
├── 1.1 GOBERNANZA Y DOMINIO PURO (Skill 03 - Core Domain)
│   ├── 1.1.1 Entidades canónicas (CotizacionMayorista, ObservacionClimatica, BalanceMercado)
│   ├── 1.1.2 Value Objects (DivipolaCode, CpcProductCode, LimitesControlShewhart)
│   ├── 1.1.3 Excepciones jerárquicas de dominio
│   ├── 1.1.4 Validador DAMA-BOK (Completitud, Rangos, Consistencia, Unicidad)
│   └── 1.1.5 Motor Bioestadístico (Shewhart 3-sigma, Reglas de Nelson 1 a 4)
│
├── 1.2 PUERTOS Y CONTRATOS ABSTRACTOS (Skill 03 - Ports & DTOs)
│   ├── 1.2.1 Puertos de entrada (Driving: Ingestion, Forecasting, SPC)
│   ├── 1.2.2 Puertos de salida (Driven: Lakehouse, DLQ, SourceExtractor, Notifier)
│   └── 1.2.3 Data Transfer Objects (DTOs tipados con Pydantic)
│
├── 1.3 ADAPTADORES DE INFRAESTRUCTURA Y CONECTORES (Skill 03 - Adapters)
│   ├── 1.3.1 Repositorio Lakehouse DuckDB / Parquet (Medallion Bronze/Silver/Gold)
│   ├── 1.3.2 Adaptador de Cuarentena Dead Letter Queue (DLQ JSON auditado)
│   ├── 1.3.3 Conectores oficiales: DANE SIPSA (Socrata API), IDEAM (OData) y NASA POWER
│   └── 1.3.4 Adaptadores de interfaz: CLI interactivo (Typer) y API REST (FastAPI)
│
├── 1.4 CASOS DE USO Y ORQUESTACIÓN (Skill 03 - Application)
│   ├── 1.4.1 Ingesta diaria y curaduría automatizada
│   ├── 1.4.2 Agregación dimensional y refresco de vistas analíticas en DuckDB
│   ├── 1.4.3 Pronóstico de demanda de corto/mediano plazo (1-12 semanas)
│   └── 1.4.4 Pipeline End-to-End con manejo resiliente de errores
│
└── 1.5 CONTROL DE CALIDAD Y PRUEBAS AUTOMATIZADAS (Skill 04 - Testing)
    ├── 1.5.1 Pruebas unitarias de dominio con cobertura > 85%
    ├── 1.5.2 Pruebas de integración de conectores y repositorio DuckDB
    ├── 1.5.3 Pruebas de punta a punta (E2E) del pipeline
    └── 1.5.4 Verificación de estándares PEP 8, typing con mypy y linting con ruff
```

---

## 2. Matriz de Trazabilidad de Requerimientos (RTM)

| Requerimiento (SRS) | Componente de Arquitectura | Entregable de Código (Skill 03) | Prueba de Verificación (Skill 04) |
|---|---|---|---|
| **RF-001** (SIPSA Precios) | `SocrataSipsaExtractorAdapter` | `adapters/driven/socrata_extractor.py` | `test_sipsa_extractor.py` |
| **RF-002** (SIPSA Abastecimiento) | `SocrataAbastecimientoAdapter` | `adapters/driven/socrata_extractor.py` | `test_abastecimiento_extractor.py` |
| **RF-004** (IDEAM Clima) | `IdeamODataExtractorAdapter` | `adapters/driven/ideam_extractor.py` | `test_ideam_extractor.py` |
| **RF-005** (Bronze Inmutable) | `DuckDBLakehouseRepository` | `adapters/driven/duckdb_repository.py` | `test_bronze_storage.py` |
| **RF-006 a RF-010** (DAMA-BOK / DLQ) | `DataQualityValidator` & `JsonDLQ` | `domain/services/data_quality_validator.py` | `test_data_quality_validator.py` |
| **RF-011 & RF-012** (Kimball Star DW) | `DuckDBLakehouseRepository` | `sql/schema_agro_dw.sql` & repo adapter | `test_dimensional_dw.py` |
| **RF-013** (Vistas Agregadas) | Vistas SQL en DuckDB | `sql/schema_agro_dw.sql` (vistas analíticas) | `test_analytical_views.py` |
| **RF-014** (SPC & Reglas Nelson) | `BioStatisticalEngine` | `domain/services/biostatistical_engine.py` | `test_biostatistical_engine.py` |
| **RF-015** (Forecasting 1-12 semanas)| `TimeSeriesForecaster` | `domain/services/forecasting_engine.py` | `test_forecasting_engine.py` |
| **RNF-001** (Performance < 30s) | DuckDB Vectorized Execution | `adapters/driven/duckdb_repository.py` | `test_performance_benchmark.py` |
| **RNF-004** (ANSI SQL Portabilidad) | SQL DDL compatible ANSI | `sql/schema_agro_dw.sql` | `validate_sql_schema.py` |
| **RNF-007** (Arquitectura Hexagonal)| Ports & Adapters Isolation | `ports/`, `domain/`, `application/` | `test_architecture_isolation.py` |

---

## 3. Cronograma de Sprints y Fases de Ejecución

```
SPRINT 1: Core Domain & Data Quality (DAMA-BOK)
├── Duración: 1 semana
├── Entregables: Entidades, Value Objects, DataQualityValidator, BioStatisticalEngine.
└── Criterio de Éxito: Cobertura unitaria de lógica pura > 90%.

SPRINT 2: Lakehouse Repository & DuckDB OLAP Integration
├── Duración: 1 semana
├── Entregables: Adaptador DuckDB, carga de esquema Star Schema Kimball, seeds canónicas y DLQ JSON.
└── Criterio de Éxito: Ejecución exitosa de queries analíticas sobre tablas de hechos en < 100 ms.

SPRINT 3: External Connectors & Pipeline Orchestration
├── Duración: 1 semana
├── Entregables: Conectores DANE SIPSA, IDEAM y NASA POWER; Casos de Uso del Pipeline diario.
└── Criterio de Éxito: Flujo completo Bronze -> Silver -> Gold con desvío automático a DLQ ante datos anómalos.

SPRINT 4: Forecasting, SPC Dashboard & Interfaces (CLI/API)
├── Duración: 1 semana
├── Entregables: TimeSeriesForecaster, subcomandos CLI (Typer), endpoints FastAPI (Swagger).
└── Criterio de Éxito: Pronóstico a 1-12 semanas con intervalos de confianza del 95% y detección de anomalías Nelson.
```

---

## 4. Definición de Hecho (Definition of Done - DoD)

Para considerar completado cualquier componente durante la fase de desarrollo (Skill 03):
1. **PEP 8 & Clean Code**: 0 errores en `ruff` y formateo con `black`.
2. **SOLID Verificado**: Ninguna violación a los 5 principios SOLID.
3. **Pruebas Unitarias**: Todo servicio o adaptador cuenta con su archivo de tests en `tests/unit/` o `tests/integration/` con cobertura mínima del 85%.
4. **Documentación Técnica**: Docstrings tipados según Google Style / PEP 257 en todas las clases y métodos públicos.
5. **Trazabilidad**: Registro del commit y actualización correspondiente en `metadata.json`.
