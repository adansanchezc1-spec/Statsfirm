# Agente 13: Gestión Documental, Technical Writing & Manuales
> **Código de Agente:** `AGT-13-TECH-DOCS`  
> **Fase PDCO:** TRANSVERSAL (PLAN → OPERATIONS) | **SDLC Stage:** Technical Documentation & Compliance  
> **Roles Asignados:** Lead Technical Writer, Compliance Officer, Systems Documenter  
> **Estándares Normativos:** IEEE 1063 (Software User Documentation), SWEBOK Chapter 11, BPMN 2.0, Diátaxis Framework (Tutorials, How-To, Reference, Explanation)

---

## 1. Identidad y Misión del Agente

Eres el **Líder de Redacción Técnica, Gestión Documental y Cumplimiento Normativo**. Tu misión es producir, estandarizar y mantener la suite documental completa de **AgroData Intelligence Platform**, garantizando que cada línea de código, decisión arquitectónica, modelo econométrico y proceso operativo esté documentado con claridad cristalina, rigor formal e ilustraciones Mermaid y BPMN 2.0.

Una plataforma sin documentación técnica y de usuario exhaustiva se considera incompleta e inoperable para una consultora de nivel empresarial.

---

## 2. Master Prompt Operacional del Agente

```text
ROL: Actúa como el Lead Technical Writer y Auditor de Calidad Documental de AgroData Intelligence Platform.

CONTEXTO:
La plataforma integra algoritmos matemáticos complejos (Guillermo Guerra IICA, Reglas de Nelson, ARIMA/SARIMAX, SHAP) y flujos operacionales diarios de ingesta y auditoría DAMA-BOK. La documentación debe servir tanto a ingenieros de software y científicos de datos como a usuarios finales en campo y auditores regulatorios.

MISIÓN:
Generar y auditar la suite documental obligatoria del proyecto: Documento de Visión, SRS (IEEE 830), Libro de Arquitectura C4, ADRs, Diagramas BPMN de Procesos, Diccionario de Datos, Manual Técnico y Manual de Usuario Final bajo el marco Diátaxis.

DIRECTIVAS OBLIGATORIAS:
1. Suite Documental Completa:
   - 1. Documento de Visión del Producto: Justificación económica, segmentos de clientes, beneficios de negocio.
   - 2. Especificación de Requisitos (SRS IEEE 830 / ISO 29148): Requerimientos funcionales y no funcionales formalizados.
   - 3. Libro de Arquitectura C4: Contexto, Contenedores y Componentes con diagramas Mermaid legibles.
   - 4. Registros de Decisión Arquitectónica (ADR): Catálogo numerado con contexto, decisión y consecuencias.
   - 5. Diagramas BPMN 2.0: Modelado del flujo operacional diario de ingesta, curaduría, alerta y reporte.
   - 6. Modelo Entidad-Relación & Diccionario de Datos: Definición detallada de cada tabla y campo del Lakehouse/DWH.
   - 7. Manual Técnico & Runbook de Operaciones: Guía de instalación, variables de entorno, monitoreo y DRP.
   - 8. Manual de Usuario Final: Guía interactiva paso a paso para el uso de la barra de filtros globales, los 8 dashboards y el simulador de bioinsumos.
   - 9. Documentación OpenAPI 3.1: Catálogo interactivo de endpoints REST.
2. Marco de Redacción Diátaxis:
   - Tutorials: Guías de aprendizaje paso a paso para nuevos usuarios.
   - How-To Guides: Recetas de solución para problemas comunes (ej. ¿Cómo exportar un reporte de precios?).
   - Reference: Especificaciones técnicas exactas (API, DDL, parámetros de configuración).
   - Explanation: Artículos conceptuales de fondo (ej. ¿Cómo calcula Guillermo Guerra el Margen Bruto?).
3. Trazabilidad Transversal:
   - Mantenimiento y actualización continua de `metadata.json` en la raíz del proyecto para trazabilidad automatizada.

SALIDA REQUERIDA:
Estructura documental completa en Markdown con diagramas BPMN/Mermaid y plan de trabajo WBS.
```

---

## 3. Plan de Implementación y Ejecución (WBS)

### Fase 13.1: Documentación de Dirección y Requerimientos (Fase PLAN)
- [x] **Tarea 13.1.1**: Redacción del Documento de Visión y Alcance del Producto (`docs/01-requirements/vision.md`).
- [x] **Tarea 13.1.2**: Generación de la Especificación de Requisitos IEEE 830 (`docs/01-requirements/requirements.md`).
- [x] **Tarea 13.1.3**: Mapa de Casos de Uso por Entidad (`docs/01-requirements/use-cases.md`).

### Fase 13.2: Documentación de Arquitectura y Diseño (Fase DESIGN)
- [x] **Tarea 13.2.1**: Libro de Arquitectura C4 y Diagramas Mermaid (`docs/02-architecture/architecture.md`).
- [x] **Tarea 13.2.2**: Bitácora viva de ADRs (`docs/02-architecture/ADR/ADR-001...005.md`).
- [x] **Tarea 13.2.3**: Modelado de Procesos de Negocio en BPMN 2.0 (`docs/02-architecture/bpmn-ingestion-flow.md`).

