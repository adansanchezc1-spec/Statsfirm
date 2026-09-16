# Catálogo de Patrones de Diseño de Software y Datos
**Plataforma**: Agrostat Data Intelligence Platform  
**Entidad**: Agro Stat & Tech Co. (División Agroindustrial de Statsfirm Co.)  
**Versión**: 1.0.0  
**Fecha**: 2026-09-14  
**Fase PDCO**: **PLAN → DEVELOPMENT**  
**Active Skill**: `02-architecture`  
**Estándares**: SWEBOK Cap. 2, GoF (Gang of Four), Craig Larman GRASP  

---

## 1. Patrones GoF (Gang of Four) Aplicados

### 1.1. Patrones Creacionales

#### 1.1.1. Factory Method (Método de Fábrica)
- **Problema que resuelve**: La plataforma extrae datos de fuentes con protocolos muy heterogéneos (Socrata Open Data para SIPSA DANE, OData REST para DHIME IDEAM, REST JSON para NASA POWER, y archivos planos para gremios). El código del pipeline no debe conocer los detalles concretos de cada conector de red.
- **Componente**: `SourceExtractorFactory` y clases abstractas `BaseSourceExtractor`.
- **Implementación**:
  ```python
  class SourceExtractorFactory:
      @staticmethod
      def create_extractor(source_type: SourceType, config: AppConfig) -> BaseSourceExtractor:
          if source_type == SourceType.SIPSA_PRECIOS:
              return SocrataSipsaPreciosExtractor(config)
          elif source_type == SourceType.SIPSA_ABASTECIMIENTO:
              return SocrataSipsaAbastecimientoExtractor(config)
          elif source_type == SourceType.IDEAM_CLIMA:
              return IdeamODataExtractor(config)
          elif source_type == SourceType.NASA_POWER:
              return NasaPowerRestExtractor(config)
          raise UnsupportedSourceError(f"Fuente no soportada: {source_type}")
  ```

#### 1.1.2. Builder (Constructor)
- **Problema que resuelve**: La construcción de consultas analíticas multidimensionales complejas sobre el Data Warehouse en DuckDB (filtrado por ventanas temporales, múltiples códigos DIVIPOLA de origen, selecciones CPC de producto y métricas bioestadísticas) requiere pasos de configuración estructurados evitando parámetros telescópicos.
- **Componente**: `DimensionalQueryBuilder`.
- **Beneficio**: Garantiza que las cláusulas SQL se construyan de forma segura y parametrizada, previniendo inyecciones SQL y validando la semántica de la consulta antes de la ejecución.

#### 1.1.3. Singleton (Instancia Única Controlada)
- **Problema que resuelve**: Mantener múltiples conexiones de escritura simultáneas sobre un archivo DuckDB local puede provocar bloqueos de archivo (*file lock contention*). Se requiere un gestor único de conexión y de pool de lectura/escritura gestionado por el contenedor de inyección.
- **Componente**: `DuckDBConnectionManager` en `container.py`.

---

### 1.2. Patrones Estructurales

#### 1.2.1. Adapter (Adaptador / Wrapper)
- **Problema que resuelve**: Los esquemas JSON brutos devueltos por `datos.gov.co` (campos con mayúsculas y acentos como `"Nombre_Municipio"`, `"Precio_Promedio"`) son incompatibles con el modelo de entidades canónicas de dominio de Agrostat.
- **Componente**: `SocrataRecordToDomainAdapter`, `IdeamObservationAdapter`.
- **Implementación**: Adapta la estructura externa a las entidades y Value Objects inmutables del dominio, normalizando tipos, codificaciones DIVIPOLA y marcas de tiempo UTC-5.

#### 1.2.2. Repository (Repositorio de Persistencia)
- **Problema que resuelve**: Aislar los detalles de persistencia física (archivos Parquet en capas Bronze/Silver y tablas DuckDB en capa Gold) de las reglas de negocio de los casos de uso.
- **Componente**: `LakehouseRepositoryPort` (interfaz) implementado por `DuckDBLakehouseRepository`.
- **Beneficio**: Los casos de uso operan con métodos semánticos (`save_bronze_batch`, `load_silver_records`, `query_market_time_series`, `upsert_gold_fact`) sin saber si los datos residen en un archivo local o en la nube.

#### 1.2.3. Facade (Fachada)
- **Problema que resuelve**: El proceso completo de actualización diaria (*End-to-End Daily Pipeline*) involucra múltiples subsistemas: extracción de varias fuentes, validación DAMA-BOK, registro en DLQ, persistencia en DuckDB, cálculo de límites Shewhart y reentrenamiento de modelos de pronóstico.
- **Componente**: `AgrostatPipelineFacade` (o caso de uso `ExecuteEndToEndPipelineUseCase`).
- **Beneficio**: Proporciona una interfaz simplificada y unificada para disparar la ejecución desde el CLI o el planificador CRON con una sola invocación.

