const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');
const store = require('../data/mockStore');

// GET /api/project
router.get('/project', (req, res) => {
  res.json({ success: true, data: store.project });
});

// GET /api/telemetry
router.get('/telemetry', (req, res) => {
  res.json({
    success: true,
    data: {
      project: store.project,
      sprints: store.sprints,
      pipelineHealth: store.pipelineHealth
    }
  });
});

// GET /api/squad
router.get('/squad', (req, res) => {
  res.json({ success: true, data: store.squad });
});

// GET & POST /api/messages (Squad Chat)
router.get('/messages', (req, res) => {
  res.json({ success: true, data: store.messages });
});

router.post('/messages', (req, res) => {
  const { text } = req.body;
  if (!text || text.trim() === '') {
    return res.status(400).json({ success: false, error: 'Mensaje requerido' });
  }

  const userMsg = {
    id: store.messages.length + 1,
    sender: 'Alejandro Morales (Cliente)',
    role: 'Client Sponsor',
    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    text: text.trim()
  };
  store.messages.push(userMsg);

  // Simulated auto-response from Squad Leaders
  setTimeout(() => {
    const responses = [
      {
        sender: 'Elena Vance (Revisor Agile)',
        role: 'Scrum Master',
        text: `Recibido Alejandro. He registrado tu observación en el Backlog Refinement del Squad. Mañana lo revisamos en la Daily sincronizada.`
      },
      {
        sender: 'Mateo Arismendi (Jefe de Procesos)',
        role: 'Process Lead',
        text: `Comprendido. Validaremos con el Data Steward el impacto sobre el contrato de datos antes del cierre del Sprint.`
      }
    ];
    const pick = responses[Math.floor(Math.random() * responses.length)];
    store.messages.push({
      id: store.messages.length + 1,
      sender: pick.sender,
      role: pick.role,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      text: pick.text
    });
  }, 1000);

  res.json({ success: true, data: userMsg });
});

// POST /api/diagnostico/calculate
router.post('/diagnostico/calculate', (req, res) => {
  const {
    dataMaturity,
    processMaturity,
    volumeTb,
    systemsCount,
    servicesSelected,
    urgency
  } = req.body;

  const dMat = parseInt(dataMaturity) || 2;
  const pMat = parseInt(processMaturity) || 2;
  const vol = parseFloat(volumeTb) || 5;
  const sys = parseInt(systemsCount) || 4;
  const services = Array.isArray(servicesSelected) ? servicesSelected : [];

  // Readiness index algorithm: 0 to 100
  let readinessScore = Math.min(100, Math.round((dMat * 10) + (pMat * 10) + (Math.min(vol, 20) * 1.5) + (services.length * 5)));

  let maturityLabel = 'Nivel 2: Gestionado (Silos)';
  if (readinessScore >= 80) maturityLabel = 'Nivel 5: Cognitivo / Inteligencia Continua';
  else if (readinessScore >= 65) maturityLabel = 'Nivel 4: Cuantitativo / MLOps';
  else if (readinessScore >= 45) maturityLabel = 'Nivel 3: Estandarizado / Lakehouse 3 Capas';
  else if (readinessScore < 30) maturityLabel = 'Nivel 1: Inicial / Reactivo';

  // FinOps Estimation Algorithm
  const baseCapex = 18000 + (services.length * 6500) + (sys * 1200);
  const baseMonthlyOpex = 950 + (vol * 85) + (services.length * 450);

  res.json({
    success: true,
    data: {
      readinessScore,
      maturityLabel,
      estimatedCapexUsd: baseCapex,
      estimatedMonthlyOpexUsd: baseMonthlyOpex,
      recommendedSquad: 'Squad Multidisciplinario Dedicado (10-12 especialistas)',
      cadence: 'Sprints quincenales sincronizados de 2 semanas',
      qualityGates: ['Definition of Ready (DoR)', 'Definition of Done (DoD)', 'Linaje DAMA-BOK']
    }
  });
});

// GET /api/vault
router.get('/vault', (req, res) => {
  res.json({ success: true, data: store.vault });
});

