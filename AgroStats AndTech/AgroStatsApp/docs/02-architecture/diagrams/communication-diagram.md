# Diagrama de Comunicación / Colaboración UML (Mermaid)
**Plataforma**: Agrostat Data Intelligence Platform  
**Proceso**: Colaboración entre Objetos para la Ingestión y Verificación de Calidad  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Active Skill**: `02-architecture`  

---

```mermaid
graph LR
    CLI((":IngestionCLIController")) -->|1: ejecutar_ingesta(fecha)| UC((":RunDailyIngestionUseCase"))
    UC -->|2: extraer_lote(fecha)| EXT((":ExternalSourceExtractor"))
    UC -->|3: guardar_bronze(lote_crudo)| REPO((":DuckDBLakehouseRepository"))
    UC -->|4: validar_lote(registros)| VAL((":DataQualityValidator"))
    VAL -->|4.1: evaluar_completitud()| RULE1((":CompletenessRule"))
    VAL -->|4.2: evaluar_rangos()| RULE2((":ValueRangeRule"))
    VAL -->|4.3: evaluar_consistencia()| RULE3((":CrossFieldConsistencyRule"))
    UC -->|5 [si inválido]: desviar_cuarentena(error)| DLQ((":JsonDeadLetterQueueAdapter"))
    UC -->|6 [si válido]: guardar_silver(curados)| REPO
    UC -->|7: refrescar_hechos_gold()| REPO
    UC -->|8: verificar_anomalias_spc()| BIO((":BioStatisticalEngine"))
    UC -->|9 [si anomalia]: notificar_alerta(evento)| NOTIF((":ConsoleTelemetryNotifier"))
```
