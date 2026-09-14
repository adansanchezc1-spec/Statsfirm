/**
 * @file contact.js
 * @description REST endpoints for commercial contact intake and interactive quote calculation.
 * Statsfirm Co. - Official Commercial Web Platform.
 * Follows BPMN-01: Proceso de Captación y Calificación de Leads Comerciales.
 */

const express = require('express');
const router = express.Router();
const leadsStore = require('../data/leadsStore');
const servicesCatalog = require('../data/servicesCatalog');

/**
 * POST /api/contact
 * Receives commercial intake form submissions per BPMN-01.
 */
router.post('/contact', (req, res) => {
  try {
    const {
      companyName,
      contactName,
      email,
      phone,
      industry,
      services,
      dataVolumeTB,
      budgetUSD,
      budgetCOP,
      urgency,
      challengeDescription,
      notes
    } = req.body;

    // Validation
    if (!companyName || !contactName || !email) {
      return res.status(400).json({
        success: false,
        error: 'Campos requeridos faltantes: Nombre de Empresa, Nombre de Contacto y Correo Corporativo son obligatorios.'
      });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        success: false,
        error: 'El formato del correo corporativo es inválido.'
      });
    }

    const leadData = {
      companyName: String(companyName).trim(),
      contactName: String(contactName).trim(),
      email: String(email).trim().toLowerCase(),
      phone: phone ? String(phone).trim() : 'No especificado',
      industry: industry || 'No especificada',
      services: Array.isArray(services) ? services : (services ? [services] : []),
      dataVolumeTB: parseFloat(dataVolumeTB) || 0,
      budgetCOP: parseFloat(budgetCOP || budgetUSD) || 0,
      budgetUSD: parseFloat(budgetUSD || budgetCOP) || 0,
      urgency: urgency || 'estandar',
      challengeDescription: challengeDescription ? String(challengeDescription).trim() : '',
      notes: notes || ''
    };

    const newLead = leadsStore.registerLead(leadData);

    return res.status(201).json({
      success: true,
      message: 'Solicitud comercial registrada exitosamente bajo protocolo BPMN-01.',
      ticket: newLead.id,
      data: {
        id: newLead.id,
        createdAt: newLead.createdAt,
        companyName: newLead.companyName,
        contactName: newLead.contactName,
        score: newLead.score,
        priority: newLead.priority,
        slaHours: newLead.priority === 'ALTA' ? 2 : (newLead.priority === 'MEDIA' ? 8 : 24),
        nextStep: 'Un Director de Arquitectura y Negocios de Statsfirm Co. coordinará la sesión de descubrimiento técnico en el plazo de SLA asignado.'
      }
    });
  } catch (error) {
    console.error('[Contact Error]', error);
    return res.status(500).json({
      success: false,
      error: 'Error interno del servidor procesando el requerimiento comercial.'
    });
  }
});

/**
 * POST /api/quote
 * Calculates estimated project scope, recommended squad, and investment range.
 */
