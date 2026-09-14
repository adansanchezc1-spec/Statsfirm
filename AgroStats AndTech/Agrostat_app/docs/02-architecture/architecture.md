# Documento de Arquitectura de Software y Datos (SAD)
**Plataforma**: Agrostat Data Intelligence Platform  
**Entidad**: Agro Stat & Tech Co. (División Agroindustrial de Statsfirm Co.)  
**Versión**: 1.0.0  
**Fecha**: 2026-09-14  
**Fase PDCO**: **PLAN → DEVELOPMENT**  
**Active Skill**: `02-architecture`  
**SDLC Stage**: Design / Planning  
**Estándares**: SWEBOK Cap. 2 (Software Design), DAMA-BOK (Data Architecture & Quality), ISO/IEC 25010, IEEE 830, Clean Code, SOLID  

---

## 1. Visión General del Sistema

La **Plataforma Agrostat Data Intelligence** es una solución de ingeniería de datos, analítica bioestadística y pronóstico agropecuario de nivel de producción. Su propósito es capturar, sanear, almacenar y modelar las series temporales de oferta, demanda mayorista, cotizaciones de mercado, balance agroalimentario y variables meteorológicas críticas de Colombia.

El diseño arquitectónico responde a tres retos fundamentales del sector:
1. **Heterogeneidad de Fuentes**: Ingestión desacoplada desde múltiples protocolos gubernamentales y satelitales (Socrata Open Data para SIPSA DANE, OData para DHIME IDEAM, REST JSON para NASA POWER, OData para Evaluaciones Agropecuarias EVA de MinAgricultura).
2. **Gobernanza y Confiabilidad DAMA-BOK**: Curaduría estricta en tres niveles (*Medallion Lakehouse*: Bronze inmutable, Silver validado y tipado, Gold dimensional analítico en estrella) con aislamiento total de anomalías en *Dead Letter Queue* (DLQ).
3. **Alto Rendimiento Analítico sin Overhead de Servidor**: Empleo de **DuckDB** como motor OLAP columnar embebido de ultra alta velocidad, capaz de ejecutar consultas vectorizadas sobre millones de registros en milisegundos con compatibilidad ANSI SQL total y exportabilidad a PostgreSQL.

---

## 2. Decisiones de Arquitectura de Software

| ID | Decisión Arquitectónica | Alternativas Evaluadas | Criterio de Selección y Justificación (RNF) |
|---|---|---|---|
| **AD-001** | **Arquitectura Hexagonal (Ports & Adapters)** | MVC Tradicional, Capas Clásicas (*Layered 3-tier*) | Desacoplamiento radical del núcleo de dominio matemático y de bioestadística frente a librerías de bases de datos, APIs web o formatos de archivo. Facilita pruebas unitarias puras sin mocks complejos (RNF-007, RNF-008). |
| **AD-002** | **Almacenamiento Medallion Lakehouse con DuckDB + Parquet** | PostgreSQL Dedicado, Spark Cluster, SQLite | DuckDB ofrece rendimiento analítico vectorial de nivel OLAP (10x-100x más rápido que SQLite y PostgreSQL en consultas dimensionales complejas), cero costo de infraestructura, compatibilidad ANSI SQL estándar (RNF-004) y almacenamiento columnar en Parquet local (RNF-001, RNF-002). |
| **AD-003** | **Modelo Dimensional Kimball en Estrella (Star Schema)** | Esquema 3NF Normalizado, Data Vault 2.0 | La dimensionalidad en estrella optimiza consultas de BI y series de tiempo con agregaciones rápidas por tiempo, geografía DIVIPOLA, producto CPC y mercado mayorista (RF-011, RF-012, RNF-002). |
| **AD-004** | **Curaduría No Destructiva con Dead Letter Queue (DLQ)** | Mutación silenciosa con medias, Drop row sin log | Alineación con DAMA-BOK: la información en crudo jamás se altera. Todo dato rechazado por completitud o rango genera una auditoría con el motivo de fallo en JSON estructurado (RF-006 a RF-010, RNF-003, RNF-006). |
| **AD-005** | **Estrategia Polimórfica de Extracción (Factory + Strategy)** | Script monolítico de scraping/curl | Permite incorporar nuevos conectores de gremios o satélites implementando una interfaz abstracta común sin tocar el motor de orquestación (OCP, ISP). |

---

## 3. Estructura de Capas e Interfaces del Sistema

