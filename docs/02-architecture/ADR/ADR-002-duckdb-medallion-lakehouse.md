# ADR-002: Almacenamiento Medallion Lakehouse con DuckDB y Apache Parquet
**Fecha**: 2026-09-14  
**Estado**: Aceptado  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Autores**: Equipo de Ingeniería de Software y Ciencia de Datos — Agro Stat & Tech Co.  

---

## Contexto
El sistema debe procesar millones de cotizaciones de precios agrícolas del DANE (SIPSA), registros de abastecimiento municipal, evaluaciones agropecuarias (EVA de Agronet) y series de tiempo meteorológicas diarias del IDEAM y NASA POWER (RF-001 a RF-005, RF-011, RF-012). 

Se requiere:
1. Rendimiento analítico en agregaciones temporales multidimensionales (latencia < 200 ms, RNF-002).
2. Cero fricción operativa: la plataforma debe ser capaz de correr de manera autónoma sin requerir la administración de servidores de bases de datos complejos o pesados en máquinas locales.
3. Compatibilidad con el estándar ANSI SQL (RNF-004) y modelado dimensional en estrella (Kimball).

Se evaluaron tres alternativas:
1. *PostgreSQL dedicado*: Robusto, pero introduce costos de infraestructura, latencias mayores en escaneos analíticos OLAP columnares de millones de filas sin extensiones complejas (TimescaleDB/Citus).
2. *SQLite*: Ligero y embebido, pero con almacenamiento basado en filas (row-oriented), soporte limitado de funciones de ventana analíticas y pobre rendimiento en queries OLAP complejas.
3. *Apache Spark*: Excelente para petabytes, pero desmesurado e ineficiente para despliegues locales y analítica analítica de escala gigabyte/terabyte.

## Decisión
Se decide implementar un **Data Lakehouse en Arquitectura Medallion** respaldado por **DuckDB** y **Apache Parquet**:
- **Capa Bronze (`data/bronze/`)**: Archivos Parquet/JSONL inmutables que preservan los payloads crudos con firma hash SHA-256 de auditoría.
- **Capa Silver (`data/silver/`)**: Tablas y archivos Parquet tipados, normalizados geográficamente (DIVIPOLA) y taxonómicamente (CPC), validados bajo reglas DAMA-BOK.
- **Capa Gold (`data/gold/agro_dw.duckdb`)**: Data Warehouse dimensional en estrella (Kimball) persistido en un archivo DuckDB local de alto rendimiento, con índices B-Tree y vistas materializadas analíticas de balance de mercado y control de calidad bioestadístico.

## Consecuencias

### Positivas:
- **Velocidad de Consulta Vectorizada**: DuckDB ejecuta agregaciones analíticas de grupos de tiempo y filtros espaciales entre 10x y 50x más rápido que motores tradicionales orientados a filas.
- **Cero Infraestructura**: No requiere configurar daemons de base de datos ni credenciales complejas para su ejecución local.
- **Interoperabilidad Total**: DuckDB lee y escribe archivos Parquet directamente y permite migrar el esquema DDL a PostgreSQL de forma transparente.

### Negativas / Trade-offs:
- DuckDB está optimizado para cargas de trabajo analíticas (OLAP). No es adecuado para transacciones OLTP de alta concurrencia con escrituras concurrentes intensivas a nivel de microsegundo.
- La persistencia en un único archivo requiere sincronización de escritura para evitar contención de bloqueo de archivo (*file locking*).
