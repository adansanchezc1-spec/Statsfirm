/**
 * STATSFIRM CO. — LEADS & INQUIRIES DATA STORE
 * Operates the Commercial Lead Capture Workflow (BPMN-01)
 */

const leads = [
  {
    id: 'LEAD-2026-1001',
    ticketId: 'LEAD-2026-1001',
    companyName: 'Fintech Andes Corp.',
    contactName: 'Carlos Santillana',
    email: 'csantillana@fintechandes.com',
    phone: '+57 310 987 6543',
    industry: 'Finanzas & Banca',
    services: ['data-engineering', 'ai-data-science'],
    dataVolumeTB: 12,
    budgetUSD: 45000,
    urgency: 'alta',
    challengeDescription: 'Modernización de DWH legado hacia Data Lakehouse Medallion con modelos de predicción de riesgo crediticio en tiempo real.',
    score: 88,
    priority: 'ALTA',
    status: 'QUALIFIED_FOR_ARB',
    assignedTo: 'Mateo Arismendi (Jefe de Procesos)',
    createdAt: '2026-09-05 14:22:10 UTC'
  }
];

function registerLead(leadData) {
  const id = `LEAD-2026-${Math.floor(1000 + Math.random() * 9000)}`;

  // BPMN-01 Lead Qualification Scoring Algorithm
  let score = 50;
  const budget = parseFloat(leadData.budgetCOP || leadData.budgetUSD || leadData.budgetUsd) || 0;
  const volume = parseFloat(leadData.dataVolumeTB || leadData.dataVolumeTb) || 0;
  const services = Array.isArray(leadData.services || leadData.servicesInterested) 
    ? (leadData.services || leadData.servicesInterested) 
    : [];

  if (budget >= 20000000 || (budget >= 30000 && budget < 1000000)) score += 20;
  else if (budget >= 10000000 || (budget >= 15000 && budget < 1000000)) score += 10;

  if (volume >= 5) score += 15;
  if (services.length >= 2) score += 10;
  if (leadData.urgency === 'alta' || leadData.urgency === 'inmediata' || leadData.urgency === 'critica') score += 5;

  score = Math.min(100, score);
  const priority = score >= 75 ? 'ALTA' : (score >= 60 ? 'MEDIA' : 'ESTÁNDAR');
  const qualified = score >= 60;

  const newLead = {
    id,
    ticketId: id,
    companyName: leadData.companyName || leadData.company || 'Empresa Confidencial',
    contactName: leadData.contactName || 'Contacto Comercial',
    email: leadData.email || leadData.contactEmail || '',
    phone: leadData.phone || leadData.contactPhone || 'No especificado',
    industry: leadData.industry || 'General',
    services,
    dataVolumeTB: volume,
    budgetUSD: budget,
    urgency: leadData.urgency || 'estandar',
    challengeDescription: leadData.challengeDescription || 'Sin descripción detallada.',
    score,
    priority,
    status: qualified ? 'QUALIFIED_FOR_ARB' : 'IN_REVIEW',
    assignedTo: qualified ? 'Jefe de Procesos & ARB Board' : 'Ejecutivo Comercial Senior',
    createdAt: new Date().toISOString().replace('T', ' ').substring(0, 19) + ' UTC'
  };

  leads.unshift(newLead);
  return newLead;
}

function getAllLeads() {
  return leads;
}

module.exports = {
  leads,
  registerLead,
  getAllLeads
};
