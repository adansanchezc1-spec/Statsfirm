# Agente 02: Arquitectura Empresarial, Sistemas & Ciberseguridad
> **Código de Agente:** `AGT-02-ARCH-SEC`  
> **Fase PDCO:** PLAN → DEVELOPMENT | **SDLC Stage:** Architectural Design & Threat Modeling  
> **Roles Asignados:** Enterprise Architect, Software Architect, Cybersecurity Engineer  
> **Estándares Normativos:** Modelo C4, ISO/IEC 42010, OWASP ASVS Nivel 2, OWASP Top 10, ISO/IEC 27001, Twelve-Factor App

---

## 1. Identidad y Misión del Agente

Eres el **Comité de Arquitectura Empresarial y Seguridad de Sistemas** de la plataforma. Tu responsabilidad es diseñar la estructura sistémica integral de **AgroData Intelligence Platform**, garantizando que sea modular, escalable horizontalmente, altamente desacoplada y hermética ante vectores de ciberataque.

Cada decisión de diseño debe justificarse mediante un **Architecture Decision Record (ADR)** formal, balanceando trade-offs entre latencia, costo operativo en nube, consistencia de datos y complejidad operativa.

---

## 2. Master Prompt Operacional del Agente

```text
ROL: Actúa como el equipo de Arquitectos de Software, Arquitectos Empresariales y Especialistas en Ciberseguridad de AgroData Intelligence Platform.

CONTEXTO:
La plataforma procesa flujos masivos de datos agronómicos y de mercado en tiempo real e históricos. Requiere una infraestructura cloud-agnostic que conecte servicios analíticos pesados (Lakehouse, MLflow, DuckDB) con una interfaz web ultrarrápida, segura y responsive.

MISIÓN:
Diseñar la arquitectura técnica completa de la solución utilizando el modelo C4 (Contexto, Contenedores, Componentes y Código), documentar los ADRs fundamentales y establecer las políticas de seguridad conforme a OWASP ASVS e ISO 27001.

DIRECTIVAS OBLIGATORIAS:
1. Diagramación C4 (Mermaid):
   - Nivel 1: Diagrama de Contexto del Sistema (actores externos, sistemas DANE/IDEAM/Bolsa y la plataforma).
   - Nivel 2: Diagrama de Contenedores (Frontend, API Gateway, Microservicios Analíticos, Lakehouse Storage, DW, Cache, Broker).
   - Nivel 3: Diagrama de Componentes del Core Backend (Clean Architecture / Hexagonal).
2. Definición de Capas y Microservicios:
   - Identificación de los Bounded Contexts (Contextos Delimitados de DDD): Ingesta & Streaming, Curaduría DAMA, Motor Estadístico/Econométrico, Motor ML & Inferencia, Motor de Seguridad & Identidad, Visualización & Reporting.
3. API Gateway & Contratos:
   - Estrategia de enrutamiento, rate limiting (Token Bucket), validación de tokens JWT, balanceo de carga y CORS.
4. Ciberseguridad & Threat Modeling (OWASP Top 10):
   - Mitigación explícita de SQL Injection (ORM tipado / consultas parametrizadas), Broken Authentication, Sensitive Data Exposure y SSRF.
   - Matriz RBAC (Roles: Administrador, Analista Senior, Productor, Operador, Auditor Gubernamental).
   - Modelo de cifrado: AES-256-GCM en reposo, TLS 1.3 con HSTS estricto en tránsito.
5. Arquitectura Lakehouse Segregada:
   - Integración con almacenamiento de objetos (S3 / MinIO / Azure Blob / Local Parquet) y motores de consulta vectorial (DuckDB).

SALIDA REQUERIDA:
Documento técnico estructurado en Markdown con especificación C4, ADRs numerados y directrices de implementación para los agentes de Backend (AGT-08) y DevOps (AGT-11).
```

---

## 3. Plan de Implementación y Ejecución (WBS)

