# Casos de Uso por Entidad (Use Cases)
**Proyecto**: Agro Stat & Tech Co. (AgroStats)  
**Versión**: 2.0.0  
**Fecha**: 2026-09-12  
**Fase PDCO**: PLAN  
**SDLC Stage**: Requirements  

---

## UC-001: Ingesta y Validación de Datasets Agropecuarios
- **Entidad Principal**: `DatasetAgropecuario`, `DataContract`
- **Actor Primario**: Administrador de Finca / Analista de Operaciones
- **Precondición**: El usuario dispone de credenciales activas y un archivo de datos (Excel/CSV) o credencial de API de su ERP.
- **Flujo Principal**:
  1. El actor sube un archivo plano o inicia la sincronización con su ERP agrícola.
  2. El sistema aplica el `DataContract` correspondiente al tipo de cultivo y labor (ej. Lote, Fecha, Grados Brix, Descarte, Humedad de Suelo muestreada).
  3. El sistema valida tipos de datos, ausencia de nulos críticos y límites biológicos admisibles.
  4. Los registros válidos se transforman y almacenan en la capa Silver del Lakehouse.
  5. El sistema emite un resumen de ingesta indicando registros procesados exitosamente.
- **Flujo Alternativo (FA-1 - Registros Anómalos)**:
  - En el paso 3, si se detectan registros inconsistentes (ej. pH = 19, fecha futura, texto en campo numérico), el sistema los deriva automáticamente a la *Dead Letter Queue (DLQ)*, genera una advertencia al usuario con el número de fila y continúa procesando los registros válidos.
- **Postcondición**: Dataset ingestando en Lakehouse, disponible para análisis bioestadístico.
- **Requerimientos Relacionados**: RF-001, RF-002, RF-003.

---

## UC-002: Análisis Bioestadístico y Control de Procesos (SPC)
- **Entidad Principal**: `CartaControlSPC`, `IndiceCapacidad`
- **Actor Primario**: Especialista Bioestadístico / Gerente de Calidad
- **Precondición**: Existen registros normalizados en el Lakehouse para el lote y ciclo evaluado.
- **Flujo Principal**:
  1. El actor selecciona el lote, el cultivo y la variable de interés (ej. calibre de fruto en cosecha, porcentaje de descarte en campo, índice de madurez).
  2. El sistema calcula la media histórica ($\bar{X}$), desviación estándar ($\sigma$) y límites de control estadístico ($UCL = \bar{X} + 3\sigma$, $LCL = \bar{X} - 3\sigma$).
  3. El sistema evalúa las Reglas de Western Electric para detectar causas especiales de variación.
  4. El sistema calcula los índices de capacidad potencial y real ($C_p, C_{pk}$) contra las tolerancias comerciales de exportación.
  5. El sistema renderiza la carta de control interactiva y muestra alertas si el proceso es inestable ($C_{pk} < 1.33$).
- **Flujo Alternativo (FA-2 - Muestra Insuficiente)**:
  - Si el número de observaciones es menor a $N=25$, el sistema informa que los límites son preliminares y sugiere consolidar más registros.
- **Postcondición**: Carta SPC generada y guardada en el historial de calidad del lote.
- **Requerimientos Relacionados**: RF-004, RF-005, RF-006.

---

## UC-003: Modelado Predictivo de Rendimiento (Yield AI)
- **Entidad Principal**: `ModeloBioestadistico`, `PronosticoCosecha`
- **Actor Primario**: Director de Producción Agroindustrial
- **Precondición**: Se dispone de datos históricos de mínimo dos campañas anteriores y registros climáticos del área.
- **Flujo Principal**:
  1. El actor solicita la proyección de cosecha para la campaña activa.
  2. El sistema entrena un modelo bioestadístico de regresión multivariada y aprendizaje automático utilizando grados-día de desarrollo (GDD), historial de precipitaciones y registros de floración provistos por el cliente.
  3. El sistema proyecta la curva de acumulación de biomasa, la ventana de cosecha estimada y el volumen total en toneladas métricas por hectárea.
  4. El sistema despliega el intervalo de confianza al 95%.
- **Postcondición**: Proyección de volumen y fecha óptima registrada en el tablero de planificación.
- **Requerimientos Relacionados**: RF-007, RF-008.

---

## UC-004: Auditoría de Procesos y Generación de Plan de Optimización BPMN
- **Entidad Principal**: `DiagnosticoBPMN`, `PlanMejoraProceso`
- **Actor Primario**: Consultor de Procesos Agro-STF / Gerente General
- **Precondición**: Completado el diagnóstico estadístico preliminar de mermas y variabilidad.
- **Flujo Principal**:
  1. El actor contrasta los hallazgos de variabilidad contra el flujo actual de labores registrado en el sistema.
  2. El sistema identifica cuellos de botella en la cadena (ej. demoras entre corte y enfriamiento, sobredosificación de insumos, calibración deficiente de seleccionadoras).
  3. El sistema genera el diagrama de proceso optimizado (*To-Be*) en notación estándar BPMN 2.0 y la matriz de acciones correctivas con impacto estimado en el P&L.
- **Postcondición**: Documento de optimización disponible para descarga y seguimiento.
- **Requerimientos Relacionados**: RF-009, RF-010.