Siguiendo el patrón Hexagonal, el sistema se divide en cuatro capas concéntricas con regla de dependencia hacia el interior:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ADAPTADORES DE ENTRADA                          │
│          CLI Runner (Typer)  │  FastAPI REST Server  │  CRON / Scheduler│
└────────────────────────────────────┬───────────────────────────────────┘
                                     │ (invoca Driving Ports)
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          CAPA DE APLICACIÓN                            │
│  RunDailyIngestionUseCase     │ TrainForecastingModelUseCase          │
│  RunCurationPipelineUseCase   │ PredictMarketDemandUseCase            │
│  GenerateSPCDashboardUseCase  │ ExecuteEndToEndPipelineUseCase         │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │ (orquesta)                      │ (usa Driven Ports)
                   ▼                                 ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│            CAPA DE DOMINIO           │  │      PUERTOS DE SALIDA       │
│  Entidades:                          │  │  (Interfaces Abstractas ABC) │
│   - CotizacionMayorista              │  │                              │
│   - RegistroAbastecimiento           │  │  - LakehouseRepositoryPort   │
│   - ObservacionClimatica             │  │  - DeadLetterQueuePort       │
│   - SerieTiempoDemanda               │  │  - ExternalSourceExtractorPort│
│   - LimitesControlShewhart           │  │  - ModelRegistryPort         │
│  Value Objects:                      │  │  - NotificationPort          │
│   - DivipolaCode, CpcCode            │  └──────────────┬───────────────┘
│   - ConfidenceInterval, MetricRecord │                 │
│  Servicios de Dominio:               │                 │ (implementado por)
│   - DataQualityValidator (DAMA-BOK)  │                 ▼
│   - BioStatisticalEngine (SPC/Nelson)│  ┌──────────────────────────────┐
│   - TimeSeriesForecaster             │  │    ADAPTADORES DE SALIDA     │
│   - MarketBalanceCalculator          │  │  - DuckDBLakehouseAdapter    │
└──────────────────────────────────────┘  │  - SocrataSipsaAdapter       │
                                          │  - IdeamODataAdapter         │
                                          │  - NasaPowerRestAdapter      │
                                          │  - JsonAuditDLQAdapter       │
                                          │  - JoblibModelRegistryAdapter│
                                          └──────────────────────────────┘
```

### 3.1. Responsabilidades por Capa

1. **Capa de Dominio Puro (`src/agrostat_app/domain/`)**:
   - Totalmente agnóstica a frameworks externos y librerías de persistencia.
   - Modela las entidades de negocio agrícola con invariantes estrictas.
   - Alberga las reglas bioestadísticas (cálculo de límites $\bar{X} \pm 3\sigma$, Reglas de Nelson 1 a 4, índices de estacionalidad agrícola) y validaciones DAMA-BOK.

2. **Capa de Puertos (`src/agrostat_app/ports/`)**:
   - Define los contratos formales mediante Clases Base Abstractas (`abc.ABC`) y type hinting.
   - **Puertos de Entrada (Driving Ports)**: Exponen casos de uso al mundo exterior.
   - **Puertos de Salida (Driven Ports)**: Abstraen el almacenamiento OLAP, la cuarentena de datos, los modelos de ML y las fuentes externas.

3. **Capa de Aplicación (`src/agrostat_app/application/`)**:
   - Coordina los flujos de ejecución (casos de uso transaccionales y analíticos).
   - Recibe DTOs tipados, valida flujos de negocio, delega en servicios de dominio y persiste vía puertos de salida.

4. **Capa de Adaptadores (`src/agrostat_app/adapters/`)**:
   - **Driving**: Interfaz de Línea de Comandos (CLI interactivo con comandos modulares) y Servidor API REST OpenAPI con FastAPI.
   - **Driven**: Conector DuckDB con soporte SQL nativo para el Data Warehouse dimensional, adaptadores HTTP para APIs gubernamentales (DANE/IDEAM/NASA), y almacenamiento de modelos serializados.

---

## 4. Validación Rigurosa de Principios SOLID

| Principio | Componente / Clase Evaluada | Cumplimiento y Mecanismo Arquitectónico |
|---|---|---|
| **S - Single Responsibility** | `DataQualityValidator` | Su única responsabilidad es auditar registros contra las dimensiones de calidad DAMA-BOK (completitud, rango, formato, consistencia). No conoce almacenamiento, no persiste en disco y no envía alertas. |
| **S - Single Responsibility** | `DuckDBLakehouseAdapter` | Su única responsabilidad es ejecutar operaciones SQL e I/O en DuckDB/Parquet. No aplica lógica de negocio ni toma decisiones sobre anomalías agronómicas. |
| **O - Open/Closed** | `ExtractorFactory` & `BaseSourceExtractor` | Nuevas fuentes oficiales (ej. UPRA Geoportal o Fedearroz) se incorporan creando un nuevo adaptador concreto derivado de `BaseSourceExtractor`, sin tocar el orquestador ni las fuentes existentes. |
| **L - Liskov Substitution** | `LakehouseRepositoryPort` | Cualquier implementación (ej. `DuckDBRepository`, `PostgreSQLRepository` o un `MockMemoryRepository` para testing) es 100% sustituible sin romper ningún caso de uso de aplicación. |
| **I - Interface Segregation** | Puertos de Salida Segregados | Se divide el acceso en interfaces especializadas: `LakehouseRepositoryPort`, `DeadLetterQueuePort`, `ModelRegistryPort` y `NotificationPort`. Ningún adaptador está forzado a implementar métodos que no necesita. |
| **D - Dependency Inversion** | Casos de Uso $\rightarrow$ Puertos | La capa de aplicación (`RunDailyIngestionUseCase`) depende exclusivamente de las abstracciones de los puertos. La inyección de dependencias concreta se realiza centralizadamente en `container.py` al arrancar el sistema. |

---

## 5. Radar de Antipatrones y Medidas de Mitigación

```
[ALERTA ANTIPATRÓN]  ──► [MITIGACIÓN ARQUITECTÓNICA IMPLEMENTADA]

