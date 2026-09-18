const express = require('express');
const router = express.Router();
const servicesCatalog = require('../data/servicesCatalog');

// GET /api/services
router.get('/', (req, res) => {
  res.json({
    success: true,
    data: servicesCatalog
  });
});

// GET /api/services/:id
router.get('/:id', (req, res) => {
  const service = servicesCatalog.serviceLines.find(s => s.id === req.params.id);
  if (!service) {
    return res.status(404).json({ success: false, error: 'Línea de servicio no encontrada' });
  }
  res.json({ success: true, data: service });
});

module.exports = router;
