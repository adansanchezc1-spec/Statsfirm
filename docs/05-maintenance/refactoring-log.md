# Bitácora de Mantenimiento y Refactorización (Refactoring Log)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: OPERATIONS / MAINTENANCE  
**SDLC Stage**: Maintenance & Evolution  

---

## 1. Motivo del Cambio
Por decisión estratégica de la dirección y requerimiento formal del negocio, se ejecutó una refactorización arquitectónica, documental y corporativa total para **excluir cualquier componente, servicio o actividad relacionada con venta, instalación, mantenimiento o recopilación física mediante sensores y hardware IoT**, reenfocando la empresa 100% en:
> **Análisis riguroso de datos agropecuarios provistos por el cliente y optimización de procesos mediante bioestadística avanzada, Control Estadístico de Procesos (SPC) e ingeniería de procesos (BPMN)**.

---

## 2. Resumen de Artefactos Modificados

| Artefacto | Tipo | Modificaciones Clave |
|---|---|---|
| **Los 14 Documentos `.docx` de AgroStats** | Documentación Corporativa | Refactorización de 14 documentos Word eliminando menciones a LoRaWAN, sensores de suelo, gateways IoT y telemetría de hardware; reemplazados por ingesta multicanal de datasets, Data Contracts, bioestadística, SPC Shewhart y BPMN. |
| **`index.html`** | Portal Web Corporativo | Actualización del Hero, widget de telemetría SPC, Capa 1 de ingesta, tabla comparativa (eliminando "venta de hardware") y selector de formulario de contacto. |
| **`docs/01-requirements/`** | Ingeniería de Requerimientos | Creación de SRS formal (IEEE 830 / ISO 29148), catálogo de casos de uso por entidad y mapa de entidades ERD enfocado en datasets y calidad DAMA-BOK. |
| **`docs/02-architecture/`** | Arquitectura de Software | Documento de arquitectura en 3 capas analíticas (Ingesta, Lakehouse, SPC/BI), catálogo de patrones GoF/GRASP, diagramas UML de clases, secuencia y componentes. |
| **`docs/03-development/`** | Desarrollo / Contratos | Especificación formal de Data Contracts JSON Schema y reglas para Dead Letter Queues (DLQ). |
| **`metadata.json`** | Gobernanza de Proyecto | Creación del archivo de metadata de trazabilidad bajo el marco PDCO. |

---

## 3. Verificación de No Regresión
- Se ejecutaron análisis estáticos y búsquedas de expresiones regulares sobre los 14 `.docx` y sobre `index.html`.
- Las únicas apariciones de la palabra "sensores" o "hardware" corresponden a negaciones explícitas de la propuesta de valor (*"No comercializamos sensores de hardware..."* y *"Venta de hardware que termina sin uso"* en la tabla comparativa contra el enfoque tradicional).
- Se preservaron las jerarquías de estilos, tipografías y estructura corporativa original.