1. ⚠️ God Class / God ETL Pipeline
   Riesgo: Un script único de 2,000 líneas que extrae, parsea, valida, calcula estadísticas y hace gráficos.
   Mitigación: Separación estricta en Casos de Uso monoproducto, Servicios de Dominio desacoplados y Adaptadores de E/S.

2. ⚠️ Spaghetti Data Wrangling (Pandas Chained Mutations)
   Riesgo: Cadenas de manipulación de DataFrames con `inplace=True` y mutaciones impredecibles.
   Mitigación: Pipeline funcional puro; contratos inmutables de datos; validación declarativa campo a campo.

3. ⚠️ Hard Coding de Endpoints, URLs y Rutas
   Riesgo: URLs de datos.gov.co o rutas locales escritas directamente en las funciones.
   Mitigación: Módulo de configuración centralizado `config.py` tipado con `pydantic-settings` y variables de entorno `.env`.

4. ⚠️ Magic Numbers en Umbrales Agronómicos
   Riesgo: Usar números mágicos como `3.0` o `0.05` dispersos en el código de anomalías.
   Mitigación: Enumeraciones y constantes semánticas (`NelsonRuleThresholds`, `DamaQualityThresholds`, `AgroTaxonomyConstants`).

5. ⚠️ Silently Swallowed Exceptions
   Riesgo: Bloques `except: pass` que ocultan fallos de conexión o caídas de las APIs del DANE o IDEAM.
   Mitigación: Jerarquía de excepciones de dominio (`AgrostatDomainError`, `SourceExtractionError`, `DataQualityThresholdViolation`) con logs contextuales y derivación a DLQ.
```

---

## 6. Stack Tecnológico Seleccionado y Justificado

| Capa / Módulo | Tecnología / Librería | Versión | Justificación Técnica |
|---|---|---|---|
| **Lenguaje Base** | Python | 3.11+ | Soporte nativo de typing estricto, pattern matching estructural, alto rendimiento en librerías numéricas y madurez en data engineering. |
| **Motor OLAP / SQL** | DuckDB | 0.10+ / 1.0+ | Motor SQL columnar embebido de alto rendimiento. Lectura y escritura directa de archivos Parquet, capacidades analíticas avanzadas (Window functions, time-series bucketing) sin necesidad de servidor de BD corriendo como daemon externo. |
| **Formato de Persistencia** | Apache Parquet | Snappy / ZSTD | Formato columnar abierto, compresión de 80%+ sobre CSV, tipado embebido y lectura particionada por fecha y municipio. |
| **Modelado y Validación** | Pydantic v2 | 2.6+ | Validación de contratos de entrada ultrarrápida compilada en Rust. Inmutabilidad y exportación JSON limpia. |
| **Cálculo Numérico & ML** | NumPy, SciPy, Scikit-learn | 1.26+ / 1.4+ | Motores estándar para control estadístico de procesos (Shewhart/Nelson), bioestadística aplicada y modelos de regresión de rendimiento. |
| **Framework Web / API** | FastAPI | 0.110+ | API asíncrona moderna de alto rendimiento con documentación OpenAPI (Swagger) generada automáticamente. |
| **CLI Interactivo** | Click / Typer | 0.9+ | Construcción de interfaces de línea de comandos robustas y autodescriptivas. |
| **Testing & Calidad** | Pytest, Ruff, Black | 8.0+ | Cobertura de pruebas unitarias y de integración > 85%, cumplimiento estricto de PEP 8 y formateo homogéneo. |
