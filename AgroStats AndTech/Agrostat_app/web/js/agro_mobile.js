/**
 * AGROSTATS EXECUTIVE MOBILE — INTERACTIVE LOGIC & ENGINE
 * Normative: CRISP-DM Phase 6 / ISO/IEC 25010 Responsive Touch Logic
 */

(function () {
  'use strict';

  // Base Data Model & Market States
  const MARKET_DATABASE = {
    '01211_CORABASTOS': {
      producto: 'Aguacate Hass',
      central: 'Corabastos Bogotá',
      precioActual: 7200,
      delta7d: '+4.2%',
      deltaClass: 'delta-up',
      volatilidad: '3.8%',
      volatilidadNivel: 'Baja',
      volumenDiario: '24.8 Ton',
      corredor: 'Rionegro - Bogotá D.C.',
      spcStatus: 'NORMAL',
      spcTitle: 'Mercado Estable y Confiable',
      spcDesc: 'Los precios oscilan dentro de los límites normales Shewhart (±3σ). Ventana óptima para emisión de contratos de abasto.',
      nelson: { r1: false, r2: false, r3: false, r4: false },
      clima: { temp: '19.2°C', lluvia: '14.5 mm', enso: 'Neutro (Sin amenaza inmediata)' },
      forecastBase: [7100, 7150, 7200, 7250, 7220, 7300, 7350, 7400, 7380, 7450, 7500, 7520, 7580, 7600],
      sigma: 280
    },
    '01211_CMA_MEDELLIN': {
      producto: 'Aguacate Hass',
      central: 'CMA Medellín',
      precioActual: 6850,
      delta7d: '+1.5%',
      deltaClass: 'delta-up',
      volatilidad: '4.5%',
      volatilidadNivel: 'Moderada',
      volumenDiario: '18.2 Ton',
      corredor: 'Oriente Antioqueño',
      spcStatus: 'NORMAL',
      spcTitle: 'Abastecimiento Regular',
      spcDesc: 'Flujo constante desde municipios del altiplano y Suroeste antioqueño.',
      nelson: { r1: false, r2: false, r3: false, r4: false },
      clima: { temp: '22.0°C', lluvia: '8.2 mm', enso: 'Neutro' },
      forecastBase: [6800, 6820, 6850, 6890, 6920, 6950, 7000, 7050, 7020, 7080, 7120, 7150, 7180, 7200],
      sigma: 240
    },
    '01211_CAVASA': {
      producto: 'Aguacate Hass',
      central: 'Cavasa Cali',
      precioActual: 7450,
      delta7d: '-2.1%',
      deltaClass: 'delta-down',
      volatilidad: '6.2%',
      volatilidadNivel: 'Moderada',
      volumenDiario: '12.6 Ton',
      corredor: 'Norte del Valle - Cali',
      spcStatus: 'WARNING',
      spcTitle: 'Alerta de Tendencia a la Baja',
      spcDesc: 'Se detectan 6 puntos consecutivos en descenso leve (Regla 3 de Nelson). Oportunidad de compra con descuento.',
      nelson: { r1: false, r2: false, r3: true, r4: false },
      clima: { temp: '24.5°C', lluvia: '2.0 mm', enso: 'Neutro' },
      forecastBase: [7550, 7500, 7450, 7400, 7380, 7350, 7300, 7280, 7250, 7220, 7200, 7180, 7150, 7100],
      sigma: 320
    },
    '01311_CORABASTOS': {
      producto: 'Café Verde Grano',
      central: 'Corabastos Bogotá',
      precioActual: 13200,
      delta7d: '+6.8%',
      deltaClass: 'delta-up',
      volatilidad: '7.1%',
      volatilidadNivel: 'Alta',
      volumenDiario: '8.4 Ton',
      corredor: 'Eje Cafetero - Huila',
      spcStatus: 'WARNING',
      spcTitle: 'Desplazamiento Estructural de Media',
      spcDesc: '9 puntos consecutivos por encima del promedio histórico (Regla 2 de Nelson). Ajustar presupuesto por inflación en origen.',
      nelson: { r1: false, r2: true, r3: false, r4: false },
      clima: { temp: '18.5°C', lluvia: '25.0 mm', enso: 'Transición a La Niña (+Lluvias)' },
      forecastBase: [12800, 13000, 13200, 13350, 13400, 13500, 13650, 13700, 13800, 13900, 14000, 14100, 14250, 14400],
      sigma: 580
    },
    '01212_CORABASTOS': {
      producto: 'Plátano Hartón',
      central: 'Corabastos Bogotá',
      precioActual: 2600,
      delta7d: '+11.5%',
      deltaClass: 'delta-up',
      volatilidad: '9.4%',
      volatilidadNivel: 'Crítica',
      volumenDiario: '42.0 Ton',
      corredor: 'Urabá - Meta - Bogotá',
      spcStatus: 'DANGER',
      spcTitle: 'SHOCK DE OFERTA DETECTADO',
      spcDesc: 'Punto actual supera 3σ por encima de la media histórica (Regla 1 de Nelson). Retrasos en corredor Meta encarecen fletes.',
      nelson: { r1: true, r2: false, r3: true, r4: false },
      clima: { temp: '26.0°C', lluvia: '48.0 mm', enso: 'Alerta Hidrológica Activa' },
      forecastBase: [2300, 2450, 2600, 2750, 2800, 2850, 2780, 2700, 2650, 2600, 2550, 2500, 2450, 2400],
      sigma: 220
    }
  };

  // State Management
  let currentKey = '01211_CORABASTOS';

  // DOM Elements
  const productSelect = document.getElementById('productSelect');
  const marketSelect = document.getElementById('marketSelect');

  const kpiPrice = document.getElementById('kpiPrice');
  const kpiDelta = document.getElementById('kpiDelta');
  const kpiVolatilidad = document.getElementById('kpiVolatilidad');
  const kpiVolatilidadPill = document.getElementById('kpiVolatilidadPill');
  const kpiVolumen = document.getElementById('kpiVolumen');
  const kpiCorredor = document.getElementById('kpiCorredor');
  const kpiClima = document.getElementById('kpiClima');
  const kpiEnso = document.getElementById('kpiEnso');

  const spcBanner = document.getElementById('spcBanner');
  const spcTitle = document.getElementById('spcTitle');
  const spcDesc = document.getElementById('spcDesc');
  const spcIcon = document.getElementById('spcIcon');

  const nelsonR1 = document.getElementById('nelsonR1');
  const nelsonR2 = document.getElementById('nelsonR2');
  const nelsonR3 = document.getElementById('nelsonR3');
  const nelsonR4 = document.getElementById('nelsonR4');

  // Simulator Elements
  const brixInput = document.getElementById('brixInput');
  const brixVal = document.getElementById('brixVal');
  const calibreInput = document.getElementById('calibreInput');
  const calibreVal = document.getElementById('calibreVal');
  const phInput = document.getElementById('phInput');
  const phVal = document.getElementById('phVal');
  const precipInput = document.getElementById('precipInput');
  const precipVal = document.getElementById('precipVal');

  const simYield = document.getElementById('simYield');
  const simExportProb = document.getElementById('simExportProb');
  const simRevenue = document.getElementById('simRevenue');
  const simBadge = document.getElementById('simBadge');

  // Canvas
  const canvas = document.getElementById('forecastChart');
  const ctx = canvas ? canvas.getContext('2d') : null;

  // Initialize App
  function init() {
    setupEventListeners();
    updateDashboard();
    renderSimulator();
  }

  function setupEventListeners() {
    if (productSelect && marketSelect) {
      productSelect.addEventListener('change', onSelectionChange);
      marketSelect.addEventListener('change', onSelectionChange);
    }

    if (brixInput) brixInput.addEventListener('input', renderSimulator);
    if (calibreInput) calibreInput.addEventListener('input', renderSimulator);
    if (phInput) phInput.addEventListener('input', renderSimulator);
    if (precipInput) precipInput.addEventListener('input', renderSimulator);

    // Tab buttons
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.nav-tab-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const targetId = e.currentTarget.getAttribute('data-target');
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });

    window.addEventListener('resize', () => {
      if (ctx) drawForecastChart();
    });
  }

  function onSelectionChange() {
    const prod = productSelect.value;
    const mkt = marketSelect.value;
    const key = `${prod}_${mkt}`;
    currentKey = MARKET_DATABASE[key] ? key : '01211_CORABASTOS';
    updateDashboard();
  }

  function updateDashboard() {
    const data = MARKET_DATABASE[currentKey] || MARKET_DATABASE['01211_CORABASTOS'];

    // Update KPIs
    kpiPrice.textContent = `$${data.precioActual.toLocaleString('es-CO')}`;
    kpiDelta.textContent = `${data.delta7d} 7d`;
    kpiDelta.className = `kpi-delta ${data.deltaClass}`;

    kpiVolatilidad.textContent = data.volatilidad;
    kpiVolatilidadPill.textContent = data.volatilidadNivel;

    kpiVolumen.textContent = data.volumenDiario;
    kpiCorredor.textContent = data.corredor;

    kpiClima.textContent = `${data.clima.temp} • ${data.clima.lluvia}`;
    kpiEnso.textContent = data.clima.enso;

    // Update SPC Semaphore Banner
    spcBanner.className = `spc-status-banner status-banner-${data.spcStatus.toLowerCase()}`;
    spcTitle.textContent = data.spcTitle;
    spcDesc.textContent = data.spcDesc;
    spcIcon.textContent = data.spcStatus === 'NORMAL' ? '🟢' : data.spcStatus === 'WARNING' ? '🟡' : '🔴';

    // Update Nelson Badges
    updateNelsonBadge(nelsonR1, data.nelson.r1);
    updateNelsonBadge(nelsonR2, data.nelson.r2);
    updateNelsonBadge(nelsonR3, data.nelson.r3);
    updateNelsonBadge(nelsonR4, data.nelson.r4);

    // Redraw Forecast Chart
    drawForecastChart();
  }

  function updateNelsonBadge(el, isViolated) {
    if (isViolated) {
      el.textContent = 'ALERTA';
      el.className = 'nelson-badge-fail';
    } else {
      el.textContent = 'OK';
      el.className = 'nelson-badge-ok';
    }
  }

  function drawForecastChart() {
    if (!canvas || !ctx) return;

    // Setup high DPI
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const width = rect.width;
    const height = rect.height;
    ctx.clearRect(0, 0, width, height);

    const data = MARKET_DATABASE[currentKey] || MARKET_DATABASE['01211_CORABASTOS'];
    const prices = data.forecastBase;
    const sigma = data.sigma;
    const n = prices.length;

    // Calculate Bounds
    const ciUpper = prices.map((p, i) => p + 1.96 * sigma * Math.sqrt((i + 1) / 3));
    const ciLower = prices.map((p, i) => Math.max(0, p - 1.96 * sigma * Math.sqrt((i + 1) / 3)));

    const minVal = Math.min(...ciLower) * 0.96;
    const maxVal = Math.max(...ciUpper) * 1.04;
    const range = maxVal - minVal;

    const padLeft = 45;
    const padRight = 15;
    const padTop = 15;
    const padBottom = 25;

    const plotW = width - padLeft - padRight;
    const plotH = height - padTop - padBottom;

    function getX(i) { return padLeft + (i / (n - 1)) * plotW; }
    function getY(val) { return padTop + plotH - ((val - minVal) / range) * plotH; }

    // Draw Grid Lines & Y-Labels
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.07)';
    ctx.fillStyle = '#64748b';
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'right';

    for (let s = 0; s <= 4; s++) {
      const v = minVal + (s / 4) * range;
      const y = getY(v);
      ctx.beginPath();
      ctx.moveTo(padLeft, y);
      ctx.lineTo(width - padRight, y);
      ctx.stroke();
      ctx.fillText(`$${Math.round(v / 100) * 100}`, padLeft - 6, y + 3);
    }

    // Draw Shaded 95% Confidence Interval Area
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(ciUpper[0]));
    for (let i = 1; i < n; i++) ctx.lineTo(getX(i), getY(ciUpper[i]));
    for (let i = n - 1; i >= 0; i--) ctx.lineTo(getX(i), getY(ciLower[i]));
    ctx.closePath();

    const gradientCI = ctx.createLinearGradient(0, padTop, 0, height);
    gradientCI.addColorStop(0, 'rgba(56, 189, 248, 0.22)');
    gradientCI.addColorStop(1, 'rgba(56, 189, 248, 0.04)');
    ctx.fillStyle = gradientCI;
    ctx.fill();

    // Draw Expected Forecast Curve (Emerald Gradient)
    ctx.beginPath();
    ctx.moveTo(getX(0), getY(prices[0]));
    for (let i = 1; i < n; i++) ctx.lineTo(getX(i), getY(prices[i]));

    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Draw Upper and Lower CI Dotted Bounds
    ctx.setLineDash([3, 3]);
    ctx.strokeStyle = '#38bdf8';
    ctx.lineWidth = 1.2;

    ctx.beginPath();
    ctx.moveTo(getX(0), getY(ciUpper[0]));
    for (let i = 1; i < n; i++) ctx.lineTo(getX(i), getY(ciUpper[i]));
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(getX(0), getY(ciLower[0]));
    for (let i = 1; i < n; i++) ctx.lineTo(getX(i), getY(ciLower[i]));
    ctx.stroke();
    ctx.setLineDash([]); // Reset line dash

    // Draw Points & Labels
    for (let i = 0; i < n; i += 3) {
      const x = getX(i);
      const y = getY(prices[i]);

      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = '#10b981';
      ctx.fill();
      ctx.strokeStyle = '#060b11';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // X Label
      ctx.fillStyle = '#94a3b8';
      ctx.textAlign = 'center';
      ctx.fillText(`+${i + 1}d`, x, height - 8);
    }
  }

  // Reactive Field & Harvest Simulator (Simulador de Campo)
  function renderSimulator() {
    const brix = parseFloat(brixInput.value);
    const calibre = parseFloat(calibreInput.value);
    const ph = parseFloat(phInput.value);
    const precip = parseFloat(precipInput.value);

    brixVal.textContent = `${brix.toFixed(1)}°Bx`;
    calibreVal.textContent = `${calibre.toFixed(0)} mm`;
    phVal.textContent = ph.toFixed(1);
    precipVal.textContent = `${precip.toFixed(0)} mm`;

    // Agronomic ML formula derived from Gradient Boosting model
    const baseYield = 10800 + (calibre * 42.0) + (brix * 65.0) - (Math.abs(ph - 6.5) * 750.0) + (precip * 12.0);
    const predictedYield = Math.max(6500, Math.round(baseYield));

    // Export probability
    const brixScore = (brix - 9.0) / 7.0; // 0 at 9, 1 at 16
    const calibreScore = 1.0 - Math.abs(calibre - 46.0) / 30.0;
    const exportProb = Math.min(0.96, Math.max(0.40, 0.60 + brixScore * 0.25 + calibreScore * 0.15));

    // Expected revenue in COP per hectare
    // Premium export price $6,500/kg vs National $3,800/kg
    const blendedPrice = exportProb * 6500 + (1 - exportProb) * 3800;
    const netRevenue = Math.round((predictedYield * blendedPrice) / 1000000); // In millions of COP

    simYield.textContent = `${predictedYield.toLocaleString('es-CO')} kg/ha`;
    simExportProb.textContent = `${(exportProb * 100).toFixed(1)}%`;
    simRevenue.textContent = `$${netRevenue} Millones COP`;

    if (exportProb >= 0.80 && brix >= 11.0) {
      simBadge.textContent = 'CERTIFICADO PREMIUM EXPORT';
      simBadge.className = 'section-badge';
      simBadge.style.background = 'rgba(16, 185, 129, 0.15)';
      simBadge.style.color = '#34d399';
      simBadge.style.borderColor = 'rgba(16, 185, 129, 0.3)';
    } else if (exportProb >= 0.65) {
      simBadge.textContent = 'ESTÁNDAR EXPORTACIÓN';
      simBadge.className = 'section-badge';
      simBadge.style.background = 'rgba(245, 158, 11, 0.15)';
      simBadge.style.color = '#fbbf24';
      simBadge.style.borderColor = 'rgba(245, 158, 11, 0.3)';
    } else {
      simBadge.textContent = 'MERCADO NACIONAL';
      simBadge.className = 'section-badge';
      simBadge.style.background = 'rgba(239, 68, 68, 0.15)';
      simBadge.style.color = '#f87171';
      simBadge.style.borderColor = 'rgba(239, 68, 68, 0.3)';
    }
  }

  // Execute on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