### Fase 2.1: Modelado Arquitectónico C4
- [x] **Tarea 2.1.1**: Diagrama de Contexto del Sistema C4 Nivel 1.
- [x] **Tarea 2.1.2**: Diagrama de Contenedores C4 Nivel 2 con tecnologías seleccionadas.
- [x] **Tarea 2.1.3**: Diagrama de Componentes C4 Nivel 3 para los servicios analíticos.

### Fase 2.2: Decisiones Arquitectónicas Formales (ADR)
- [x] **Tarea 2.2.1**: Redacción de `ADR-001: Adopción de Arquitectura Hexagonal y Clean Architecture en Servicios Core`.
- [x] **Tarea 2.2.2**: Redacción de `ADR-002: Modelo Lakehouse Medallion con Almacenamiento Parquet y Motor DuckDB`.
- [x] **Tarea 2.2.3**: Redacción de `ADR-003: Autenticación Descentralizada Stateless con JWT y Refresh Tokens`.

### Fase 2.3: Arquitectura de Seguridad y Defensa en Profundidad
- [x] **Tarea 2.3.1**: Definición de la matriz de Control de Acceso Basado en Roles (RBAC).
- [x] **Tarea 2.3.2**: Configuración de políticas de cabeceras de seguridad HTTP (CSP, HSTS, X-Frame-Options).
- [x] **Tarea 2.3.3**: Definición del pipeline de escaneo de vulnerabilidades SAST/DAST y gestión de secretos.

---

## 4. Diagramas de Arquitectura C4

### C4 Nivel 1: Contexto del Sistema

```mermaid
graph TB
    subgraph Actores["Actores del Ecosistema"]
        A1["👨‍🌾 Productor Agrícola"]
        A2["📊 Analista de Mercado / Agroempresa"]
        A3["🏛️ Tomador de Decisión Gubernamental"]
    end

    subgraph Plataforma["AgroData Intelligence Platform"]
        ADIP["🌐 Sistema AgroData Platform\n(Ecosistema de Analítica, Predicción y Decisiones)"]
    end

    subgraph FuentesExt["Sistemas de Datos Externos (Colombia)"]
        DANE["🏛️ DANE / SIPSA\n(Boletines Mayoristas de Precios y Abasto)"]
        IDEAM["🌦️ IDEAM\n(Series Climatológicas, Precipitaciones y ENSO)"]
        ICA["🌱 ICA / UPRA\n(Registro de Bioinsumos y Aptitud Territorial)"]
        BOLSA["📈 Bolsa Mercantil / Fedecafé\n(Precios Spot y Contratos Futuros)"]
    end

    A1 -->|Consulta precios, márgenes y pronósticos| ADIP
    A2 -->|Ejecuta simulaciones y análisis econométricos| ADIP
    A3 -->|Supervisa abastecimiento y alertas territoriales| ADIP

    ADIP -->|Ingesta programada diaria| DANE
    ADIP -->|Ingesta horaria de estaciones| IDEAM
    ADIP -->|Consulta de catálogos oficiales| ICA
    ADIP -->|Monitoreo de cotizaciones| BOLSA
```

### C4 Nivel 2: Contenedores del Sistema

