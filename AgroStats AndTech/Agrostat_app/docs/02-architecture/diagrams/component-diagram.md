# Diagrama de Componentes UML (Mermaid)
**Plataforma**: Agrostat Data Intelligence Platform  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Active Skill**: `02-architecture`  

---

```mermaid
graph TB
    %% ==========================================
    %% PRESENTACIÓN Y ADAPTADORES DE ENTRADA
    %% ==========================================
    subgraph DrivingAdapters["1. Capa de Adaptadores de Entrada (Driving)"]
        CLI["CLI Tool (Typer / Argparse)<br/><code>agrostat ingest / predict / spc</code>"]
        API["FastAPI REST Server<br/><code>/api/v1/forecast /spc /market</code>"]
        CRON["Task Scheduler<br/><code>Cron Daemon / Airflow Runner</code>"]
    end

    %% ==========================================
    %% CAPA DE APLICACIÓN
    %% ==========================================
    subgraph Application["2. Capa de Aplicación (Casos de Uso)"]
        UC_INGEST["RunDailyIngestionUseCase"]
        UC_CURATE["RunCurationPipelineUseCase"]
        UC_FORECAST["PredictMarketDemandUseCase"]
        UC_SPC["RunSPCAnalysisUseCase"]
        UC_E2E["EndToEndDataPipelineUseCase"]
    end

    %% ==========================================
    %% CAPA DE DOMINIO PURO
    %% ==========================================
    subgraph CoreDomain["3. Capa de Dominio Puro (Core Domain)"]
        DOM_MODELS["Entidades y VOs<br/><code>Cotizacion, Clima, Divipola, CPC</code>"]
        DOM_VAL["DataQualityValidator<br/><code>Reglas DAMA-BOK</code>"]
        DOM_BIO["BioStatisticalEngine<br/><code>Shewhart 3-Sigma & Reglas Nelson</code>"]
        DOM_ML["TimeSeriesForecaster<br/><code>SARIMAX, Gradient Boosting</code>"]
    end

    %% ==========================================
    %% PUERTOS (INTERFACES ABSTRACTAS)
    %% ==========================================
    subgraph Ports["4. Capa de Puertos (Interfaces Abstractas ABC)"]
        P_IN["Driving Ports<br/><code>IngestionPort, ForecastPort, SPCPort</code>"]
        P_REPO["Driven: LakehouseRepositoryPort"]
        P_EXT["Driven: ExternalSourceExtractorPort"]
        P_DLQ["Driven: DeadLetterQueuePort"]
        P_REG["Driven: ModelRegistryPort"]
        P_NOTIF["Driven: NotificationPort"]
    end

    %% ==========================================
    %% ADAPTADORES DE SALIDA E INFRAESTRUCTURA
    %% ==========================================
    subgraph DrivenAdapters["5. Capa de Adaptadores de Salida (Driven)"]
        ADAPT_DUCK["DuckDBLakehouseRepository<br/><code>SQL DW Engine</code>"]
        ADAPT_SOCRATA["SocrataSipsaExtractor<br/><code>SIPSA_P & SIPSA_A (DANE)</code>"]
        ADAPT_IDEAM["IdeamODataExtractor<br/><code>DHIME Meteorología</code>"]
        ADAPT_NASA["NasaPowerRestExtractor<br/><code>Reanálisis Satelital</code>"]
        ADAPT_DLQ["JsonDeadLetterQueueAdapter<br/><code>Auditoría Cuarentena</code>"]
        ADAPT_REG["JoblibModelRegistryAdapter<br/><code>Model Artifacts & JSON Metas</code>"]
        ADAPT_NOTIF["ConsoleTelemetryAdapter<br/><code>Structured Logging</code>"]
    end

    %% ==========================================
    %% ALMACENAMIENTO FÍSICO (LAKEHOUSE)
    %% ==========================================
    subgraph StorageLakehouse["6. Almacenamiento Físico (Medallion Lakehouse)"]
        FS_BRONZE[("data/bronze/<br/>Raw JSONL / Parquet inmutable")]
        FS_SILVER[("data/silver/<br/>Cleaned & Validated Parquet")]
        FS_GOLD[("data/gold/agro_dw.duckdb<br/>Star Schema OLAP DW")]
        FS_DLQ[("data/dlq/<br/>Quarantined Records JSONL")]
        FS_MODELS[("data/models/<br/>Serialized ML Pipelines")]
    end

    %% Conexiones
    CLI --> P_IN
    API --> P_IN
    CRON --> P_IN

    P_IN --> UC_INGEST
    P_IN --> UC_FORECAST
    P_IN --> UC_SPC
    P_IN --> UC_E2E

    UC_INGEST --> CoreDomain
    UC_FORECAST --> CoreDomain
    UC_SPC --> CoreDomain
    UC_E2E --> UC_INGEST
    UC_E2E --> UC_FORECAST
    UC_E2E --> UC_SPC

    UC_INGEST --> P_REPO
    UC_INGEST --> P_EXT
    UC_INGEST --> P_DLQ
    UC_INGEST --> P_NOTIF

    UC_FORECAST --> P_REPO
    UC_FORECAST --> P_REG

    P_REPO <|.. ADAPT_DUCK
    P_EXT <|.. ADAPT_SOCRATA
    P_EXT <|.. ADAPT_IDEAM
    P_EXT <|.. ADAPT_NASA
    P_DLQ <|.. ADAPT_DLQ
    P_REG <|.. ADAPT_REG
    P_NOTIF <|.. ADAPT_NOTIF

    ADAPT_DUCK --> FS_BRONZE
    ADAPT_DUCK --> FS_SILVER
    ADAPT_DUCK --> FS_GOLD
    ADAPT_DLQ --> FS_DLQ
    ADAPT_REG --> FS_MODELS
```
