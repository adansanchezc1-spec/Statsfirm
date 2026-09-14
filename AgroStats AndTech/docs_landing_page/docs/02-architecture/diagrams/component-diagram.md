# Diagrama de Componentes de la Arquitectura en Tres Capas Analíticas (Mermaid)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  

```mermaid
graph TB
    subgraph Fuentes de Datos del Cliente (Sin Sensores de Hardware)
        ERP[ERPs Agropecuarios: SAP / AgroWin / Odoo]
        FILES[Planillas de Labores y Cosecha de Campo: Excel / CSV]
        LABS[Ensayos Físico-Químicos de Laboratorio Certificado]
        CLIMA_EXT[Bases de Datos Meteorológicas Comerciales / Públicas]
    end

    subgraph Capa 1: Ingesta Multicanal y Validación
        API_GATEWAY[HTTPS / SFTP Ingestion Gateway]
        PARSER[Multi-Format Dataset Parsers]
        DATA_CONTRACTS[Data Contracts Validator]
        DLQ[(Dead Letter Queue / Cuarentena)]
    end

    subgraph Capa 2: Curaduría y Lakehouse Agrícola
        BRONZE[(Bronze Lake: Raw Ingested Datasets)]
        DBT[dbt / Spark Transformations & Kriging]
        SILVER[(Silver Lake: Curated & Georeferenced Data)]
    end

    subgraph Capa 3: Decisiones, SPC, Yield AI y BI
        SPC_ENGINE[Statistical Process Control Engine: Shewhart / Cp / Cpk]
        YIELD_AI[Yield AI: Modelos Predictivos y Curvas de Maduración]
        BPMN_OPT[BPMN Process Optimization Analyzer]
        DASHBOARD[Consola Web y Tableros Ejecutivos de Rentabilidad]
    end

    ERP --> API_GATEWAY
    FILES --> API_GATEWAY
    LABS --> API_GATEWAY
    CLIMA_EXT --> API_GATEWAY

    API_GATEWAY --> PARSER
    PARSER --> DATA_CONTRACTS
    DATA_CONTRACTS -->|Inválido / Error Biológico| DLQ
    DATA_CONTRACTS -->|Válido| BRONZE

    BRONZE --> DBT
    DBT --> SILVER

    SILVER --> SPC_ENGINE
    SILVER --> YIELD_AI
    SILVER --> BPMN_OPT

    SPC_ENGINE --> DASHBOARD
    YIELD_AI --> DASHBOARD
    BPMN_OPT --> DASHBOARD
```