// GET /api/vault/download/:docId
router.get('/vault/download/:docId', (req, res) => {
  const { docId } = req.params;
  const basePath = path.resolve(__dirname, '../../');

  if (docId === 'bpmn') {
    const bpmnFile = path.join(basePath, 'bpmn/statsfirm_organizacion_procesos.bpmn');
    if (fs.existsSync(bpmnFile)) {
      return res.download(bpmnFile, 'statsfirm_organizacion_procesos.bpmn');
    }
  }

  // Generic sample download
  const sampleContent = `STATSFIRM CO. - DOCUMENTO DE ALTA INGENIERIA\nID: ${docId}\nFecha: ${new Date().toISOString()}\nHash SHA-256: ${crypto.createHash('sha256').update(docId).digest('hex')}\n`;
  res.setHeader('Content-disposition', `attachment; filename=SFC-${docId.toUpperCase()}.txt`);
  res.setHeader('Content-type', 'text/plain');
  res.send(sampleContent);
});

// GET & POST /api/approvals (Digital Signatures & DoD)
router.get('/approvals', (req, res) => {
  res.json({
    success: true,
    pending: store.pendingApprovals,
    history: store.signedApprovalsHistory
  });
});

router.post('/approvals/sign', (req, res) => {
  const { approvalId, signerName, signerRole, signatureType, npsScore, feedback } = req.body;

  const itemIndex = store.pendingApprovals.findIndex(a => a.id === approvalId);
  if (itemIndex === -1) {
    return res.status(404).json({ success: false, error: 'Entregable no encontrado' });
  }

  const item = store.pendingApprovals[itemIndex];
  const timestamp = new Date().toISOString();
  const signaturePayload = `${item.id}|${item.sprint}|${signerName}|${timestamp}|STATSFIRM_CERT`;
  const signatureHash = crypto.createHash('sha256').update(signaturePayload).digest('hex');

  const signedRecord = {
    ...item,
    status: 'SIGNED_AND_INVOICED',
    signedAt: timestamp,
    signerName: signerName || 'Ing. Alejandro Morales',
    signerRole: signerRole || 'Head of Engineering / Client Sponsor',
    signatureType: signatureType || 'Firma Electrónica Avanzada FIDO2 / Biometría',
    signatureHash,
    npsScore: npsScore || 10,
    feedback: feedback || 'Incremento validado conforme a DoD sin observaciones.',
    invoiceNumber: `INV-2026-${Math.floor(1000 + Math.random() * 9000)}`,
    invoiceStatus: 'GENERATED_ERP_SENT'
  };

  store.pendingApprovals.splice(itemIndex, 1);
  store.signedApprovalsHistory.unshift(signedRecord);

  res.json({
    success: true,
    data: signedRecord,
    message: 'Entregable aprobado con Firma Electrónica Avanzada. Factura electrónica emitida en ERP.'
  });
});

// GET & POST /api/incidents (Support & SLAs)
router.get('/incidents', (req, res) => {
  res.json({ success: true, data: store.incidents });
});

router.post('/incidents', (req, res) => {
  const { title, severity, component, description } = req.body;

  if (!title || !severity) {
    return res.status(400).json({ success: false, error: 'Título y severidad requeridos' });
  }

  const newIncident = {
    id: `INC-2026-${Math.floor(1000 + Math.random() * 9000)}`,
    title,
    severity: severity || 'Sev 2',
    component: component || 'Microservicios Core / API Gateway',
    reportedAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
    status: 'ACTIVE_TRIAGE',
    slaMinutesTarget: severity === 'Sev 1' ? 15 : severity === 'Sev 2' ? 60 : 240,
    slaExpiresAt: new Date(Date.now() + (severity === 'Sev 1' ? 15 : severity === 'Sev 2' ? 60 : 240) * 60000).toISOString(),
    description: description || 'Incidente reportado desde la consola del cliente.',
    sreOnCallAssigned: 'Tomás Echeverry (DevOps/SRE Lead)'
  };

  store.incidents.unshift(newIncident);

  res.json({
    success: true,
    data: newIncident,
    message: 'Incidente registrado. SLA de respuesta inicial activado.'
  });
});

module.exports = router;
