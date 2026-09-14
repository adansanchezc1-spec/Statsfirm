# Documento de Arquitectura de Software
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: PLAN -> DEVELOPMENT  
**SDLC Stage**: Design  
**Estándar**: SWEBOK / DAMA-BOK / Clean Architecture  

---

## 1. Visión General del Sistema
La plataforma tecnológica de **Agro Stat & Tech Co.** adopta una **Arquitectura en Tres Capas Analíticas Desacopladas**, diseñada para operar sobre datos provistos por clientes agropecuarios (sin intermediación de hardware propietario ni sensores físicos):
1. **Capa 1: Ingesta Multicanal & Data Contracts**: Recepción segura por lotes (Excel, CSV) o streaming/API (ERPs agrícolas), validación sintáctica y biológica inmediata, y gestión de colas de cuarentena (*Dead Letter Queues*).
2. **Capa 2: Curaduría Geoestadística & Lakehouse**: Almacenamiento inmutable en formatos abiertos (Delta Lake / Apache Iceberg) con procesamiento espacial mediante Apache Sedona e interpolación Kriging ordinaria sobre datos de muestreo.
3. **Capa 3: Decisiones, Yield AI, SPC & BI Ejecutivo**: Motores bioestadísticos de cálculo de cartas Shewhart, pruebas de hipótesis (ANOVA), inferencia de rendimiento y cuadros de mando de rentabilidad por hectárea.

---

## 2. Decisiones de Arquitectura (ADR - Architecture Decision Records)

| ID | Decisión | Alternativas Evaluadas | Justificación Técnica |
|---|---|---|---|
| **AD-001** | **Arquitectura 100% orientada a Software y Analítica (Sin Sensores/Hardware)** | Venta de sensores físicos, despliegue de redes LoRaWAN | El modelo de negocio se enfoca en resolver el problema central: la variabilidad y la falta de capacidad estadística en los datos que los clientes ya generan, evitando costos de capital y mantenimiento de hardware. |
| **AD-002** | **Data Contracts y Validación Preventiva en Ingesta** | Validación tardía en data warehouse | Previene que datos corruptos, outliers o registros biofísicamente imposibles contaminen los modelos de control estadístico ($UCL/LCL$). |
| **AD-003** | **Almacenamiento en Lakehouse de Tablas Abiertas (Delta Lake / Parquet)** | Bases de datos relacionales tradicionales, encierro propietario | Garantiza alta velocidad analítica columnar, *Time Travel* para auditoría agronómica y cumplimiento del principio de *Zero Data Lock-In* para el productor. |
| **AD-004** | **Clean Architecture y Principio de Inversión de Dependencias (DIP)** | Monolito acoplado con scripts dispersos | El núcleo de cálculo bioestadístico (dominio) no depende de los adaptadores de entrada (archivos, APIs) ni de los almacenes de persistencia. |

---

## 3. Validación de Principios SOLID

### 3.1. Single Responsibility Principle (SRP)
- `DataContractValidator`: Responsable exclusivamente de validar la coherencia y tipos de un registro contra las reglas del cultivo.
- `SpcCalculationEngine`: Responsable únicamente de calcular medias, límites de control ($\pm 3\sigma$) e índices de capacidad ($C_p, C_{pk}$).
- `AnovaAnalysisService`: Responsable exclusivamente de contrastes de hipótesis y descomposición de varianza.

### 3.2. Open/Closed Principle (OCP)
- Los contratos de ingesta implementan una interfaz común `IDataContract`. Nuevos esquemas y líneas operativas agroempresariales se agregan extendiendo contratos sin modificar el motor de validación.

### 3.3. Liskov Substitution Principle (LSP)
- Cualquier algoritmo de interpolación o pronóstico implementa `ISurfaceInterpolator` o `IPredictionModel` y puede ser sustituido transparentemente sin alterar la capa de aplicación.

### 3.4. Interface Segregation Principle (ISP)
- Las interfaces de cliente exponen métodos específicos: `IDatasetIngestionPort` para carga, `ISpcAnalyticsPort` para consultas de calidad y `IYieldForecastPort` para proyecciones, evitando interfaces gigantes.

### 3.5. Dependency Inversion Principle (DIP)
- Las capas de aplicación y dominio dependen de abstracciones (`IRepository`, `IStorageGateway`). La infraestructura concreta (Delta Lake, DuckDB, PostgreSQL) implementa dichas interfaces.
