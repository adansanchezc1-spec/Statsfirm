# Catálogo Técnico de Formularios Camunda Forms ("Las Formas") — Statsfirm Co.

**Código Documental**: SFC-CAMUNDA-FRM-008  
**Versión**: 1.0  
**Fecha**: Septiembre 2026  
**Fase PDCO**: DEVELOPMENT / CONTROL  
**Estándar de Esquema**: Camunda Form Schema Version 16 | Camunda Desktop & Web Modeler 5.x+ | Camunda 7 & 8 Compatible  
**Ubicación de Archivos**: `bpmn/forms/*.form`  

---

## 1. Visión General de Formularios de Usuario

En la ingeniería de procesos de **Statsfirm Co.**, las tareas de usuario (`bpmn:userTask`) representan los puntos de control humano y toma de decisiones donde los especialistas del Squad, las Oficinas Corporativas o el Cliente interactúan con la plataforma.

Cada formulario ha sido construido como un archivo formal **Camunda Form JSON (`.form`)** que puede ser:
1. Diseñado y visualizado nativamente en el **Form Builder de Camunda Modeler** (desktop o SaaS).
2. Renderizado dinámicamente en **Camunda Tasklist** (Camunda 7 o Camunda 8).
3. Consumido vía API por la **App Móvil y Web del Cliente** ([Documento 10](file:///c:/Users/ADAN/Downloads/Statsfirm/Statsfirm/Statsfirm%20Co%20-%2010.%20Ecosistema%20Digital%20y%20Especificación%20de%20la%20Aplicación%20del%20Cliente.docx)).

---

## 2. Matriz de Mapeo de Formularios vs Tareas del BPMN

| # | Archivo de Formulario | ID Camunda Form | Tarea BPMN Vinculada | Grupo / Rol Asignado | Propósito Operativo |
|---|---|---|---|---|---|
| 01 | `form_01_lead_comercial.form` | `Form_01_LeadComercial` | `Task_CapturaLead` / `Task_Cli_Solicitud` | Ejecutivo Comercial / Cliente | Captura de requerimientos iniciales y caracterización del lead. |
| 02 | `form_02_evaluacion_viabilidad_arb.form` | `Form_02_EvaluacionViabilidadARB` | `Task_PreEvaluacionViabilidad` / `Task_ValidacionARB` | Jefe de Procesos / ARB | Pre-evaluación técnica y validación de arquitectura base. |
| 03 | `form_03_diagnostico_madurez_okrs.form` | `Form_03_DiagnosticoMadurezOKRs` | `Task_InformeMadurezOKRs` / `Task_Cli_Discover` | Jefe de Procesos / Data Auditor | Diagnóstico As-Is, Process Mining y definición de OKRs. |
| 04 | `form_04_formalizacion_finops_contrato.form` | `Form_04_FormalizacionFinOpsContrato` | `Task_FormalizarContrato` / `Task_Cli_FirmaContrato` | FinOps / Legal Counsel / Cliente | Modelado de costos Cloud, DPA y firma digital del contrato. |
| 05 | `form_05_sprint_planning_dor.form` | `Form_05_SprintPlanningDoR` | `Task_SprintPlanningDoR` / `Task_RefinarBacklog` | Product Owner / Revisor Agile | Planificación quincenal y verificación de Definition of Ready. |
| 06 | `form_06_gobierno_calidad_dato.form` | `Form_06_GobiernoCalidadDato` | `Task_ValidarGobernanza` | Data Steward | Certificación de calidad >99.5%, PII y linaje criptográfico. |
| 07 | `form_07_qa_signoff_dod.form` | `Form_07_QASignoffDoD` | `Task_PruebasQA` | QA Engineer / DevOps | Verificación de pruebas E2E, SonarQube y Definition of Done. |
| 08 | `form_08_aprobacion_entrega_firma.form` | `Form_08_AprobacionEntregaFirma` | `Task_SprintReviewDemo` / `Task_Cli_FirmaEntrega` | Revisor Agile / Cliente | Sprint Review, conformidad y firma electrónica de aprobación. |
| 09 | `form_09_gestion_incidentes_sev.form` | `Form_09_GestionIncidentesSev` | `Task_MitigacionIncidente` / `Task_Cli_ReportarIncidente` | DevOps / SRE On-Call | Clasificación Sev 1/2/3, control de SLA 15m y Post-Mortem. |
| 10 | `form_10_acelerador_innova_lab.form` | `Form_10_AceleradorInnovaLab` | `Task_PropuestaAcelerador` | Head of Innova Lab / Process Lead | Incubación de aceleradores técnicos y evolución metodológica. |

---

## 3. Especificación Detallada de Campos por Formulario

### Formulario 01: `form_01_lead_comercial.form`
- **Tarea Asociada**: `Task_CapturaLead` (BPMN-01)
- **Rol**: Ejecutivo Comercial (`Ejecutivo Comercial`)
- **Estructura de Componentes**:
  - `f_cliente_empresa` (textfield, requerido): Razón social o nombre comercial de la empresa.
  - `f_cliente_contacto` (textfield, requerido): Nombre y cargo del contacto clave.
  - `f_cliente_email` (textfield, requerido): Correo electrónico corporativo con validación sintáctica.
  - `f_sector_industrial` (select, requerido): Industria (Finanzas, Salud, Retail, Telecom, Logística, Energía, Gobierno).
  - `f_tipo_intervencion` (checklist): Áreas de interés (Lakehouse 3 Capas, Microservicios, Analítica/IA, BPMN, DAMA-BOK).
  - `f_volumen_datos_tb` (number, requerido): Estimación de volumen de datos en Terabytes.
  - `f_presupuesto_usd` (number, requerido): Presupuesto referencial de transformación en USD.
  - `f_urgencia_proyecto` (select, requerido): Nivel de urgencia (Baja, Media, Alta, Crítica).
  - `f_descripcion_desafio` (textarea, requerido): Descripción textual de los dolores operativos y objetivos.

---

### Formulario 02: `form_02_evaluacion_viabilidad_arb.form`
- **Tarea Asociada**: `Task_PreEvaluacionViabilidad` / `Task_ValidacionARB` (BPMN-01)
- **Rol**: Jefe de Procesos & Architecture Review Board (`Jefe de Procesos`, `Architecture Review Board`)
- **Estructura de Componentes**:
  - `cliente_empresa` (textfield, deshabilitado): Nombre del cliente importado de la variable de proceso.
  - `f_score_viabilidad` (number, requerido, mín: 1, máx: 100): Puntuación técnica de viabilidad.
  - `f_score_fit` (number, requerido, mín: 1, máx: 100): Puntuación de compatibilidad con el marco STF.
  - `f_topologia_arquitectura` (select, requerido): Arquitectura base recomendada (Lakehouse Medallion, EDA, Data Mesh, Híbrido).
  - `f_complejidad_estimada` (select, requerido): Grado de complejidad (Baja, Media, Alta, Muy Alta).
  - `f_riesgos_integracion` (textarea): Factores de riesgo identificados (sistemas legados, streaming, PII).
  - `f_dictamen_arb` (select, requerido): Aprobado para Diagnóstico, Condicionado, Rechazado.
  - `f_justificacion_arb` (textarea, requerido): Sustento técnico del dictamen y recomendación de Squad Lead.

---

### Formulario 03: `form_03_diagnostico_madurez_okrs.form`
- **Tarea Asociada**: `Task_InformeMadurezOKRs` (BPMN-02)
- **Rol**: Jefe de Procesos (`Jefe de Procesos`)
- **Estructura de Componentes**:
  - `f_madurez_datos` (select, requerido): Nivel de madurez de datos (Nivel 1 Reactivo a Nivel 5 Cognitivo).
  - `f_deuda_tecnica_score` (number, requerido): Índice de deuda técnica de 0 a 100.
  - `f_hallazgos_process_mining` (textarea, requerido): Resumen de cuellos de botella detectados en trazas de logs.
  - `f_okr_obj_1` (textfield, requerido): Primer objetivo estratégico de transformación.
  - `f_okr_kr_1` (textfield, requerido): Resultado clave cuantitativo asociado al OKR 1.
  - `f_okr_obj_2` (textfield): Segundo objetivo estratégico complementario.
  - `f_okr_kr_2` (textfield): Resultado clave cuantificable del OKR 2.
  - `f_diagnostico_firmado` (checkbox, requerido): Confirmación de acuerdo del cliente sobre el diagnóstico.

---

### Formulario 04: `form_04_formalizacion_finops_contrato.form`
- **Tarea Asociada**: `Task_FormalizarContrato` (BPMN-03)
- **Rol**: Especialista FinOps & Legal Counsel (`FinOps`, `Legal Counsel`)
- **Estructura de Componentes**:
  - `f_capex_usd` (number, requerido): Inversión inicial estimada para el despliegue.
  - `f_opex_cloud_usd` (number, requerido): Costo operativo mensual proyectado de nube.
  - `f_cloud_provider` (select, requerido): Proveedor cloud primario (AWS, Azure, GCP, Multicloud).
  - `f_modelo_contrato` (select, requerido): Modalidad (Squad Dedicado Quincenal, Híbrido, Hitos Modulares).
  - `f_dpa_aprobado` (checkbox, requerido): Certificación de cumplimiento del Data Processing Agreement.
  - `f_soberania_dato` (checkbox, requerido): Declaración de residencia geográfica y soberanía de los datos.
  - `f_hash_contrato` (textfield, requerido): Hash SHA-256 del documento contractual formal.
  - `f_contrato_firmado_cliente` (checkbox, requerido): Verificación de firma digital del cliente en la App.

---

### Formulario 05: `form_05_sprint_planning_dor.form`
- **Tarea Asociada**: `Task_SprintPlanningDoR` (BPMN-04 / BPMN-06)
- **Rol**: Product Owner & Revisor Agile (`Product Owner`, `Revisor Agile / PO`)
- **Estructura de Componentes**:
  - `f_sprint_num` (number, requerido): Número correlativo del Sprint (ej. 1, 2, 3...).
  - `f_squad_id` (textfield, requerido): Código identificador de la célula Squad (ej. SQ-DATA-01).
  - `f_sprint_goal` (textarea, requerido): Objetivo unificado del Sprint para Datos y Software.
  - `f_story_points` (number, requerido): Puntos de historia totales comprometidos en la iteración.
  - `f_dor_gherkin` (checkbox, requerido): Criterios de aceptación estructurados en formato Dado/Cuando/Entonces.
  - `f_dor_esquemas` (checkbox, requerido): Esquemas de datos validados en el Data Catalog corporativo.
  - `f_dor_apis` (checkbox, requerido): Contratos de OpenAPI / AsyncAPI formalmente definidos.
  - `f_dor_dependencias` (checkbox, requerido): Confirmación de ausencia de dependencias bloqueantes externas.
  - `f_dor_aprobado` (select, requerido): Aprobado (Sprint inicia) o Rechazado (Retorna a Refinamiento).

---

### Formulario 06: `form_06_gobierno_calidad_dato.form`
- **Tarea Asociada**: `Task_ValidarGobernanza` (BPMN-04 / BPMN-05)
- **Rol**: Data Steward (`Data Steward`)
- **Estructura de Componentes**:
  - `f_dataset_id` (textfield, requerido): Nombre del dataset o tabla Delta/Iceberg.
  - `f_capa_datos` (select, requerido): Capa evaluada (Bronze Raw, Silver Curated, Gold Semantic).
  - `f_clasificacion_seguridad` (select, requerido): Clasificación (Público, Interno, Confidencial, PII Restringido).
  - `f_calidad_ok` (checkbox, requerido): Pruebas de completitud, tipo y unicidad superadas (>99.5%).
  - `f_linaje_ok` (checkbox, requerido): Linaje criptográfico inmutable asentado en OpenLineage / Atlas.
  - `f_cifrado_ok` (checkbox, requerido): Enmascaramiento y cifrado AES-256 en reposo verificado.
  - `f_dictamen_steward` (select, requerido): Aprobado, No Conforme (Enviar a DLQ), o Bloqueado por PII.
  - `f_obs_steward` (textarea): Comentarios técnicos y directrices del Data Steward.

---

### Formulario 07: `form_07_qa_signoff_dod.form`
- **Tarea Asociada**: `Task_PruebasQA` (BPMN-06)
- **Rol**: QA Engineer & DevOps (`QA Engineer`, `DevOps`)
- **Estructura de Componentes**:
  - `f_release_tag` (textfield, requerido): Tag semántico de versión en Git (ej. v1.4.0).
  - `f_pr_url` (textfield, requerido): Enlace al Pull Request aprobado en GitHub / GitLab.
  - `f_cobertura_tests` (number, requerido, mín: 80, máx: 100): Porcentaje de cobertura de pruebas unitarias.
  - `f_sonarqube_status` (select, requerido): Estado de SonarQube (PASSED o FAILED).
  - `f_staging_ok` (checkbox, requerido): Pruebas de humo en Staging (Kubernetes) superadas.
  - `f_e2e_ok` (checkbox, requerido): Batería de pruebas funcionales automatizadas E2E sin fallos.
  - `f_dod_aprobado` (checkbox, requerido): Certificación de cumplimiento integral de la Definition of Done.
  - `f_notas_release` (textarea): Notas de release y observaciones de calidad.

---

### Formulario 08: `form_08_aprobacion_entrega_firma.form`
- **Tarea Asociada**: `Task_SprintReviewDemo` / `Task_Cli_FirmaEntrega` (BPMN-07)
- **Rol**: Cliente / Usuario & Revisor Agile (`Cliente / Firmante Autorizado`, `Revisor Agile`)
- **Estructura de Componentes**:
  - `f_cliente_firmante` (textfield, requerido): Nombre del representante legal o PO del cliente.
  - `f_hito_aprobado` (textfield, requerido): Sprint o entregable sometido a validación formal.
  - `f_conformidad_criterios` (select, requerido): Aceptado Totalmente, Aceptado con Observaciones, Rechazado.
  - `f_nps_score` (number, requerido, mín: 1, máx: 10): Calificación Net Promoter Score del Sprint.
  - `f_mecanismo_firma` (select, requerido): Firma FIDO2 / Biometría en App, Certificado PKI X.509, OTP OIDC.
  - `f_autoriza_factura` (checkbox, requerido): Consentimiento expreso para la emisión inmediata de factura ERP.
  - `f_feedback_cliente` (textarea): Retroalimentación cualitativa para el Squad.

---

### Formulario 09: `form_09_gestion_incidentes_sev.form`
- **Tarea Asociada**: `Task_MitigacionIncidente` (BPMN-08)
- **Rol**: DevOps / SRE On-Call (`DevOps / SRE On-Call`)
- **Estructura de Componentes**:
  - `f_incidente_id` (textfield, requerido): Identificador de ticket o alerta (ej. INC-2026-0891).
  - `f_componente_impactado` (select, requerido): Subsistema afectado (Ingesta C1, Silver C2, Gold/BI C3, APIs, App Cliente, K8s).
  - `f_severidad_nivel` (select, requerido): Nivel (Sev 1 Crítico, Sev 2 Mayor, Sev 3 Menor).
  - `f_sla_cumplido` (checkbox, requerido): Verificación de respuesta inicial antes de los 15 minutos (para Sev 1).
  - `f_mitigacion_inmediata` (textarea, requerido): Acciones técnicas inmediatas ejecutadas para contener el fallo.
  - `f_causa_raiz_rca` (textarea, requerido): Análisis de causa raíz RCA (técnica de los 5 Porqués).
  - `f_plan_preventivo` (textarea, requerido): Medidas correctivas definitivas para evitar recurrencia.
  - `f_estado_incidente` (select, requerido): Resuelto y Verificado, En Monitoreo, o Escalado a Junta Directiva.

---

### Formulario 10: `form_10_acelerador_innova_lab.form`
- **Tarea Asociada**: `Task_PropuestaAcelerador` (BPMN-09)
- **Rol**: Head of Innova Lab & Process Lead (`Head of Innova Lab`, `Jefe de Procesos`)
- **Estructura de Componentes**:
  - `f_acelerador_nombre` (textfield, requerido): Nombre del componente o plantilla a incubar.
  - `f_acelerador_categoria` (select, requerido): Categoría (Conector Ingesta C1, Template dbt C2/C3, Pipeline IaC, Modelo MLOps, SDK UI).
  - `f_friccion_detectada` (textarea, requerido): Cuello de botella recurrente identificado en los Sprints.
  - `f_ahorro_horas` (number, requerido): Estimación de horas hombre ahorradas por Sprint con el acelerador.
  - `f_metrica_dora` (select, requerido): Métrica DORA optimizada (Deployment Frequency, Lead Time, CFR, MTTR).
  - `f_version_stf` (textfield, requerido): Versión del marco STF beneficiada (ej. STF 2.1).
  - `f_dictamen_innova` (select, requerido): Aprobado para Incubación, Publicado en Ecosistema, o Archivado.

---

## 4. Guía de Importación y Ejecución en Camunda

1. **Apertura en Camunda Desktop Modeler**:
   - Abrir el archivo `bpmn/statsfirm_organizacion_procesos.bpmn`.
   - Abrir simultáneamente cualquiera de los archivos `.form` de la carpeta `bpmn/forms/`.
   - El modeler reconocerá automáticamente las referencias `camunda:formRef` asignadas a cada User Task.
2. **Despliegue en Camunda Platform 7 / 8**:
   - En Camunda Modeler, hacer clic en el botón de despliegue (**Deploy Current Diagram**).
   - Incluir los 10 archivos `.form` en el mismo despliegue para garantizar la resolución estricta de formularios en tiempo de ejecución.
   - En **Camunda Tasklist**, cada especialista visualizará su bandeja de entrada de tareas filtrada por `candidateGroups` con el formulario renderizado y validaciones en tiempo real.
