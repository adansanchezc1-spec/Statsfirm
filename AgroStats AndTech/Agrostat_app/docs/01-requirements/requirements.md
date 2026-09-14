# Especificación de Requerimientos de Software y Datos (SRS)
**Plataforma**: Agrostat Data Intelligence Platform  
**Entidad**: Agro Stat & Tech Co. (División Agroindustrial de Statsfirm Co.)  
**Versión**: 1.0.0  
**Fecha**: 2026-09-14  
**Fase PDCO**: **PLAN** | **Active Skill**: `01-requirements`  
**Estándares Normativos**: IEEE 830 / ISO 29148, ISO/IEC 25010, DAMA-BOK, SWEBOK Cap. 1  

---

## 1. Definición del Problema y Alcance

### 1.1. ¿Qué problema resuelve?
El sector agroalimentario colombiano sufre de una asimetría estructural de información y alta volatilidad de precios debido a la dispersión de datos entre múltiples entidades gubernamentales, gremiales y climatológicas. Los productores y agroempresas carecen de una plataforma unificada que integre la oferta histórica, la demanda mayorista en centrales de abastos, las cotizaciones de mercado, el balance oferta/consumo y los factores meteorológicos críticos (precipitación, anomalías climáticas ENSO y temperatura) para predecir precios, planificar siembras y gestionar el riesgo bioestadístico.

### 1.2. Solución Propuesta
Construir una arquitectura de ingeniería de datos y data warehousing con Curaduría DAMA-BOK en capas Medallion (Bronze $\rightarrow$ Silver $\rightarrow$ Gold), alimentada por fuentes oficiales colombianas y globales, modelada bajo un esquema dimensional en estrella (Kimball) y respaldada por servicios de dominio hexagonal para pronóstico de series de tiempo y control estadístico de procesos (SPC).

### 1.3. Fuentes de Datos Oficiales Mapeadas

| Fuente | Tipo de Entidad | Variables Principales | Granularidad Nativa | Protocolo / Acceso |
|---|---|---|---|---|
| **DANE (SIPSA_P)** | Precios Mayoristas | Precio mínimo, máximo, promedio por kg, central mayorista | Diaria por producto y mercado | API Socrata (datos.gov.co) / CSV / WSDL SOAP |
| **DANE (SIPSA_A)** | Abastecimiento | Volúmenes de entrada (toneladas), procedencia municipal | Diaria por mercado y municipio de origen | API Socrata / Informes DANE |
| **DANE (SIPSA_I)** | Insumos Agrícolas | Precios de fertilizantes, semillas, plaguicidas | Mensual / Trimestral por casa comercial | Reportes DANE / datos.gov.co |
| **Agronet (MinAgricultura)** | Producción y Área (EVA) | Área sembrada (ha), cosechada (ha), rendimiento (t/ha), producción | Semestral / Anual por municipio | OData / datos.gov.co / Agronet |
| **UPRA** | Planificación y Suelos | Aptitud del suelo rural, zonificación, frontera agrícola | Polígonos geoespaciales / Catastro rural | Geoportal UPRA / Shapefiles / WFS |
| **Gremios (Fedearroz, FENALCE, Fedegan)** | Gremios de Producción | Costos de producción por hectárea, inventarios en silos, cosechas | Mensual / Por ciclo productivo | Boletines gremiales / Informes técnicos |
| **Bolsa Mercantil (BMC)** | Registro Transaccional | Facturas registradas, precios reales de transacción, volumen negociado | Diaria por rueda de negocios | Boletines bursátiles / Registro BMC |
| **IDEAM (DHIME / Datos Abiertos)** *(Nueva Fuente)* | Climatología y Meteorología | Precipitación diaria (mm), temperatura máx/mín/media (°C), humedad relativa (%) | Diaria / Horaria por estación meteorológica | Portal DHIME / API OData datos.gov.co |
| **NASA POWER / CHIRPS** *(Nueva Fuente)* | Reanálisis Agroclimático Satelital | Radiación solar (MJ/m²), déficit de presión de vapor (VPD), evapotranspiración | Grilla satelital 0.5° $\times$ 0.5° diaria | API REST NASA POWER (JSON/CSV) |
| **FAO & USDA** | Contexto Internacional | Balances mundiales de cereales, precios FOB, índice FAO de alimentos | Mensual por país y bloque comercial | FAOSTAT API / USDA PSD Online |

