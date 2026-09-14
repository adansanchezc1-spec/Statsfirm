/**
 * STATSFIRM CO. — OFFICIAL COMMERCIAL & CORPORATE WEB PLATFORM
 * Node.js Express Backend & BFF Architecture
 * 
 * Normativa:
 * - Documento 05: Catálogo de Servicios y Portafolio Tecnológico
 * - Documento 08: BPMN-01 Proceso de Captación y Calificación de Leads
 * - Documento 02: Manual de Marca y Sistema de Diseño
 * - ISO/IEC 25010 Calidad del Software & Principios Clean Code / SOLID
 */

const express = require('express');
const cors = require('cors');
const path = require('path');

const servicesRouter = require('./routes/services');
const contactRouter = require('./routes/contact');
const bpmnRouter = require('./routes/bpmn');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request Telemetry Logger
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    if (req.originalUrl.startsWith('/api')) {
      console.log(`[HTTP] ${req.method} ${req.originalUrl} -> ${res.statusCode} (${duration}ms)`);
    }
  });
  next();
});

// Static Assets
app.use(express.static(path.join(__dirname, 'public')));

// Corporate & Commercial REST API Routes
app.use('/api/services', servicesRouter);
app.use('/api', contactRouter);
app.use('/api/bpmn', bpmnRouter);

// Fallback for Single Page Commercial Application
app.get('*', (req, res) => {
  if (!req.originalUrl.startsWith('/api')) {
    res.sendFile(path.join(__dirname, 'public/index.html'));
  } else {
    res.status(404).json({ success: false, error: 'Endpoint API comercial no encontrado' });
  }
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('[SERVER ERROR]', err);
  res.status(500).json({
    success: false,
    error: 'Error interno en la plataforma comercial de Statsfirm Co.',
    details: err.message
  });
});

// Start Server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log('================================================================');
    console.log(`  STATSFIRM CO. — SITIO WEB COMERCIAL & CORPORATIVO              `);
    console.log(`  Servidor activo en: http://localhost:${PORT}                  `);
    console.log(`  Fase PDCO: DEVELOPMENT / OPERATIONS                          `);
    console.log(`  Catálogo de Servicios, Cotizador y Protocolo BPMN-01 Listos  `);
    console.log('================================================================');
  });
}

module.exports = app;
