# Servicio 02: Tableros Ejecutivos en Tiempo Real (Business Intelligence & Decision Analytics)

**Código de Servicio**: STF-SRV-02  
**Línea de Portafolio**: 02 / Visualización & Decisión  
**Normativa Aplicable**: SWEBOK Cap. 2, ISO/IEC 25010 (Usabilidad y Eficiencia), Directrices de Visualización y Experiencia Directiva.  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico*), Sección `#servicios` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones?
Transforma los datos limpios de la capa Gold del Lakehouse en consolas visuales ejecutivas, tableros interactivos (Power BI, Looker, Apache Superset) y árboles de KPIs que permiten a la dirección general y a los líderes de área monitorear el desempeño del negocio minuto a minuto desde su computador o teléfono móvil.

### Metáfora Operativa
Es como reemplazar el velocímetro análogo roto de su automóvil por una cabina de navegación digital de alta definición que no solo le muestra la velocidad y combustible exactos, sino que le advierte con anticipación si una ruta presenta riesgo de colisión o retraso.

### Dolor de Negocio Resuelto
- **Decisiones Tardías o a Ciegas**: Acaba con la espera de 15 a 30 días posteriores al cierre contable mensual para enterarse de desviaciones financieras o comerciales.
- **Sobrecarga de Reportes Manuales**: Reduce hasta en un 80% el tiempo que los equipos operativos y analistas destinan a armar presentaciones y cuadros manuales.
- **Falta de Alineación Estratégica**: Establece una única definición de métricas (EBITDA, CAC, LTV, Rotación, Margen de Contribución) compartida por toda la compañía.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Consolas Ejecutivas Dark Mode** | Diseñadas para juntas directivas con paletas de alto contraste y legibilidad ejecutiva. | Tableros Power BI Embedded / Looker con filtros dinámicos. |
| **Árboles de KPIs & Drill-Down** | Navegación desde el indicador macro hasta la transacción individual o cliente específico. | Modelo semántico multidimensional (Esquema Estrella/Copo de Nieve). |
| **Alertas Inteligentes Push** | Disparadores automáticos vía Webhook, correo corporativo o WhatsApp ante caída de márgenes. | Sistema de alertas configurado con umbrales de tolerancia. |
| **Simuladores What-If** | Parámetros interactivos para proyectar el impacto de variaciones de precios o costos. | Módulo de simulación de escenarios de negocio. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Motores BI      │ Power BI Embedded, Google Looker, Tableau │
│ Open Source BI  │ Apache Superset, Metabase, Evidence.dev   │
│ Capa Semántica  │ Cube.js, dbt Semantic Layer               │
│ Almacenamiento  │ DuckDB, PostgreSQL, Snowflake, BigQuery   │
│ Cache & Rápido  │ Redis, ClickHouse                         │
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Tiempo de Carga de Tableros**: < 2.5 segundos para el 95% de las consultas analíticas directivas.
- **Reducción de Tiempo en Informes**: -80% en horas invertidas por el equipo financiero/comercial en consolidación manual.
- **Frecuencia de Actualización**: Cuadros comerciales actualizados en tiempo real o cada 15 minutos según requerimiento.
