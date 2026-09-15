# Manual Técnico y Arquitectura de la Plataforma AgroData Enterprise v1.0

## 1. Visión General
**AgroData Intelligence Platform** es una suite empresarial de analítica de datos, inteligencia de mercado y bioeconomía para el agro colombiano. La solución integra datos de fuentes oficiales (DANE SIPSA, MADR Agronet/EVA, ICA, IDEAM) en una arquitectura **Lakehouse Medallion** con DuckDB/Parquet y expone servicios analíticos mediante **FastAPI** y una interfaz web corporativa desacoplada y reactiva.

---

## 2. Estructura Arquitectónica

```
AgroStatsApp/
├── data/
│   ├── landing/                     # Datos crudos ingestionados
│   ├── bronze/                      # Parquet estructurado inicial
│   ├── silver/                      # Datos limpios e imputados (DAMA-BOK)
│   ├── gold/                        # Métricas agregadas y modelos analíticos
│   └── seeds/                       # Catálogos maestros oficiales (CPC, DIVIPOLA, ICA)
├── src/agrostats/
│   ├── domain/
│   │   ├── entities.py              # Entidades de negocio ricas
│   │   ├── value_objects.py         # Objetos de valor inmutables
│   │   ├── exceptions.py            # Jerarquía de excepciones RFC 7807
│   │   └── services/
│   │       ├── guerra_agroeconomics_engine.py  # Metodología Guillermo Guerra (IICA)
│   │       ├── biostatistical_engine.py       # Shewhart SPC & 4 Reglas de Nelson
│   │       ├── data_quality_validator.py      # 6 Dimensiones DAMA-DMBOK
│   │       └── intelligent_imputer.py         # Diagnóstico MCAR/MAR & Imputación
│   └── adapters/
│       └── driving/api/server.py    # API REST FastAPI / OpenAPI 3.1
├── web/
│   ├── index.html                   # Suite de los 8 Dashboards & Barra Global
│   ├── css/design_system.css        # Sistema de diseño, tokens y glassmorphism
│   └── js/app.js                    # AgroStateStore pub/sub y renderizador Canvas
├── sql/
│   ├── schema_oltp.sql              # Esquema 3NF PostgreSQL 16
│   ├── schema_dwh_star.sql          # Esquema Estrella Kimball con particionamiento
│   └── seeds_catalogs.sql           # Inserción de semillas SQL
├── tests/
│   ├── unit/                        # Pruebas unitarias de dominio y servicios
│   ├── integration/                 # Pruebas de integración de endpoints
│   └── run_tests.py                 # Runner maestro (100% assertions passing)
├── Dockerfile                       # Construcción multi-stage de producción
├── docker-compose.yml               # Orquestación de contenedores
├── requirements.txt                 # Dependencias Python
└── metadata.json                    # Gobernanza y trazabilidad técnica
```

---

## 3. Modelo Bioeconómico de Guillermo Guerra (IICA)
Implementado en [`src/agrostats/domain/services/guerra_agroeconomics_engine.py`](file:///c:/Users/ADAN/OneDrive/Documentos/Statsfirm/AgroStats%20AndTech/AgroStatsApp/src/agrostats/domain/services/guerra_agroeconomics_engine.py):

$$\text{Margen Bruto (MB)} = \text{Ingreso Bruto (IB)} - \text{Costos Variables (CV)}$$

$$\text{Punto de Equilibrio Físico} = \frac{\text{Costos Fijos} + \text{Costos Variables}}{\text{Precio Efectivo}}$$

$$\text{Punto de Equilibrio Monetario} = \frac{\text{Costos Fijos} + \text{Costos Variables}}{\text{Rendimiento (kg/ha)}}$$

$$\text{Ahorro Químico} = \text{Costo Insumos Síntesis} \times (\text{Tasa Ahorro Max} \times \text{Factor Adopción})$$

$$\text{Precio Efectivo} = \text{Precio Base} \times (1 + \text{Prima Verde Cero LMR} \times \text{Factor Adopción})$$

---

## 4. Control Estadístico Shewhart y 4 Reglas de Nelson (ISO 7870)
- **Límites de Control**:
  $$\mu \pm 3\sigma$$
- **Regla 1**: Un punto más allá de $3\sigma$ respecto a la línea central.
- **Regla 2**: 9 puntos consecutivos en el mismo lado de la línea central.
- **Regla 3**: 6 puntos consecutivos en aumento o descenso continuo.
- **Regla 4**: 14 puntos alternando consecutivamente hacia arriba y hacia abajo.

---

## 5. Instrucciones de Ejecución

### Ejecución de Pruebas Automatizadas
```bash
python tests/run_tests.py
```

### Ejecución del Servidor Backend (FastAPI)
```bash
uvicorn src.agrostats.adapters.driving.api.server:app --reload --port 8000
```
- Swagger UI interactivo: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Visualización de la Aplicación Web
Abrir [`web/index.html`](file:///c:/Users/ADAN/OneDrive/Documentos/Statsfirm/AgroStats%20AndTech/AgroStatsApp/web/index.html) en cualquier navegador web moderno o servir con cualquier servidor estático HTTP.
