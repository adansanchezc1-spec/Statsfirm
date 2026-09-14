const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');

const candidateFormsDirs = [
  path.resolve(__dirname, '../../docs_landing_page/bpmn/forms'),
  path.resolve(__dirname, '../docs_landing_page/bpmn/forms'),
  path.resolve(__dirname, '../../bpmn/forms')
];
const formsDir = candidateFormsDirs.find(d => fs.existsSync(d)) || candidateFormsDirs[0];

const candidateBpmnFiles = [
  path.resolve(__dirname, '../../docs_landing_page/bpmn/statsfirm_organizacion_procesos.bpmn'),
  path.resolve(__dirname, '../docs_landing_page/bpmn/statsfirm_organizacion_procesos.bpmn'),
  path.resolve(__dirname, '../../bpmn/statsfirm_organizacion_procesos.bpmn')
];
const bpmnFile = candidateBpmnFiles.find(f => fs.existsSync(f)) || candidateBpmnFiles[0];

// Simulated active workflow instances
let workflowLog = [
  {
    instanceId: 'INST-STF-001',
    process: 'BPMN-01: Captación & Calificación Comercial',
    currentTask: 'Task_CapturaLead',
    taskName: 'Captura de Requerimientos Iniciales',
    formRef: 'form_01_lead_comercial.form',
    candidateGroup: 'Ejecutivo Comercial',
    status: 'COMPLETED',
    timestamp: '2026-09-01 08:30 UTC'
  },
  {
    instanceId: 'INST-STF-001',
    process: 'BPMN-02: Diagnóstico Inicial & OKRs',
    currentTask: 'Task_InformeMadurezOKRs',
    taskName: 'Diagnóstico de Madurez Digital y OKRs',
    formRef: 'form_03_diagnostico_madurez_okrs.form',
    candidateGroup: 'Jefe de Procesos',
    status: 'COMPLETED',
    timestamp: '2026-09-03 14:15 UTC'
  },
  {
    instanceId: 'INST-STF-001',
    process: 'BPMN-03: FinOps & Contratación',
    currentTask: 'Task_FormalizarContrato',
    taskName: 'Modelado FinOps y Formalización Contractual',
    formRef: 'form_04_formalizacion_finops_contrato.form',
    candidateGroup: 'FinOps & Legal',
    status: 'COMPLETED',
    timestamp: '2026-09-04 16:00 UTC'
  },
  {
    instanceId: 'INST-STF-001',
    process: 'BPMN-04 & 06: Ejecución Sincronizada (Datos + SW)',
    currentTask: 'Task_ValidarGobernanza',
    taskName: 'Validación de Gobernanza y Linaje Criptográfico',
    formRef: 'form_06_gobierno_calidad_dato.form',
    candidateGroup: 'Data Steward',
    status: 'ACTIVE_PENDING',
    timestamp: '2026-09-06 10:00 UTC'
  }
];

// GET /api/bpmn/forms (List of all 10 Camunda forms)
router.get('/forms', (req, res) => {
  try {
    if (!fs.existsSync(formsDir)) {
      return res.status(404).json({ success: false, error: 'Directorio de formularios no encontrado' });
    }

    const files = fs.readdirSync(formsDir).filter(f => f.endsWith('.form'));
    const formSummaries = files.map(file => {
      const filePath = path.join(formsDir, file);
      const raw = fs.readFileSync(filePath, 'utf-8');
      const json = JSON.parse(raw);
      return {
        filename: file,
        formId: json.id,
        schemaVersion: json.schemaVersion,
        title: json.components && json.components[0] ? json.components[0].text.split('\n')[0].replace('# ', '') : file,
        fieldCount: json.components ? json.components.filter(c => c.type !== 'text').length : 0
      };
    });

    res.json({ success: true, count: formSummaries.length, forms: formSummaries });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/bpmn/forms/:formKey
router.get('/forms/:formKey', (req, res) => {
  try {
    let { formKey } = req.params;
    if (!formKey.endsWith('.form')) {
      formKey += '.form';
    }

    const filePath = path.join(formsDir, formKey);
    if (!fs.existsSync(filePath)) {
      return res.status(404).json({ success: false, error: `Formulario '${formKey}' no encontrado` });
    }

    const raw = fs.readFileSync(filePath, 'utf-8');
    const schema = JSON.parse(raw);
    res.json({ success: true, formKey, schema });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/bpmn/tasks/submit (Submit Camunda user task form)
router.post('/tasks/submit', (req, res) => {
  try {
    const { formKey, formData, taskId, processInstanceId } = req.body;

    if (!formKey || !formData) {
      return res.status(400).json({ success: false, error: 'formKey y formData son obligatorios' });
    }

    const executionRecord = {
      instanceId: processInstanceId || 'INST-STF-001',
      taskId: taskId || `TSK-${Date.now()}`,
      formKey,
      submittedBy: req.body.submittedBy || 'Alejandro Morales (Cliente)',
      submittedAt: new Date().toISOString(),
      status: 'PROCESSED_SUCCESS',
      variablesReceived: Object.keys(formData).length,
      nextRecommendedTask: 'Avanzado automáticamente por el orquestador Camunda Zeebe'
    };

    workflowLog.unshift(executionRecord);

    res.json({
      success: true,
      data: executionRecord,
      message: `Formulario Camunda '${formKey}' procesado con éxito. Estado del flujo actualizado.`
    });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/bpmn/instances (Workflow log)
router.get('/instances', (req, res) => {
  res.json({ success: true, log: workflowLog });
});

// GET /api/bpmn/xml (Raw BPMN 2.0 XML)
router.get('/xml', (req, res) => {
  try {
    if (!fs.existsSync(bpmnFile)) {
      return res.status(404).json({ success: false, error: 'Archivo BPMN no encontrado' });
    }
    const xml = fs.readFileSync(bpmnFile, 'utf-8');
    res.setHeader('Content-Type', 'application/xml');
    res.send(xml);
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
