# Especificación Formal de Contratos de Datos (Data Contracts)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: DEVELOPMENT  
**SDLC Stage**: Implementation  
**Estándar**: DAMA-BOK / JSON Schema / Pydantic  

---

## 1. Fundamentos y Propósito
Para garantizar la integridad y veracidad de los análisis bioestadísticos sin depender de hardware ni mecanismos físicos de captura, AgroStats implementa **Data Contracts** estrictos. Todo dataset provisto por el cliente debe satisfacer las dimensiones de calidad de **DAMA-BOK**:
1. **Completitud**: Campos obligatorios libres de valores nulos o vacíos.
2. **Validez**: Conformidad con tipos de datos y rangos agronómicos admisibles.
3. **Consistencia**: Coherencia cronológica (ej. fecha de cosecha posterior a fecha de siembra/floración).
4. **Unicidad**: Ausencia de registros duplicados para el mismo lote y franja horaria.
5. **Precisión**: Unidades de medida estandarizadas (ej. kg, ton/ha, °Brix, mm de precipitación).

---

## 2. Esquema Canónico de Ingesta (Dataset de Cosecha y Calidad)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AgroHarvestBatchContract",
  "type": "object",
  "required": [
    "lote_id",
    "fecha_cosecha",
    "kilos_totales",
    "kilos_exportables",
    "calibre_promedio",
    "grados_brix",
    "responsable_registro"
  ],
  "properties": {
    "lote_id": {
      "type": "string",
      "pattern": "^[A-Z0-9_-]{3,30}$",
      "description": "Identificador unívoco del lote o cuartel agronómico."
    },
    "fecha_cosecha": {
      "type": "string",
      "format": "date",
      "description": "Fecha de recolección en formato ISO 8601 (YYYY-MM-DD)."
    },
    "kilos_totales": {
      "type": "number",
      "minimum": 0.1,
      "maximum": 500000.0,
      "description": "Peso bruto recolectado en kilogramos."
    },
    "kilos_exportables": {
      "type": "number",
      "minimum": 0.0,
      "description": "Peso de fruta que cumple estándar de exportación."
    },
    "calibre_promedio": {
      "type": "number",
      "minimum": 10.0,
      "maximum": 90.0,
      "description": "Calibre o peso unitario medio del fruto en gramos o clasificación comercial."
    },
    "grados_brix": {
      "type": "number",
      "minimum": 4.0,
      "maximum": 32.0,
      "description": "Concentración de sólidos solubles (azúcares) medida por refractómetro en poscosecha."
    },
    "ph_suelo_muestreado": {
      "type": ["number", "null"],
      "minimum": 3.5,
      "maximum": 9.5,
      "description": "Medición físico-química de laboratorio si está disponible."
    },
    "responsable_registro": {
      "type": "string",
      "minLength": 3,
      "maxLength": 100,
      "description": "Nombre o identificador del técnico que cargó la información."
    }
  }
}
```

---

## 3. Comportamiento ante Inconsistencias (Dead Letter Queue)
Cuando un registro viola las restricciones del contrato:
1. El registro se excluye inmediatamente del conjunto de entrenamiento de modelos predictivos y del cálculo de límites SPC.
2. Se emite un payload de cuarentena a `dlq_inconsistencias` registrando:
   - Identificador del lote y número de fila en el archivo de origen.
   - Regla violada (ej. `grados_brix=45.0 > max 32.0`).
   - Timestamp de ingesta.
3. Se notifica al productor para corregir el valor en su sistema de origen (evitando el antipatrón de modificar datos silenciosamente sin trazabilidad).
