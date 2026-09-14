# Especificación de Requerimientos de Software (SRS)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: PLAN  
**SDLC Stage**: Requirements  
**Estándar**: IEEE 830 / ISO 29148 / DAMA-BOK  

---

## 1. Introducción y Propósito del Sistema

### 1.1. Propósito
El presente documento especifica los requerimientos de la plataforma analítica de **Agro Stat & Tech Co.** El sistema tiene como objetivo principal la **ingesta, estandarización, validación biofísica, análisis bioestadístico y optimización de procesos agropecuarios** a partir de datasets y registros provistos directamente por productores, asociaciones y agroexportadoras.

### 1.2. Alcance y Exclusión Explícita de Hardware
- **Dentro del Alcance**: Ingesta multicanal de archivos planos (CSV, Excel), APIs REST de ERPs agronómicos (SAP, AgroWin, Odoo), cuadernos de campo digitalizados, análisis de laboratorio físico-químico, evaluación de calidad según DAMA-BOK, cálculo de cartas de control estadístico (Shewhart), análisis de varianza (ANOVA), modelos predictivos de cosecha (*Yield AI*) y diagramación/rediseño de procesos en BPMN.
- **Fuera del Alcance (Exclusión Crítica)**: Queda explícitamente excluido el desarrollo, comercialización, aprovisionamiento, instalación o mantenimiento de sensores físicos de suelo/clima, redes de telemetría por hardware (LoRaWAN/gateways dedicados) y mecanismos de captura física directa en campo.

---

## 2. Requerimientos Funcionales (RF)

| ID | Descripción | Prioridad | Entidad Principal | Casos de Uso |
|---|---|---|---|---|
| **RF-001** | El sistema debe permitir la carga e ingesta de datasets en formatos CSV, XLSX, JSON y conexión directa SQL/API a ERPs agrícolas. | Alta | `DatasetAgropecuario` | UC-001 |
| **RF-002** | El sistema debe validar los datos entrantes contra **Data Contracts** estrictos, verificando tipos de datos, rangos biológicos admisibles y consistencia temporal. | Alta | `DataContract` | UC-001 |
| **RF-003** | El sistema debe aislar en una cola de error (*Dead Letter Queue - DLQ*) aquellos registros que contengan inconsistencias o valores fuera de especificación biológica, sin interrumpir el lote analítico. | Alta | `RegistroAnomalo` | UC-001 |
| **RF-004** | El sistema debe calcular cartas de control estadístico de procesos (SPC) tipo $\bar{X}-R$, $\bar{X}-S$ e individuales ($I-MR$) sobre variables clave agronómicas y de cosecha en campo. | Alta | `CartaControlSPC` | UC-002 |
| **RF-005** | El sistema debe calcular índices de capacidad de proceso ($C_p$, $C_{pk}$, $P_p$, $P_{pk}$) para parámetros de exportación (grados Brix, calibres, peso, firmeza). | Alta | `IndiceCapacidad` | UC-002 |
| **RF-006** | El sistema debe identificar causas especiales de variación aplicando las Reglas de Western Electric (puntos fuera de $3\sigma$, tendencias de 7 puntos consecutivos, oscilaciones sistemáticas). | Media | `AlertaSPC` | UC-002 |
| **RF-007** | El sistema debe ejecutar análisis de varianza (ANOVA) y regresiones multivariadas para correlacionar factores de manejo histórico con rendimiento por hectárea. | Media | `ModeloBioestadistico` | UC-003 |
| **RF-008** | El sistema debe generar pronósticos de cosecha y curvas de maduración (*Yield AI*) basados en datos climáticos históricos y registros fenológicos del productor. | Media | `PronosticoCosecha` | UC-003 |
| **RF-009** | El sistema debe emitir reportes de diagnóstico de procesos y oportunidades de mejora modeladas bajo estándar BPMN 2.0. | Media | `DiagnosticoBPMN` | UC-004 |
| **RF-010** | El sistema debe exportar reportes auditables de trazabilidad y linaje de datos para certificación internacional (GlobalG.A.P., EUDR libre de deforestación). | Alta | `ReporteTrazabilidad` | UC-004 |

---

## 3. Requerimientos No Funcionales (RNF)

| ID | Dimensión (ISO 25010) | Descripción | Métrica / Criterio |
|---|---|---|---|
| **RNF-001** | **Rendimiento** | El motor bioestadístico debe procesar un dataset de 1.000.000 de registros y generar cartas SPC en menos de 5 segundos. | Tiempo de ejecución < 5.0 s (P95) |
| **RNF-002** | **Calidad del Dato** | Cumplimiento estricto de las 6 dimensiones de calidad de DAMA-BOK (Completitud, Unicidad, Validez, Precisión, Consistencia, Integridad). | Tasa de error en ingesta < 0.01% tras validación |
| **RNF-003** | **Seguridad** | Aislamiento lógico estricto multi-inquilino (*multi-tenant*) y cifrado de datos en reposo y en tránsito. | Cifrado AES-256 en reposo, TLS 1.3 en tránsito |
| **RNF-004** | **Disponibilidad** | Disponibilidad continua de la plataforma SaaS para consulta gerencial y carga de planillas. | SLA 99.9% Uptime mensual |
| **RNF-005** | **Soberanía del Dato** | Garantía de *Zero Data Lock-In*: exportación de datos crudos y procesados en formatos abiertos (Parquet, CSV, GeoJSON). | 100% de datasets exportables bajo demanda |
| **RNF-006** | **Portabilidad** | Despliegue agnóstico a la nube mediante contenedores OCI (Docker / Kubernetes). | 100% cloud-native portátil |

---

## 4. Restricciones del Sistema

| ID | Restricción |
|---|---|
| **R-001** | Ningún módulo del sistema debe requerir drivers de hardware de campo, gateways LoRaWAN ni firmware embebido. |
| **R-002** | La ingesta debe funcionar exclusivamente sobre protocolos web estándar (HTTPS REST, SFTP, SQL) o subida directa de archivos por el usuario. |
| **R-003** | Stack tecnológico backend recomendado: Python 3.11+ (Polars, SciPy, Statsmodels, DuckDB, FastAPI). |