---

## 2. Mapa de Stakeholders

| Rol | Interés Principal | Nivel de Influencia | Expectativa de Consumo |
|---|---|---|---|
| **Productor Agropecuario** | Decidir ventana de cosecha y precio de venta justo | Alto | Alertas de precio y clima en tiempo real |
| **Agroexportador & Comercializador** | Previsión de oferta, abastecimiento y calidad | Alto | Dashboards de demanda y pronóstico estocástico |
| **Gremios de la Producción** | Monitoreo de competitividad y costos de insumos | Medio | Análisis comparativo de márgenes e inventarios |
| **Analista de Riesgo / Crédito (Finagro/Bancos)** | Evaluar viabilidad financiera y climática del cultivo | Alto | Modelos de scoring de riesgo y tendencias |
| **Ingeniero / Científico de Datos** | Automatizar ingesta, asegurar calidad DAMA y entrenar modelos | Alto | Esquema SQL dimensional y APIs REST/gRPC |

---

## 3. Requerimientos Funcionales (RF)

### Módulo 1: Ingesta y Conectores de Datos (Bronze Layer)
- **RF-001**: El sistema debe conectarse a la API de Datos Abiertos de Colombia (`datos.gov.co` vía Socrata/OData) para extraer diariamente los boletines mayoristas de precios del DANE (SIPSA).
- **RF-002**: El sistema debe ingestar los volúmenes de abastecimiento de alimentos por mercado y municipio de origen de SIPSA_A.
- **RF-003**: El sistema debe extraer los registros de Evaluaciones Agropecuarias Municipales (EVA de Agronet) por ciclo agrícola y municipio.
- **RF-004**: El sistema debe conectarse al portal del IDEAM / NASA POWER para capturar series temporales de precipitación, temperatura y radiación solar por estación y municipio.
- **RF-005**: El sistema debe almacenar cada lote de extracción crudo en la capa Bronze en formato inmutable (JSONL / Parquet con timestamp y firma SHA-256 de auditoría).

### Módulo 2: Curaduría y Calidad del Dato (Silver Layer - DAMA-BOK)
- **RF-006**: El sistema debe validar la **completitud** del dataset asegurando que campos obligatorios (fecha, código DIVIPOLA municipio, código CPC producto, central mayorista, precio o volumen) no sean nulos.
- **RF-007**: El sistema debe validar la **validez de rangos** (precios > 0, volúmenes $\ge$ 0, grados Brix 0-32, pH 3.5-9.0, precipitaciones $\ge$ 0 mm).
- **RF-008**: El sistema debe validar la **consistencia** (ej. kilos exportables $\le$ kilos totales, precio mínimo $\le$ precio promedio $\le$ precio máximo).
- **RF-009**: El sistema debe validar la **unicidad** mediante clave compuesta natural (`fecha + mercado_id + producto_id + variedad_id`).
- **RF-010**: El sistema debe enrutar automáticamente cualquier registro anómalo hacia la cola de descarte *Dead Letter Queue* (DLQ) con diagnóstico del motivo del rechazo.

### Módulo 3: Almacenamiento Dimensional y Series Temporales (Gold Layer - Data Warehouse SQL)
- **RF-011**: El sistema debe poblar un esquema dimensional en estrella (Kimball Star Schema) con dimensiones canónicas (`dim_tiempo`, `dim_geografia_divipola`, `dim_producto_cpc`, `dim_mercado_abasto`, `dim_estacion_clima`, `dim_actor_cadena`).
- **RF-012**: El sistema debe registrar las métricas transaccionales en tablas de hechos (`fact_precios_sipsa`, `fact_abastecimiento_sipsa`, `fact_produccion_agronet`, `fact_clima_diario`).
- **RF-013**: El sistema debe mantener vistas materializadas analíticas con agregaciones a diferentes niveles de granularidad (diario, semanal, mensual, trimestral y anual).

