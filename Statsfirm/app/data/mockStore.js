/**
 * Statsfirm Co. - In-Memory State & Mock Store
 * Stores state for Sprints, Telemetry, Squad Members, Document Vault,
 * Digital Approvals, and Support Incidents.
 */

const fs = require('fs');
const path = require('path');

const store = {
  project: {
    id: 'PRJ-STF-2026-01',
    name: 'Transformación Analítica Corporativa & Lakehouse 3 Capas',
    clientCompany: 'Global Fintech Corp.',
    clientUser: 'Ing. Alejandro Morales (Head of Engineering)',
    currentSprint: 'Sprint 04 (Iteración Quincenal)',
    status: 'ACTIVE_EXECUTION',
    uptimeSla: '99.98%',
    activePhase: 'STF Fase 4: CURATE & Capa 2 Silver'
  },

  sprints: {
    activeSprintNum: 4,
    sprintGoal: 'Consolidación de Transformaciones dbt en Capa 2 Silver, Linaje Criptográfico y Exposición de API GraphQL en Staging',
    storyPointsCommitted: 48,
    storyPointsCompleted: 38,
    daysRemaining: 4,
    totalDays: 10,
    dorStatus: 'APPROVED_100%',
    dodTargetStatus: 'IN_QA_VALIDATION',
    burndown: [
      { day: 'Día 1', ideal: 48, actual: 48 },
      { day: 'Día 2', ideal: 43.2, actual: 46 },
      { day: 'Día 3', ideal: 38.4, actual: 42 },
      { day: 'Día 4', ideal: 33.6, actual: 35 },
      { day: 'Día 5', ideal: 28.8, actual: 30 },
      { day: 'Día 6', ideal: 24.0, actual: 22 },
      { day: 'Día 7', ideal: 19.2, actual: 16 },
      { day: 'Día 8 (Hoy)', ideal: 14.4, actual: 10 }
    ],
    gantt: [
      { id: 'TSK-101', task: 'Ingesta Streaming Kafka Capa 1', owner: 'Ingeniería de Datos', progress: 100, status: 'DONE' },
      { id: 'TSK-102', task: 'Modelos dbt Silver y Desduplicación', owner: 'Ingeniería de Datos', progress: 90, status: 'IN_PROGRESS' },
      { id: 'TSK-103', task: 'Validación de Linaje y Máscaras PII', owner: 'Data Steward', progress: 85, status: 'IN_PROGRESS' },
      { id: 'TSK-104', task: 'Microservicios Core BFF & GraphQL', owner: 'Desarrollo Software', progress: 95, status: 'IN_PROGRESS' },
      { id: 'TSK-105', task: 'Pipeline SonarQube & K8s Staging', owner: 'DevOps / DataOps', progress: 100, status: 'DONE' },
      { id: 'TSK-106', task: 'Batería de Pruebas Funcionales E2E', owner: 'QA Engineer', progress: 70, status: 'IN_PROGRESS' }
    ]
  },

  pipelineHealth: {
    capa1Bronze: {
      name: 'Capa 1: Ingesta & Raw Bronze',
      status: 'HEALTHY',
      throughput: '1.42 GB/s',
      recordsProcessedToday: '42,850,120',
      schemaCompliancePct: 99.99,
      dlqQueueCount: 0,
      protocolSupport: ['Kafka', 'MQTT', 'REST API', 'Batch S3']
    },
    capa2Silver: {
      name: 'Capa 2: Curated & Enriched Silver',
      status: 'HEALTHY',
      dbtTestPassRatePct: 99.85,
      deduplicationEfficiency: '99.92%',
      lineageRegistered: true,
      deltaTablesActive: 14,
      lastCuratedTimestamp: new Date().toISOString()
    },
    capa3Gold: {
      name: 'Capa 3: Analytical & Semantic Gold',
      status: 'OPTIMAL',
      latencyP99Ms: 108,
      featureStoreStatus: 'ONLINE_ML_READY',
      dashboardsConnected: ['Power BI Executive', 'Looker Ops', 'Risk Realtime'],
      apiQueryQuotaUsedPct: 34.2
    },
    doraMetrics: {
      deploymentFrequency: '2.4 deploys / semana (Elite)',
      leadTimeForChanges: '26 horas (Elite)',
      changeFailureRate: '1.8% (Target < 5%)',
      meanTimeToRestore: '28 minutos (Target < 45 min)'
    }
  },

  squad: [
    {
      role: 'Product Owner',
      name: 'Carlos Mendoza',
      bio: 'Líder de valor de negocio y priorización estratégica en Squads ágiles.',
      chapter: 'Product Management Chapter',
      status: 'ONLINE',
      email: 'carlos.mendoza@statsfirm.co'
    },
    {
      role: 'Revisor Agile (Scrum Master)',
      name: 'Elena Vance',
      bio: 'Facilitadora de ceremonias ágiles, remoción de bloqueos y cadencia de sprints.',
      chapter: 'Agile Coaching Chapter',
      status: 'ONLINE',
      email: 'elena.vance@statsfirm.co'
    },
    {
      role: 'Jefe de Procesos (Process Lead)',
      name: 'Mateo Arismendi',
      bio: 'Arquitecto de procesos BPMN 2.0, ingeniería de requerimientos y optimización.',
      chapter: 'Business Architecture Chapter',
      status: 'ONLINE',
      email: 'mateo.arismendi@statsfirm.co'
    },
    {
      role: 'Administrador de Datos (Data Steward)',
      name: 'Julián Ríos',
      bio: 'Custodio del gobierno del dato, políticas DAMA-BOK, linaje y privacidad PII.',
      chapter: 'Data Governance Chapter',
      status: 'AWAY',
      email: 'julian.rios@statsfirm.co'
    },
    {
      role: 'Arquitecta de Datos',
      name: 'Dra. Sofía Alarcón',
      bio: 'Diseñadora de la topología Lakehouse Medallion (Bronze/Silver/Gold) y Data Mesh.',
      chapter: 'Data Engineering Chapter',
      status: 'ONLINE',
      email: 'sofia.alarcon@statsfirm.co'
    },
    {
      role: 'Arquitecto de Software',
      name: 'Daniel Ortiz',
      bio: 'Estratega de microservicios cloud-native, BFF GraphQL y contratos OpenAPI.',
      chapter: 'Software Engineering Chapter',
      status: 'ONLINE',
      email: 'daniel.ortiz@statsfirm.co'
    },
    {
      role: 'QA Engineer',
      name: 'Laura Pineda',
      bio: 'Garante de calidad, automatización de pruebas E2E y certificación Definition of Done.',
      chapter: 'Quality Assurance Chapter',
      status: 'ONLINE',
      email: 'laura.pineda@statsfirm.co'
    },
    {
      role: 'DevOps & DataOps',
      name: 'Tomás Echeverry',
      bio: 'Automatización de pipelines CI/CD, Kubernetes, SonarQube e IaC con Terraform.',
      chapter: 'DevOps & SRE Chapter',
      status: 'ONLINE',
      email: 'tomas.echeverry@statsfirm.co'
    }
  ],

  messages: [
    {
      id: 1,
      sender: 'Elena Vance (Revisor Agile)',
      role: 'Scrum Master',
      timestamp: '10:15 AM',
      text: '¡Hola Alejandro! El Sprint 04 avanza según el plan. Las pruebas de dbt en Staging alcanzaron 99.85% de aprobación. La Sprint Review está fijada para este jueves.'
    },
    {
      id: 2,
      sender: 'Mateo Arismendi (Jefe de Procesos)',
      role: 'Process Lead',
      timestamp: '11:30 AM',
      text: 'Hola equipo. Acabamos de auditar la compuerta de linaje con el Data Steward. Los contratos de datos Avro para la capa Silver ya están registrados en el Catálogo.'
    }
  ],

  vault: [
    {
      id: 'DOC-01',
      title: 'Contrato Marco de Prestación de Servicios Tecnológicos (MSA)',
      type: 'LEGAL_CONTRACT',
      hashSha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      size: '1.2 MB',
      date: '2026-09-01',
      status: 'SIGNED_VERIFIED',
      downloadUrl: '/api/vault/download/contrato'
    },
    {
      id: 'DOC-02',
      title: 'Data Processing Agreement (DPA) & Cláusulas GDPR/PII',
      type: 'COMPLIANCE',
      hashSha256: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
      size: '640 KB',
      date: '2026-09-01',
      status: 'SIGNED_VERIFIED',
      downloadUrl: '/api/vault/download/dpa'
    },
    {
      id: 'DOC-03',
      title: 'Modelo BPMN 2.0 Camunda: Organización y Procesos Canónicos',
      type: 'BPMN_ARCHITECTURE',
      hashSha256: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
      size: '60.6 KB',
      date: '2026-09-06',
      status: 'APPROVED_EXECUTABLE',
      downloadUrl: '/api/vault/download/bpmn'
    },
    {
      id: 'DOC-04',
      title: 'Especificación de Arquitectura Empresarial (TOGAF ADM & 3 Capas)',
      type: 'TECHNICAL_SPEC',
      hashSha256: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
      size: '1.0 MB',
      date: '2026-09-02',
      status: 'ACTIVE_SPEC',
      downloadUrl: '/api/vault/download/arquitectura'
    }
  ],

  pendingApprovals: [
    {
      id: 'APP-SP3-01',
      title: 'Incremento Sprint 03: Pipeline Capa 2 Silver Curated & Módulo BFF GraphQL',
      sprint: 'Sprint 03',
      deliverables: [
        '14 Tablas Delta Silver Curadas en Lakehouse',
        'Endpoints GraphQL BFF con Autenticación OIDC',
        'Suite de Tests Automatizados con Cobertura 88.4%',
        'Registro de Linaje Inmutable en Catálogo de Datos'
      ],
      dodChecklist: [
        { item: 'Cobertura de pruebas unitarias > 80% (Alcanzado: 88.4%)', passed: true },
        { item: 'SonarQube Quality Gate en estado PASSED (0 vulnerabilidades)', passed: true },
        { item: 'Linaje criptográfico registrado por Data Steward', passed: true },
        { item: 'Despliegue exitoso verificado en ambiente Staging K8s', passed: true }
      ],
      amountToInvoiceUsd: 14500,
      status: 'PENDING_CLIENT_SIGNATURE'
    }
  ],

  signedApprovalsHistory: [],

  incidents: [
    {
      id: 'INC-2026-0042',
      title: 'Saturación temporal en consumidor Kafka de Capa 1 Bronze',
      severity: 'Sev 2',
      component: 'Ingesta / Kafka / Conectores Capa 1',
      reportedAt: '2026-09-06 09:12 UTC',
      status: 'RESOLVED',
      slaResponseMet: true,
      rca: 'Pico de eventos transaccionales no planificado mitigado mediante auto-escalado horizontal (HPA) de pods en Kubernetes.',
      resolutionTimeMin: 24
    }
  ]
};

module.exports = store;
