# Casos de Uso por Entidad y Proceso
**Plataforma**: Agrostat Data Intelligence Platform  
**Fase PDCO**: **PLAN** | **Active Skill**: `01-requirements`  
**Estándar**: IEEE 830 / ISO 29148  

---

## 1. Mapeo de Actores

- **Ingeniero de Datos (Pipeline Orchestrator)**: Configura pipelines de extracción, ingestión y validación de fuentes oficiales.
- **Analista de Mercados Agrícolas**: Consulta precios, tendencias de oferta/demanda y estacionalidad.
- **Productor / Agroexportador**: Consume previsiones de demanda, análisis de volatilidad y alertas climatológicas.
- **Auditor de Calidad del Dato (Data Steward)**: Monitorea tasas de completitud, consistencia y registros en cuarentena (DLQ).
- **Motor Estadístico / ML Engine**: Consume datos limpios de la capa Gold para entrenar modelos predictivos.

---

## 2. Casos de Uso por Entidad

### Entidad: `BoletinSIPSA` (Precios y Abastecimiento)

#### UC-001: Ingesta y Validación de Precios Mayoristas Diarios
- **Actor Principal**: Pipeline Orchestrator (Sistema Autónomo).
- **Precondición**: El DANE ha publicado el boletín SIPSA_P diario en `datos.gov.co` o archivo plano.
- **Flujo Principal**:
  1. El orquestador extrae los registros de la API del DANE para la fecha solicitada.
  2. Almacena el payload bruto en la capa Bronze con timestamp y hash SHA-256.
  3. Invoca el servicio de dominio `DataQualityValidator`.
  4. Valida completitud de producto (código CPC), mercado mayorista, precio mínimo, medio y máximo.
  5. Valida consistencia lógica ($precio_{min} \le precio_{medio} \le precio_{max}$).
  6. Las filas válidas se transforman en entidades de dominio `MercadoPrecio` y se persisten en la capa Silver.
  7. El orquestador inserta los hechos en `fact_precios_sipsa` de la base de datos SQL.
- **Flujo Alternativo (FA-1)**: Si un producto tiene precios negativos o nulos:
  - Se aísla el registro, se adjunta el diagnóstico de error y se envía a la tabla/archivo DLQ.
  - El sistema emite una alerta de calidad al Data Steward y continúa con el resto del lote.
- **Postcondición**: Precios normalizados disponibles para analítica en la base de datos SQL.

---

### Entidad: `AbastecimientoMercado` (Flujos de Entrada de Alimentos)

#### UC-002: Ingesta y Georreferenciación de Flujos de Abastecimiento
- **Actor Principal**: Pipeline Orchestrator.
- **Precondición**: Datos de SIPSA_A disponibles en el portal oficial.
- **Flujo Principal**:
  1. El sistema extrae los volúmenes en toneladas que ingresan a cada central de abastos.
  2. Valida la correspondencia geográfica del municipio de procedencia con la tabla DIVIPOLA.
  3. Transforma los volúmenes a kilogramos estándar y calcula el porcentaje de participación del municipio de origen.
  4. Persiste los datos en `fact_abastecimiento_sipsa` vinculando las dimensiones geográficas y de producto.
- **Postcondición**: Matriz origen-destino de alimentos disponible para análisis de consumo y logística agroalimentaria.

---

### Entidad: `ProduccionMunicipalEVA` (Oferta Agrícola Agronet)

#### UC-003: Curaduría y Carga de Evaluaciones Agropecuarias Municipales
- **Actor Principal**: Data Engineer / Analista Agronómico.
- **Precondición**: Datos semestrales o anuales de Agronet/UPRA disponibles.
- **Flujo Principal**:
  1. El sistema extrae los registros de área sembrada, cosechada y rendimiento.
  2. Valida la regla de negocio: $Área\ Cosechada \le Área\ Sembrada$.
  3. Valida que el rendimiento ($t/ha$) esté dentro de los límites biológicos aceptables de la especie (ej. Plátano 5-30 t/ha, Papa 10-45 t/ha).
  4. Persiste en `fact_produccion_agronet` para correlación histórica de oferta.
- **Postcondición**: Línea base de oferta municipal registrada en el Data Warehouse.

---

### Entidad: `ClimatologiaEstacion` (Variables Ambientales IDEAM / NASA)

#### UC-004: Ingesta y Correlación de Variables Meteorológicas
- **Actor Principal**: Pipeline Orchestrator.
- **Precondición**: Acceso a estaciones hidrometeorológicas del IDEAM o grilla NASA POWER.
- **Flujo Principal**:
  1. El sistema consulta las series de precipitación (mm), temperatura (°C) y humedad relativa (%) para cada estación y municipio.
  2. Imputa valores faltantes utilizando el promedio móvil ponderado de estaciones vecinas o reanálisis satelital.
  3. Registra las métricas en `fact_clima_diario`.
  4. Calcula anomalías de precipitación respecto a la media histórica del mes (indicador de sequía o inundación).
- **Postcondición**: Indicadores climáticos alineados temporalmente con los precios y volúmenes de cosecha.

---

### Entidad: `SerieDemanda` (Analítica Predictiva y SPC)

#### UC-005: Modelado de Series de Tiempo y Pronóstico de Demanda
- **Actor Principal**: Analista de Mercados / Algoritmo Predictivo.
- **Precondición**: Mínimo 24 periodos históricos en `fact_abastecimiento_sipsa` y `fact_precios_sipsa`.
- **Flujo Principal**:
  1. El analista selecciona el producto y la central mayorista objetivo.
  2. El sistema extrae la serie temporal diaria y la agrega a nivel semanal o mensual.
  3. Descompone la serie en tendencia, estacionalidad y componente estocástico.
  4. Genera el pronóstico a $H$ semanas con bandas de confianza al 95%.
  5. Computa los límites de control estadístico Shewhart e identifica si el mercado se encuentra en estabilidad o con quiebre estructural (Reglas de Nelson).
- **Postcondición**: Predicción de demanda y alerta temprana de desabastecimiento o sobreoferta emitida.
