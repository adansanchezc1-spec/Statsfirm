# Servicio 03: Curaduría Lakehouse & Datos Agroempresariales

**Código de Servicio**: AGRO-SRV-03  
**Línea de Portafolio**: 03 / Infraestructura TI & Gobernanza del Dato  
**Normativa Aplicable**: SWEBOK Cap. 2 & 3, DAMA-BOK (Calidad del Dato y Gobernanza), Estándares Internacionales de Exportación (Regulación EUDR, GlobalGAP, Rainforest Alliance).  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico Agroindustrial*), Documento 04 (*Gobierno Corporativo y Políticas del Dato Agropecuario*), Sección `#que-ofrecemos` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones agroempresariales?
Centraliza, limpia, audita y estructura todas las fuentes dispersas de la agroempresa (archivos de labores, básculas camioneras, ERPs corporativos como SAP, Siigo o AgroWin) bajo un repositorio central inmutable (**Lakehouse Agroempresarial**). Implementa contratos de datos (*Data Contracts*) que impiden la contaminación del sistema con información duplicada o incompleta, garantizando la soberanía absoluta de los datos en manos de la agroempresa.

### Metáfora Operativa
Es como una planta de purificación y empaque con laboratorio de calidad certificado: no permite que ingrese materia prima sucia o con piedras a la cadena de producción. Cada dato que entra es tamizado, catalogado y sellado criptográficamente para que, si un auditor internacional o comprador exige pruebas de trazabilidad de hace tres años, el expediente completo esté disponible al instante.

### Dolor de Negocio Resuelto
- **Falta de Trazabilidad y Riesgo de Sanciones de Exportación**: Cumple estrictamente los requerimientos de no-deforestación de la Unión Europea (EUDR) y certificaciones internacionales.
- **Opacidad en los Centros de Costos**: Identifica con exactitud cuánto costó producir cada tonelada en cada lote particular, absorbiendo insumos, mano de obra y transporte.
- **Dependencia de Proveedores Cautivos de Sensores**: Funciona 100% sobre los datos que la empresa ya tiene, sin obligar a comprar sensores o hardware costoso.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Data Contracts & Cuarentena Automática** | Esquemas JSON Schema / Pydantic que rechazan automáticamente registros que violen rangos agronómicos o reglas de negocio. | Tubería con área de cuarentena y alertas de calidad del dato. |
| **Linaje Criptográfico para EUDR & GlobalGAP** | Registro inmutable de predio, coordenadas poligonales, fecha de siembra/cosecha y despachos. | Dossier digital de trazabilidad y linaje para exportaciones. |
| **Estructuración de Centros de Costos (ABC)** | Asignación automática de costos directos e indirectos por hectárea, variedad y predio. | Modelo de costeo analítico integrado al sistema contable. |
| **Soberanía Inalienable de la Información** | Implementación en la nube propia del cliente (AWS, Azure, GCP o servidores propios) con estándares abiertos. | Custodia total de datos bajo estándares abiertos (Parquet, Delta Lake). |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Formato de Almacén│ Delta Lake, Apache Parquet, DuckDB       │
│ Procesamiento   │ Python 3.11 (Pandas, Polars, PySpark)     │
│ Contratos Datos │ Pydantic V2, Great Expectations, dbt tests│
│ Conectores ERP  │ Conectores para SAP, Siigo, AgroWin, Excel│
│ Seguridad       │ Cifrado AES-256 en reposo, Hashing SHA-256│
│ Infraestructura │ Nube del cliente o Servidor Local On-Premise│
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Tasa de Pureza del Dato**: > 99.8% de registros validados y conformes en la capa de producción analítica.
- **Tiempo de Respuesta en Auditorías**: Expediente de trazabilidad de lote generado en < 2 minutos para inspectores o clientes.
- **Soberanía del Dato**: 100% de la propiedad legal y técnica en servidores del productor, sin vendor lock-in.
