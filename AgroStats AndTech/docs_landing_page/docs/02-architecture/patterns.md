# Catálogo de Patrones de Diseño Aplicados (GoF & GRASP)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: PLAN -> DEVELOPMENT  
**SDLC Stage**: Design  

---

## 1. Patrones GoF (Gang of Four)

### 1.1. Strategy (Comportamiento)
- **Problema**: Diferentes cultivos y variables agropecuarias requieren diferentes formulaciones estadísticas para el cálculo de límites de control (cartas de variables continuas como $\bar{X}-S$ vs. cartas de atributos discretos como $p$ o $np$ para defectos o variabilidad en cosecha).
- **Aplicación**: Interfaz `ISpcStrategy` con implementaciones concretas `VariablesSpcStrategy`, `AttributesSpcStrategy` y `CuSumSpcStrategy`.
- **Beneficio**: Permite intercambiar el algoritmo de control estadístico en tiempo de ejecución según la naturaleza de los datos del cliente sin alterar la lógica de negocio.

### 1.2. Factory Method (Creacional)
- **Problema**: La ingesta recibe múltiples orígenes y formatos heterogéneos provistos por el cliente (CSV de registros agronómicos de campo, planillas Excel de labores, respuestas JSON de APIs de SAP/AgroWin).
- **Aplicación**: `DatasetParserFactory` que instancia el parser adecuado (`ExcelDatasetParser`, `CsvDatasetParser`, `ErpRestApiParser`) a partir del tipo MIME o metadata del archivo.
- **Beneficio**: Desacopla la lógica de lectura y deserialización del controlador de ingesta.

### 1.3. Observer / Event-Driven (Comportamiento)
- **Problema**: Cuando el cálculo de SPC detecta una violación a las Reglas de Western Electric (un lote que sale de control estadístico en una labor de cosecha o fertilización), múltiples subsistemas deben reaccionar (disparar alerta al panel, registrar incidente en bitácora y notificar al consultor agrónomo).
- **Aplicación**: `SpcDomainEventPublisher` con suscriptores desacoplados (`ConsoleAlertSubscriber`, `AuditLogSubscriber`, `BpmTriggerSubscriber`).
- **Beneficio**: Alta cohesión y bajo acoplamiento entre el motor analítico y los canales de notificación.

### 1.4. Template Method (Comportamiento)
- **Problema**: El flujo de ingesta y validación de datos sigue una serie de pasos invariables (lectura de bytes, validación sintáctica, aplicación de Data Contract, detección de anomalías, persistencia en Lakehouse), pero la verificación de rangos biofísicos varía por tipo de cultivo.
- **Aplicación**: Clase base abstracta `BaseIngestionPipeline` que define el esqueleto del algoritmo y delega `validateBiologicalBounds()` a las subclases especializadas (`AvocadoDataPipeline`, `CoffeeDataPipeline`).

---

## 2. Patrones GRASP

| Patrón | Componente | Justificación |
|---|---|---|
| **Information Expert** | `DataContract` | Posee el conocimiento completo de los esquemas, tipos y rangos agronómicos admisibles; por lo tanto, es el responsable de evaluar si un registro es válido. |
| **Creator** | `SpcAnalysisService` | Dispone de los datos históricos y de las tolerancias requeridas para instanciar objetos de tipo `CartaControlSPC`. |
| **Low Coupling & High Cohesion** | Arquitectura en 3 Capas | Capa de ingesta (C1), curaduría (C2) y modelado (C3) interactúan únicamente mediante interfaces de datos, minimizando dependencias cruzadas. |
| **Protected Variations** | `IDataStorageAdapter` | Protege al núcleo de cálculo estadístico ante cambios en el motor de almacenamiento (migración de DuckDB a Delta Lake / Iceberg). |

---

## 3. Antipatrones Evitados Activamente

1. **God Object**: Se divide estrictamente la gestión de ingesta, cálculo matemático de SPC, modelado predictivo y visualización en módulos independientes.
2. **Hard Coding**: Parámetros agronómicos (grados Brix mínimos, umbrales de humedad, calibres comerciales) se configuran en contratos YAML/JSON versionados, nunca en código fuente.
3. **Data Lock-In**: No se usan formatos binarios cerrados; todos los datos se persisten en estándares abiertos compatibles con cualquier motor SQL (Apache Parquet / Delta Lake).