router.post('/quote', (req, res) => {
  try {
    const { selectedServices = [], dataVolumeTB = 1, urgency = 'estandar', engagementModel = 'squad' } = req.body;

    if (!Array.isArray(selectedServices) || selectedServices.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Debe seleccionar al menos un servicio del catálogo para estimar el proyecto.'
      });
    }

    // Base pricing algorithm based on selected service lines
    let baseCapexMin = 0;
    let baseCapexMax = 0;
    let baseWeeksMin = 0;
    let baseWeeksMax = 0;
    let matchedServices = [];

    const serviceLines = servicesCatalog.serviceLines || [];

    selectedServices.forEach(srvId => {
      const srv = serviceLines.find(s => s.id === srvId);
      const name = srv ? srv.title : srvId;
      matchedServices.push(name);

      switch (srvId) {
        case 'data-engineering':
        case 'data-intelligence':
          baseCapexMin += 12000;
          baseCapexMax += 28000;
          baseWeeksMin += 6;
          baseWeeksMax += 12;
          break;
        case 'bi-analytics':
        case 'business-intelligence':
          baseCapexMin += 8000;
          baseCapexMax += 18000;
          baseWeeksMin += 4;
          baseWeeksMax += 8;
          break;
        case 'ai-data-science':
          baseCapexMin += 15000;
          baseCapexMax += 35000;
          baseWeeksMin += 8;
          baseWeeksMax += 16;
          break;
        case 'software-cloud':
          baseCapexMin += 14000;
          baseCapexMax += 30000;
          baseWeeksMin += 6;
          baseWeeksMax += 14;
          break;
        case 'process-engineering':
          baseCapexMin += 7000;
          baseCapexMax += 16000;
          baseWeeksMin += 4;
          baseWeeksMax += 8;
          break;
        default:
          baseCapexMin += 6000;
          baseCapexMax += 12000;
          baseWeeksMin += 4;
          baseWeeksMax += 6;
      }
    });

    // Volume multiplier (TB scaling)
    const vol = parseFloat(dataVolumeTB) || 1;
    let volMultiplier = 1.0;
    if (vol > 100) volMultiplier = 1.45;
    else if (vol > 20) volMultiplier = 1.25;
    else if (vol > 5) volMultiplier = 1.10;

    // Urgency multiplier
    let urgencyMultiplier = 1.0;
    let timelineFactor = 1.0;
    if (urgency === 'inmediata') {
      urgencyMultiplier = 1.25;
      timelineFactor = 0.70;
    } else if (urgency === 'alta') {
      urgencyMultiplier = 1.12;
      timelineFactor = 0.85;
    }

    // Synergy discount for bundled multi-discipline engagements
    let synergyDiscount = 1.0;
    if (selectedServices.length >= 4) synergyDiscount = 0.82;
    else if (selectedServices.length >= 2) synergyDiscount = 0.90;

    // Calculated final values
    const estimatedCapexMin = Math.round(baseCapexMin * volMultiplier * urgencyMultiplier * synergyDiscount);
    const estimatedCapexMax = Math.round(baseCapexMax * volMultiplier * urgencyMultiplier * synergyDiscount);
    const estimatedWeeksMin = Math.max(3, Math.round(baseWeeksMin * timelineFactor));
    const estimatedWeeksMax = Math.max(5, Math.round(baseWeeksMax * timelineFactor));

    // Recommend squad configuration
    let recommendedSquad = 'Squad Especializado Ágil (3-4 profesionales)';
    if (selectedServices.length >= 3 || vol > 20) {
      recommendedSquad = 'Squad Enterprise Multidisciplinario (5-7 roles: Lead Architect, Data Engineers, BI/ML Specialists, Scrum Master)';
    }

    return res.json({
      success: true,
      quote: {
        matchedServices,
        dataVolumeTB: vol,
        urgency,
        engagementModel,
        estimatedInvestmentUSD: {
          min: estimatedCapexMin,
          max: estimatedCapexMax,
          currency: 'USD',
          formatted: `$${estimatedCapexMin.toLocaleString('en-US')} - $${estimatedCapexMax.toLocaleString('en-US')} USD`
        },
        estimatedTimelineWeeks: {
          min: estimatedWeeksMin,
          max: estimatedWeeksMax,
          formatted: `${estimatedWeeksMin} a ${estimatedWeeksMax} semanas`
        },
        recommendedSquad,
        stfMethodologyStages: [
          'Fase 1: Diagnóstico & Blueprint Arquitectónico (Semanas 1-2)',
          'Fase 2: Implementación de Fundaciones & MVP de Valor (Semanas 3-6)',
          'Fase 3: Escalamiento e Integración Productiva',
          'Fase 4: Gobierno Continuo, MLOps y Transferencia Tecnológica'
        ],
        disclaimer: 'Esta estimación es referencial. El alcance definitivo, cronograma e inversión se consolidan tras la sesión de descubrimiento técnico (BPMN-01.03).'
      }
    });
  } catch (error) {
    console.error('[Quote Error]', error);
    return res.status(500).json({
      success: false,
      error: 'Error calculando la cotización paramétrica.'
    });
  }
});

/**
 * GET /api/leads
 * Returns summary of captured leads (for demonstration/admin audit).
 */
router.get('/leads', (req, res) => {
  const allLeads = leadsStore.getAllLeads();
  res.json({
    success: true,
    total: allLeads.length,
    leads: allLeads
  });
});

module.exports = router;