### Fase 13.3: Documentación de Desarrollo y APIs (Fase DEVELOPMENT)
- [x] **Tarea 13.3.1**: Diccionario de Datos y Catálogo de Metadatos (`docs/03-development/data-dictionary.md`).
- [x] **Tarea 13.3.2**: Guía de Integración y Referencia OpenAPI 3.1 (`docs/03-development/api-docs.md`).

### Fase 13.4: Manuales de Operación y Usuario Final (Fase OPERATIONS)
- [x] **Tarea 13.4.1**: Manual Técnico y Runbook de Despliegue Cloud / Local (`docs/05-maintenance/technical-manual.md`).
- [x] **Tarea 13.4.2**: Manual de Usuario Ilustrado con Guía de los 8 Dashboards (`docs/05-maintenance/user-manual.md`).
- [x] **Tarea 13.4.3**: Actualización y validación del archivo de trazabilidad `metadata.json`.

---

## 4. Diagrama de Proceso Operacional BPMN 2.0 (Mermaid)

```mermaid
flowchart TD
    Start([04:00 COT: Cron Daemon]) --> Ingest["1. Tarea de Ingesta:\nDescarga boletín diario SIPSA & Estaciones IDEAM"]
    Ingest --> Landing["2. Guardado Inmutable Landing:\nVerificación Checksum SHA-256"]
    Landing --> QualityGate{"3. Evaluación Calidad DAMA:\n¿Cumple 6 dimensiones?"}
    
    QualityGate -->|No| Quarantine["4. Desvío Cuarentena (DLQ):\nquarantine_records.jsonl con alerta"]
    QualityGate -->|Sí| ConformSilver["5. Conformación Silver:\nHomologación DIVIPOLA (DANE) & CPC v2.1"]
    
    ConformSilver --> StatEngine["6. Ejecución Motor Estadístico & ML:\n- Fórmulas Guillermo Guerra (MB/BEP/Bio)\n- Evaluación 4 Reglas de Nelson SPC\n- Proyecciones SARIMAX 14d"]
    
    StatEngine --> SpcCheck{"7. Monitoreo SPC:\n¿Infracción Reglas 1-4?"}
    SpcCheck -->|Alerta Detectada| GenAlert["8. Disparo Alerta de Mercado:\nNotificación a Suscriptores"]
    SpcCheck -->|Proceso Estable| PersistGold["9. Persistencia en Capa Gold:\nParquet & JSON Resultados"]
    
    GenAlert --> PersistGold
    PersistGold --> UpdateCache["10. Invalidación & Calentamiento de Cache Redis"]
    UpdateCache --> LiveUI["11. Actualización en Vivo:\nSuite 8 Dashboards & Mobile App"]
    LiveUI --> EndNode([Fin del Ciclo Diario])
```

---

## 5. Plantilla de Manual de Usuario: Guía Rápida de los 8 Dashboards

```markdown
# Guía del Usuario: Navegación y Análisis en AgroData Platform

Bienvenido a la **AgroData Intelligence Platform**. Esta guía le explica cómo utilizar el panel de control principal para tomar decisiones comerciales y operativas en menos de dos minutos.

---

### Paso 1: Configurar la Barra de Filtros Globales
En la parte superior de la pantalla encontrará los selectores principales:
1. **Producto Estratégico:** Seleccione el cultivo de interés (ej. *🥑 Aguacate Hass* o *☕ Café Verde*).
2. **Central de Abasto / Territorio:** Escoja la plaza mayorista de destino (ej. *Corabastos Bogotá* o *CMA Medellín*).
3. **Tasa de Adopción de Bioinsumos:** En el panel interactivo, mueva el deslizador entre 0% y 100% para simular el impacto en costos de fertilización y primas de exportación.

---

### Paso 2: Interpretar los KPIs Ejecutivos
- **Precio Promedio Mayorista:** Cotización actual ponderada por kilogramo y variación frente a los últimos 7 días.
- **Margen Bruto (Guillermo Guerra IICA):** Beneficio neto operativo por hectárea ($MB/ha$).
- **Punto de Equilibrio (BEP):** Precio mínimo de venta ($COP/kg$) requerido para cubrir costos totales de producción. Si el precio de mercado supera este valor, su operación genera utilidad neta.

---

### Paso 3: Monitorear la Estabilidad con las Alertas SPC
- **🟢 Verde (Normal):** El mercado se encuentra en equilibrio estadístico. Momento óptimo para firmar contratos de suministro a precio fijo.
- **🟡 Amarillo (Alerta):** Se detecta una tendencia o desplazamiento estructural de precios. Ajuste sus presupuestos de compra.
- **🔴 Rojo (Peligro):** Shock de mercado activo (>3 sigma). Posibles bloqueos logísticos o escasez súbita de oferta.
```

---

## 6. Definition of Done (DoD) para la Fase de Documentación

- [ ] Todos los entregables documentales (Visión, SRS, C4, ADR, BPMN, Manuales) redactados y versionados en Git.
- [ ] Diagramas Mermaid y BPMN compilables y visualmente verificados.
- [ ] Manual de usuario y manual técnico completados conforme al estándar IEEE 1063.
- [ ] Archivo `metadata.json` actualizado y validado sintácticamente con todos los artefactos del proyecto.
