# Diagrama de Secuencia UML (Mermaid)
**Plataforma**: Agrostat Data Intelligence Platform  
**Proceso**: Ingesta Diaria, Curaduría DAMA-BOK, Carga Dimensional DuckDB y Detección de Anomalías  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Active Skill**: `02-architecture`  

---

```mermaid
sequenceDiagram
    autonumber
    actor CLI_Cron as Operador / CRON Job
    participant IngestionController as IngestionCLIController
    participant IngestionUseCase as RunDailyIngestionUseCase
    participant SipsaExtractor as SocrataSipsaExtractorAdapter
    participant IdeamExtractor as IdeamODataExtractorAdapter
    participant Validator as DataQualityValidator (Dominio)
    participant DLQ as JsonDeadLetterQueueAdapter
    participant Lakehouse as DuckDBLakehouseRepository
    participant BioEngine as BioStatisticalEngine (Dominio)
    participant Notifier as NotificationAdapter

    CLI_Cron->>IngestionController: agrostat ingest --date 2026-09-14
    IngestionController->>IngestionUseCase: ejecutar_ingesta_diaria(2026-09-14)
    
    %% Ingesta Capa Bronze
    par Extracción Paralela de Fuentes Oficiales
        IngestionUseCase->>SipsaExtractor: extraer_lote(2026-09-14)
        SipsaExtractor-->>IngestionUseCase: RawBatch (Precios y Abastecimiento SIPSA)
    and
        IngestionUseCase->>IdeamExtractor: extraer_lote(2026-09-14)
        IdeamExtractor-->>IngestionUseCase: RawBatch (Meteorología IDEAM)
    end

    IngestionUseCase->>Lakehouse: guardar_bronze(lotes_crudos)
    Lakehouse-->>IngestionUseCase: bronze_batch_id (SHA-256 verificado)

    %% Curaduría Capa Silver (DAMA-BOK)
    loop Por cada registro en el lote
        IngestionUseCase->>Validator: validar_registro(registro_crudo)
        alt Registro Válido (Completitud, Rangos, Coherencia)
            Validator-->>IngestionUseCase: Status OK (Entidad Normalizada)
        else Registro Inválido / Anómalo
            Validator-->>IngestionUseCase: ValidationViolation(motivo="precio_min > precio_max")
            IngestionUseCase->>DLQ: enviar_a_cuarentena(registro_crudo, diagnostico)
            DLQ-->>IngestionUseCase: quarantine_ack
        end
    end

    %% Persistencia Silver & Gold
    IngestionUseCase->>Lakehouse: guardar_silver(entidades_curadas)
    Lakehouse-->>IngestionUseCase: silver_count_guardado

    IngestionUseCase->>Lakehouse: upsert_gold_fact_tables(fecha=2026-09-14)
    Lakehouse-->>IngestionUseCase: gold_refresh_ack (fact_precios_sipsa, fact_clima_diario)

    %% Control Estadístico Bioestadístico
    IngestionUseCase->>Lakehouse: cargar_series_recientes(producto="Papa R-12 Diacol", ventana_dias=30)
    Lakehouse-->>IngestionUseCase: serie_tiempo_precios
    IngestionUseCase->>BioEngine: verificar_reglas_nelson(serie_tiempo_precios)
    BioEngine-->>IngestionUseCase: violaciones_detectadas (ej. "Regla 1: Precio supera +3 sigma")

    opt Violación de Límites de Control o Tasa DLQ > 5%
        IngestionUseCase->>Notifier: notificar_alerta(anomalia_spc)
        Notifier-->>IngestionUseCase: alerta_despachada
    end

    IngestionUseCase-->>IngestionController: PipelineExecutionSummary (Válidos, DLQ, Métricas)
    IngestionController-->>CLI_Cron: 200 OK — Pipeline completado exitosamente
```