### Módulo 4: Analítica Avanzada, Demanda y Bioestadística
- **RF-014**: El sistema debe generar series de tiempo de demanda agregada y calcular bandas de control estadístico Shewhart ($\bar{X} \pm 3\sigma$) auditando las Reglas de Nelson (1 a 4).
- **RF-015**: El sistema debe permitir entrenar y versionar modelos de machine learning para predicción de precios mayoristas y rendimiento agrícola con intervalos de confianza del 95%.

---

## 4. Requerimientos No Funcionales (RNF) — ISO/IEC 25010

| ID | Característica | Métrica / Criterio de Aceptación |
|---|---|---|
| **RNF-001** | Rendimiento (Performance) | Ingesta y validación de 100,000 registros en < 30 segundos. |
| **RNF-002** | Latencia de Consulta SQL | Consultas analíticas sobre series temporales de 5 años en < 200 ms con índices btree/brin. |
| **RNF-003** | Calidad del Dato (DAMA-BOK) | Tasa de completitud $\ge 98\%$, consistencia $\ge 99.5\%$ en la capa Silver. |
| **RNF-004** | Portabilidad del Motor SQL | DDL 100% compatible con estándar ANSI SQL (ejecutable en PostgreSQL y DuckDB sin modificación de sintaxis base). |
| **RNF-005** | Disponibilidad y Tolerancia a Fallos | Reintentos automáticos con backoff exponencial ante fallos de APIs externas (DANE/IDEAM). |
| **RNF-006** | Auditabilidad y Trazabilidad | Registro transaccional de fecha de ingestión, fuente, hash de archivo y auditor en cada tabla de hechos. |
| **RNF-007** | Modularidad Arquitectónica | Cero acoplamiento entre la capa de dominio/reglas de negocio y el motor de base de datos relacional (Arquitectura Hexagonal). |
| **RNF-008** | Estándar de Código | 100% cumplimiento de PEP 8 en Python y guías SQL Style Guide. |

---

## 5. Restricciones del Sistema (R)

- **R-001**: Uso de códigos oficiales **DIVIPOLA** (DANE) para departamentos y municipios de Colombia.
- **R-002**: Uso de la **Clasificación Central de Productos (CPC Versión 2.1 A.C.)** adaptada para Colombia.
- **R-003**: Cero dependencia de sensores propietarios o venta de hardware (enfoque en analítica y curaduría de datos ya existentes).
- **R-004**: Base de datos SQL compatible con **PostgreSQL 14+** y **DuckDB 0.9+**.
- **R-005**: Manejo nativo de zonas horarias en `America/Bogota` (UTC-5).

---

## 6. Glosario del Dominio Agrícola y de Datos

- **DIVIPOLA**: Codificación de la División Político-Administrativa de Colombia emitida por el DANE (ej. 11001 = Bogotá, D.C.).
- **SIPSA**: Sistema de Información de Precios y Abastecimiento del Sector Agropecuario (DANE).
- **EVA**: Evaluaciones Agropecuarias Municipales coordinadas por Agronet y UPRA.
- **Central de Abastos**: Mercado mayorista de concentración de alimentos (ej. Corabastos, Cavasa).
- **Capa Bronze**: Repositorio inmutable de datos en crudo (*Raw Data*).
- **Capa Silver**: Datos curados, tipados, validados y libres de anomalías (*Cleaned Data*).
- **Capa Gold**: Modelo dimensional en estrella para consultas analíticas y BI (*Data Mart*).
- **SPC (Statistical Process Control)**: Control estadístico de calidad basado en límites Shewhart y Reglas de Nelson.
- **ENSO**: El Niño-Southern Oscillation (ciclos climáticos El Niño / La Niña con impacto hidrológico en cultivos).
