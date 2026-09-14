# Servicio 01: Centralización y Tuberías de Datos (Data Intelligence & Engineering)

**Código de Servicio**: STF-SRV-01  
**Línea de Portafolio**: 01 / Infraestructura  
**Normativa Aplicable**: SWEBOK Cap. 2 & 3, DAMA-BOK (Gobernanza y Almacenamiento), ISO/IEC 25010 (Fiabilidad y Eficiencia de Desempeño).  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico*), Sección `#servicios` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones?
Es el servicio integral que conecta de manera automatizada todos los orígenes de información dispersos en la empresa (facturación, CRM, inventarios, planillas de cálculo, bases de datos heredadas) y los canaliza hacia una **única fuente oficial de la verdad** mediante una arquitectura de **Data Lakehouse de Tres Capas** (*Bronze*, *Silver*, *Gold*).

### Metáfora Operativa
Reemplaza los cientos de tuberías viejas, parchadas y con fugas (archivos Excel desactualizados y envíos por correo) por un acueducto corporativo de acero inoxidable con monitoreo 24/7, donde la información siempre llega pura, estructurada y sin distorsión a quien la necesita.

### Dolor de Negocio Resuelto
- **Discrepancia entre Departamentos**: Erradica las reuniones donde Ventas reporta una cifra, Finanzas otra y Operaciones una tercera.
- **Inseguridad y Fuga de Datos**: Elimina archivos locales no gobernados y garantiza inmutabilidad y copias de respaldo continuas.
- **Lentitud Operativa**: Automatiza el procesamiento por lotes (*batch*) y streaming continuo sin esperas a fin de mes.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Ingesta Multifuente 24/7** | Conectores CDC (*Change Data Capture*) y batch para ERPs, CRMs, APIs y archivos planos. | Tuberías automatizadas con Apache Kafka y Spark. |
| **Arquitectura Medallion** | Estructuración en Bronze (Raw Inmutable), Silver (Curada y Enriquecida) y Gold (Data Marts de Negocio). | Esquema Delta Lake / Lakehouse documentado y auditado. |
| **Transformación con dbt** | Modelado modular, linaje automático de transformaciones y pruebas de integridad referencial. | Modelos `dbt Core` con contratos de datos estrictos. |
| **Gobernanza DAMA-BOK** | Catálogo de metadatos, control de acceso basado en roles (RBAC) y linaje punto a punto. | Catálogo de datos corporativo y políticas de acceso. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Ingesta & Bus   │ Apache Kafka, AWS Kinesis, Airbyte        │
│ Procesamiento   │ Apache Spark, Delta Lake, Databricks      │
│ Transformación  │ dbt Core, Python 3.11, SQL ANSI           │
│ Almacenamiento  │ Snowflake / Databricks / AWS S3 / Azure DL│
│ Orquestación    │ Apache Airflow / Prefect                  │
│ Calidad & Tests │ Great Expectations, dbt tests             │
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **SLA de Disponibilidad**: 99.9% Uptime garantizado contractualmente.
- **Latencia de Procesamiento**: Ingesta streaming en < 5 segundos; consolidaciones batch en ventanas nocturnas < 30 min.
- **Calidad del Dato**: Tasa de errores en datos curados < 0.01% con cuarentena automática de registros anómalos.