---

### 1.3. Patrones de Comportamiento

#### 1.3.1. Chain of Responsibility (Cadena de Responsabilidad)
- **Problema que resuelve**: La curaduría DAMA-BOK requiere una secuencia de validaciones independientes y ordenadas. Si una regla crítica de completitud falla, se documenta y se deriva; si pasa, se evalúan reglas de consistencia cruzada y finalmente de unicidad.
- **Componente**: `DataQualityValidationChain`:
  1. `CompletenessRuleValidator` (Verifica nulos en claves obligatorias).
  2. `ValueRangeRuleValidator` (Verifica precios > 0, volúmenes $\ge$ 0, pH, precipitación).
  3. `CrossFieldConsistencyValidator` (Verifica coherencia: $P_{min} \le P_{prom} \le P_{max}$).
  4. `NaturalKeyUniquenessValidator` (Verifica duplicados por fecha, mercado y producto).
- **Beneficio**: Cada validador es una clase pequeña, testeable de forma aislada y desacoplada de las demás.

#### 1.3.2. Strategy (Estrategia)
- **Problema que resuelve**: El motor de pronóstico de series de tiempo de demanda y precios debe soportar diferentes algoritmos según el horizonte temporal y la densidad de datos disponibles:
  - Horizonte corto (1-4 semanas): Modelo autorregresivo (ARIMA / SARIMAX con covariables climáticas).
  - Horizonte medio (5-12 semanas): Modelo de aprendizaje automático (Random Forest / Gradient Boosting con lags).
  - Detección de tendencias estacionales: Suavizamiento exponencial Holt-Winters.
- **Componente**: `ForecastingStrategy` (interfaz) con implementaciones `SarimaxForecastingStrategy`, `GradientBoostingForecastingStrategy` y `HoltWintersStrategy`.

#### 1.3.3. Observer (Observador / Notificador de Eventos)
- **Problema que resuelve**: Cuando el motor bioestadístico detecta una violación de las Reglas de Nelson (ej. 1 punto fuera de $3\sigma$ o 9 puntos consecutivos del mismo lado de la media), o la tasa de rechazo DLQ supera el umbral del 5%, el sistema debe notificar a los suscriptores (consola, logs de auditoría, o alertas webhook).
- **Componente**: `DomainEventDispatcher` y `SPCAnomalyObserver`.

---

## 2. Patrones GRASP (General Responsibility Assignment Software Patterns)

| Patrón GRASP | Responsabilidad Asignada en Agrostat Platform | Componente Concreto |
|---|---|---|
| **Information Expert** | Asignar la responsabilidad al objeto que posee los datos requeridos para realizar el cálculo. | La entidad `SerieTiempoDemanda` calcula sus propias medidas de tendencia central y dispersión ($IQR$, desviación estándar). |
| **Creator** | Asignar la creación de una instancia a la clase que la agrega, contiene o registra estrechamente. | El validador `DataQualityValidator` es el creador de las instancias `DataQualityReport` y `QuarantineRecord`. |
| **Controller** | Asignar el manejo de peticiones externas a un coordinador que no ejecute lógica de negocio directa. | `IngestionController` en la capa de adaptadores recibe la petición HTTP o comando CLI y la delega a `RunDailyIngestionUseCase`. |
| **Low Coupling** | Minimizar las dependencias entre componentes para facilitar el mantenimiento y la evolución. | El motor de cálculo `BioStatisticalEngine` no conoce la base de datos DuckDB ni las librerías de visualización; opera solo con tipos primitivos y Value Objects. |
| **High Cohesion** | Mantener las responsabilidades de cada módulo estrechamente focalizadas y comprensibles. | Cada caso de uso en `application/use_cases/` implementa exclusivamente un único flujo de negocio de la plataforma. |
| **Polymorphism** | Asignar responsabilidades de comportamiento variable mediante interfaces polimórficas en lugar de condicionales `if/else` extensos. | El puerto `ExternalSourceExtractorPort` permite invocar `.extract_records()` de manera polimórfica sin importar la fuente. |
| **Pure Fabrication** | Crear clases conceptuales que no corresponden directamente a entidades del dominio del problema para mantener la cohesión y el bajo acoplamiento. | `DuckDBConnectionManager`, `DataQualityAuditLogger` y `ModelMetricsTracker`. |
| **Indirection** | Asignar la responsabilidad a un intermediario para evitar el acoplamiento directo entre dos o más componentes. | Los puertos de salida (`ports/out_*.py`) desacoplan los casos de uso de las tecnologías de persistencia física e I/O. |
| **Protected Variations** | Diseñar puntos de inestabilidad identificados para que los cambios en ellos no afecten al resto del sistema. | La especificación formal de esquemas SQL en la capa Gold protege los dashboards de BI ante cambios de formato en las fuentes gubernamentales externas. |
