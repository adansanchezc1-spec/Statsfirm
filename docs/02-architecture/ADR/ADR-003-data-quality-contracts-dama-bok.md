# ADR-003: Contratos de Calidad de Datos DAMA-BOK y Dead Letter Queue (DLQ)
**Fecha**: 2026-09-14  
**Estado**: Aceptado  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Autores**: Equipo de Ingeniería de Software y Ciencia de Datos — Agro Stat & Tech Co.  

---

## Contexto
Los datos provenientes de fuentes abiertas gubernamentales (SIPSA, IDEAM, Agronet) presentan con frecuencia valores atípicos, tipografías dispares, codificaciones incompletas o campos numéricos nulos. 

Las prácticas ingenuas de ingeniería de datos suelen cometer dos graves errores:
1. *Mutación silenciosa*: Imputar medias o medianas a ciegas en el paso de ingesta, alterando la verdad de los datos crudos.
2. *Descarte silencioso (`drop_na`)*: Eliminar registros sin registro alguno, perdiendo trazabilidad y sesgando los análisis posteriores.

Bajo el marco **DAMA-BOK (Data Management Body of Knowledge)**, la calidad de datos es un activo de gobierno que requiere verificación explícita de dimensiones de calidad (completitud, validez, consistencia, unicidad) y auditabilidad completa (RF-006 a RF-010, RNF-003, RNF-006).

## Decisión
Se establece una política de **Contratos de Datos Estrictos y Curaduría No Destructiva**:
1. **Validación Declarativa en el Dominio**: La clase `DataQualityValidator` ejecuta una cadena de reglas determinísticas sobre cada lote entrante.
2. **Derivación a Dead Letter Queue (DLQ)**: Todo registro que viole un invariante crítico de negocio (precio negativo, fecha futura, clave primaria nula, o inconsistencia $P_{min} > P_{max}$) se extrae del lote analítico y se persiste de manera inmutable en `data/dlq/quarantine_YYYYMMDD_HHMMSS.jsonl`.
3. **Diagnóstico Estructurado**: Cada registro en la DLQ incluye el registro crudo original, el nombre de la regla infringida, el valor anómalo detectado y el timestamp de auditoría.
4. **Métricas de Calidad**: El sistema calcula un `DataQualityReport` con el porcentaje de completitud y validez del lote. Si la tasa de rechazo supera el umbral del 5%, se dispara una alerta preventiva (`QualityThresholdExceededAlert`).

## Consecuencias

### Positivas:
- **Cero Corrupción de la Capa Gold**: El Data Warehouse y los modelos de ML solo reciben datos 100% verificados y consistentes.
- **Trazabilidad Forense Total**: Los ingenieros de datos pueden inspeccionar la DLQ e identificar patrones de degradación en las APIs de origen sin haber perdido ningún registro.
- **Cumplimiento DAMA-BOK**: Trazabilidad y gobernanza de principio a fin.

### Negativas / Trade-offs:
- Requiere espacio en disco para el almacenamiento de registros en cuarentena.
- Necesidad de herramientas o comandos de reprocesamiento para corregir y reingestar lotes de la DLQ una vez subsanada la causa raíz.