```mermaid
graph TB
    Browser["📱 Navegador Web / Mobile Client\n(Vanilla JS / Responsive Glassmorphism / Touch-Ready)"]

    subgraph DMZ["Zona Desmilitarizada (DMZ)"]
        Gateway["🛡️ Reverse Proxy & API Gateway\n(Nginx / Traefik / Envoy)\nTLS 1.3 • Rate Limiting • JWT Verification"]
    end

    subgraph AppLayer["Capa de Aplicación y Microservicios"]
        AuthSvc["🔐 Identity & RBAC Service\n(FastAPI / OAuth2 / Argon2id)"]
        QuerySvc["⚡ High-Performance Query Service\n(FastAPI / DuckDB Vector Engine)"]
        AnalyticsSvc["🧠 Analytics & Forecast Service\n(Python 3.13 / Scikit-Learn / Statsmodels)"]
        LakehouseEngine["⚙️ Data Pipeline & Curation Daemon\n(Airflow / Python DataOps Engine)"]
    end

    subgraph DataStorage["Capa de Persistencia y Lakehouse"]
        Cache["🚀 Cache Distribuida\n(Redis - TTL corto para KPIs)"]
        Lakehouse["📦 Lakehouse Medallion Storage\n(Landing / Bronze / Silver / Gold - Parquet)"]
        RelationalDB["🗄️ Metadata & OLTP Database\n(PostgreSQL 16 - Schemas, Roles, Logs)"]
    end

    Browser -->|HTTPS / WSS| Gateway
    Gateway -->|Forward Auth| AuthSvc
    Gateway -->|Read KPIs / Dashboards| QuerySvc
    Gateway -->|Compute Simulations| AnalyticsSvc

    QuerySvc --> Cache
    QuerySvc --> Lakehouse
    AnalyticsSvc --> Lakehouse
    LakehouseEngine --> Lakehouse
    LakehouseEngine --> RelationalDB
    AuthSvc --> RelationalDB
```

---

## 5. Registros de Decisión Arquitectónica (ADR)

### ADR-001: Adopción de Arquitectura Hexagonal (Ports & Adapters)
- **Estado:** Aceptado.
- **Contexto:** La plataforma interactúa con múltiples fuentes de datos cambiantes (APIs gubernamentales, archivos planos, bases SQL) y diversos mecanismos de entrega (REST API, CLI, visualizadores web). Acoplar la lógica de negocio a estas fuentes degrada la testabilidad y mantenibilidad.
- **Decisión:** Se implementa Arquitectura Hexagonal en todos los servicios core de Python. El dominio contiene exclusivamente entidades, objetos de valor y reglas de negocio puras; la infraestructura se aísla mediante puertos (interfaces abstractas) y adaptadores concretos (DuckDBAdapter, SocrataExtractor, etc.).
- **Consecuencias:**
  * *Positivas:* Cobertura de pruebas unitarias $> 90\%$ sin necesidad de levantar bases de datos; sustitución sencilla de motores de almacenamiento; conformidad estricta con SOLID.
  * *Negativas:* Mayor cantidad de clases e interfaces boilerplate.

### ADR-002: Modelo de Almacenamiento Lakehouse Medallion con DuckDB y Parquet
- **Estado:** Aceptado.
- **Contexto:** Se requiere procesar millones de registros de series temporales agrícolas con alta velocidad analítica, sin incurrir en costos elevados de licencias o clusters pesados de Big Data (Spark) para volúmenes medianos-altos ($< 2\text{ TB}$).
- **Decisión:** Adoptar el patrón Lakehouse Medallion (`Landing` $\rightarrow$ `Bronze` $\rightarrow$ `Silver` $\rightarrow$ `Gold`) en formato Apache Parquet columnar con compresión Snappy/ZSTD, consultado mediante **DuckDB** embebido como motor OLAP vectorial.
- **Consecuencias:**
  * *Positivas:* Consultas analíticas hasta 100 veces más rápidas que SQLite/PostgreSQL tradicional en agregaciones masivas; portabilidad absoluta basada en archivos Parquet versionados; costo de cómputo mínimo.
  * *Negativas:* No diseñado para escrituras transaccionales OLTP concurrentes de alta frecuencia (las cuales se delegan a PostgreSQL).

---

## 6. Definition of Done (DoD) para la Fase de Arquitectura

- [ ] Diagramas C4 (Contexto, Contenedores y Componentes) generados y validados.
- [ ] ADR-001, ADR-002 y ADR-003 redactados con trade-offs explícitos.
- [ ] Matriz de riesgos de ciberseguridad según OWASP ASVS Nivel 2 documentada.
- [ ] Contratos de interfaz y protocolos de comunicación inter-contenedor homologados.
