# Servicio 02: Inteligencia de Negocios (BI) & Control Gerencial

**Código de Servicio**: AGRO-SRV-02  
**Línea de Portafolio**: 02 / Analítica de Negocio & Control Directivo  
**Normativa Aplicable**: SWEBOK Cap. 2, ISO/IEC 25010 (Usabilidad y Eficiencia), DAMA-BOK (Gestión de Inteligencia de Negocios).  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico Agroindustrial*), Sección `#que-ofrecemos` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones agroempresariales?
Diseña e implementa consolas gerenciales interactivas y tableros de control analítico que consolidan en tiempo real los datos agronómicos, operacionales, de inventario y financieros provenientes de los predios, plantas de beneficio y canales de comercialización. Facilita la toma de decisiones basada 100% en evidencia y rigor bioestadístico para gerentes, juntas directivas y cooperativas.

### Metáfora Operativa
Es como tener una torre de control agroindustrial de alta fidelidad que supervisa todos los frentes de la empresa: permite a los directores ver en una sola pantalla los rendimientos por hectárea, la curva de calidades de la cosecha de hoy y el margen neto por centro de costo sin esperar a los informes contables mensuales.

### Dolor de Negocio Resuelto
- **Decisiones Operativas Basadas en Corazonadas**: Sustituye la intuición y las aproximaciones empíricas por indicadores de rendimiento verificables y auditables.
- **Dispersión de Fuentes y Reportes Contradictorios**: Conecta los datos de producción de campo con los costos de planta y los ingresos por ventas.
- **Incapacidad de Comparación Histórica**: Permite evaluar de inmediato cómo se compara la cosecha o lote actual contra temporadas y ciclos climatológicos anteriores.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Cuadros de Mando Gerenciales Multi-predio** | Visualización unificada de rendimientos (kg/ha), calidades (primera, segunda, descarte) y costos unitarios. | Tableros ejecutivos Power BI / Looker accesibles en web y móvil. |
| **Análisis Comparativo Multitemporal** | Comparación de cosechas actuales contra cosechas históricas, condiciones edafoclimáticas y benchmarks. | Módulo analítico de tendencias agronómicas y productivas. |
| **Reportes Automatizados para Banca & Fondos** | Informes estructurados de flujo de caja operativo, proyecciones de volumen y cumplimiento de metas. | Generador automático de dossiers para comités de crédito y socios. |
| **Control de Mermas y Calidad en Línea** | Monitoreo del porcentaje de merma entre salida de campo y recepción en planta procesadora. | Indicador en tiempo real de mermas y causas de degradación. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Plataformas BI  │ Power BI Pro/Premium, Looker Studio       │
│ Visualización   │ Apache Superset, Observable, D3.js        │
│ Modelado        │ Esquema Estrella Agroindustrial, DAX, SQL │
│ Capa Semántica  │ Cube.js, Data Marts en PostgreSQL/DuckDB  │
│ Exportación     │ PDF ejecutivos automáticos, Excel dinámico│
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Latencia de Refresco**: Indicadores gerenciales actualizados en < 5 minutos tras sincronización de lotes.
- **Adopción de Usuarios**: Interfaz intuitiva probada para directores de operaciones y miembros de junta sin perfil técnico.
- **Cero Papel en Comités**: 100% de la información directiva presentada en tableros en vivo, reduciendo horas de preparación de comités en un 85%.
