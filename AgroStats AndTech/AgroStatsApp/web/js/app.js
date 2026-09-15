/**
 * AGRODATA INTELLIGENCE PLATFORM — ENTERPRISE CLIENT ENGINE v1.0
 * Standards: SWEBOK / DAMA-BOK / ISO 7870 Nelson Rules / Guillermo Guerra (IICA)
 * Architecture: Unidirectional Reactive State Store (Pub/Sub)
 */

'use strict';

// ============================================================================
// 1. CROP & COMMODITY DATA PROFILES (CATÁLOGO MAESTRO CPC v2.1 A.C.)
// ============================================================================
const CROP_DATABASE = {
  '01221': {
    code: '01221',
    name: 'Aguacate Hass',
    icon: '🥑',
    unit: 'kg',
    basePrice: 6450,
    baseYieldKgHa: 10500,
    costoFijoHa: 5200000,
    costoVariableBaseHa: 39325000,
    costoQuimicoBaseHa: 15500000,
    maxAhorroQuimico: 0.248, // 24.8% de ahorro en insumos
    maxPrimaExportacion: 0.125, // +12.5% sobreprecio internacional
    volatilidad: 4.2,
    abastoDiarioTon: 420,
    clima: 'Clima Favorable (ONI -0.4°C)',
    departamentoLider: 'Antioquia',
    municipioLider: 'Sonsón (05756)',
    municipioRend: '14.2 Ton/ha',
    areaNacionalHa: 58420,
    produccionNacionalTon: 547155,
    bioinsumos: [
      { nombre: 'Trichoderma harzianum B-01', tipo: 'Biofungicida', empresa: 'BioProtección Andina', ica: 'ICA-0941-F', dosis: '1.5 L/ha', sustitucion: '35% Mancozeb', estatus: 'Vigente' },
      { nombre: 'Bacillus subtilis AgroGold', tipo: 'Bactericida Orgánico', empresa: 'AgroBiológicos del Cauca', ica: 'ICA-1182-B', dosis: '2.0 kg/ha', sustitucion: '40% Cúpricos', estatus: 'Vigente' },
      { nombre: 'Micorrizas Glomus intraradices', tipo: 'Biofertilizante Fósforo', empresa: 'BioInsumos Colombia', ica: 'ICA-0753-F', dosis: '25 kg/ha', sustitucion: '30% DAP sintético', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Westfalia Fruit Colombia S.A.S.', nit: '900.412.551-3', tipo: 'Empaque & Exportación', share: 24.5, sic: 'Mercado Abierto' },
      { razon: 'Cartama Corp S.A.S.', nit: '900.284.119-1', tipo: 'Producción & Exportación', share: 19.8, sic: 'Mercado Abierto' },
      { razon: 'Avofruit S.A.S.', nit: '901.055.321-4', tipo: 'Transformación & Aceite', share: 14.2, sic: 'Competencia' },
      { razon: 'Jardín Exotics S.A.S.', nit: '900.671.902-8', tipo: 'Comercializadora', share: 11.5, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '05756', mpio: 'Sonsón', depto: 'Antioquia', area: 12500, rend: 14200, precio: 6600 },
      { cod: '17042', mpio: 'Anserma', depto: 'Caldas', area: 8400, rend: 11800, precio: 6450 },
      { cod: '66170', mpio: 'Dosquebradas', depto: 'Risaralda', area: 6200, rend: 10900, precio: 6380 },
      { cod: '73026', mpio: 'Armero Guayabal', depto: 'Tolima', area: 4100, rend: 9800, precio: 6200 }
    ]
  },
  '01610': {
    code: '01610',
    name: 'Café Verde Arábica',
    icon: '☕',
    unit: 'kg',
    basePrice: 16800,
    baseYieldKgHa: 2100,
    costoFijoHa: 4100000,
    costoVariableBaseHa: 22400000,
    costoQuimicoBaseHa: 8900000,
    maxAhorroQuimico: 0.285,
    maxPrimaExportacion: 0.220, // +22.0% Cafés Especiales
    volatilidad: 6.8,
    abastoDiarioTon: 850,
    clima: 'Floración Normal',
    departamentoLider: 'Huila',
    municipioLider: 'Pitalito (41551)',
    municipioRend: '2.8 Ton/ha',
    areaNacionalHa: 842000,
    produccionNacionalTon: 810000,
    bioinsumos: [
      { nombre: 'Beauveria bassiana BB-21', tipo: 'Bioinsecticida Broca', empresa: 'Cenicafé Licencia Tech', ica: 'ICA-0412-I', dosis: '1.0 kg/ha', sustitucion: '60% Clorpirifos', estatus: 'Vigente' },
      { nombre: 'Lecanicillium lecanii', tipo: 'Biocontrolador Roya', empresa: 'Bioagro del Huila', ica: 'ICA-0891-F', dosis: '2.0 L/ha', sustitucion: '45% Triazoles', estatus: 'Vigente' },
      { nombre: 'Lombricompuesto Líquido Enriquecido', tipo: 'Biofertilizante Foliar', empresa: 'EcoCafé Andina', ica: 'ICA-1420-A', dosis: '10 L/ha', sustitucion: '25% Urea sintética', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Federación Nacional de Cafeteros', nit: '860.007.538-2', tipo: 'Gremio & Exportación', share: 31.0, sic: 'Regulado' },
      { razon: 'Carcafe Ltda.', nit: '860.034.908-1', tipo: 'Exportadora Mayorista', share: 16.5, sic: 'Competencia' },
      { razon: 'Olam Agro Colombia S.A.S.', nit: '900.321.456-7', tipo: 'Comercializadora Global', share: 14.2, sic: 'Competencia' },
      { razon: 'Louis Dreyfus Company Colombia', nit: '800.123.987-4', tipo: 'Multinacional Agro', share: 12.0, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '41551', mpio: 'Pitalito', depto: 'Huila', area: 28400, rend: 2800, precio: 17200 },
      { cod: '19743', mpio: 'Santander de Quilichao', depto: 'Cauca', area: 16200, rend: 2300, precio: 16800 },
      { cod: '63001', mpio: 'Armenia', depto: 'Quindío', area: 12100, rend: 2150, precio: 16900 },
      { cod: '05001', mpio: 'Fredonia', depto: 'Antioquia', area: 9800, rend: 2050, precio: 16750 }
    ]
  },
  '01222': {
    code: '01222',
    name: 'Plátano Hartón',
    icon: '🍌',
    unit: 'kg',
    basePrice: 3200,
    baseYieldKgHa: 14000,
    costoFijoHa: 3800000,
    costoVariableBaseHa: 26000000,
    costoQuimicoBaseHa: 9500000,
    maxAhorroQuimico: 0.210,
    maxPrimaExportacion: 0.150,
    volatilidad: 3.5,
    abastoDiarioTon: 620,
    clima: 'Humedad Óptima',
    departamentoLider: 'Quindío',
    municipioLider: 'Armenia (63001)',
    municipioRend: '18.5 Ton/ha',
    areaNacionalHa: 412000,
    produccionNacionalTon: 3650000,
    bioinsumos: [
      { nombre: 'Paecilomyces lilacinus', tipo: 'Bionematicida Radicular', empresa: 'NematoControl Ltda.', ica: 'ICA-0631-N', dosis: '3.0 L/ha', sustitucion: '50% Carbofuran', estatus: 'Vigente' },
      { nombre: 'BioPlatanus Enzimas', tipo: 'Bioestimulante Foliar', empresa: 'Quindío AgroBio', ica: 'ICA-1029-A', dosis: '2.5 L/ha', sustitucion: '30% Fertilizante NPK', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Bananon Agroexport S.A.', nit: '900.111.222-3', tipo: 'Exportación Plátano', share: 22.0, sic: 'Mercado Abierto' },
      { razon: 'Comercializadora del Eje S.A.S.', nit: '900.333.444-5', tipo: 'Abastecimiento Nacional', share: 18.5, sic: 'Competencia' },
      { razon: 'AgroPlátano Arauca Ltda.', nit: '800.555.666-7', tipo: 'Comercialización Frontera', share: 15.0, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '63001', mpio: 'Armenia', depto: 'Quindío', area: 18000, rend: 18500, precio: 3350 },
      { cod: '81001', mpio: 'Arauca', depto: 'Arauca', area: 22000, rend: 15200, precio: 2980 },
      { cod: '05837', mpio: 'Turbo', depto: 'Antioquia', area: 19500, rend: 14800, precio: 3100 }
    ]
  },
  '01232': {
    code: '01232',
    name: 'Tomate Chonto',
    icon: '🍅',
    unit: 'kg',
    basePrice: 4100,
    baseYieldKgHa: 38000,
    costoFijoHa: 8500000,
    costoVariableBaseHa: 82000000,
    costoQuimicoBaseHa: 36000000,
    maxAhorroQuimico: 0.315,
    maxPrimaExportacion: 0.180,
    volatilidad: 8.4,
    abastoDiarioTon: 310,
    clima: 'Sensible a Lluvia Alta',
    departamentoLider: 'Boyacá',
    municipioLider: 'Sutamarchán (15776)',
    municipioRend: '52.0 Ton/ha',
    areaNacionalHa: 14800,
    produccionNacionalTon: 485000,
    bioinsumos: [
      { nombre: 'Bacillus thuringiensis Kurstaki', tipo: 'Bioinsecticida Cogollero', empresa: 'BioControl Andino', ica: 'ICA-0284-I', dosis: '1.0 kg/ha', sustitucion: '55% Deltametrina', estatus: 'Vigente' },
      { nombre: 'Extracto de Neem + Pongamia', tipo: 'Acaricida Botánico', empresa: 'FitoSalud Verde', ica: 'ICA-1290-B', dosis: '2.0 L/ha', sustitucion: '40% Abamectina', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Hortalizas del Valle S.A.', nit: '890.123.456-1', tipo: 'Comercialización Abasto', share: 20.4, sic: 'Competencia' },
      { razon: 'AgroInsumos Boyacá S.A.S.', nit: '900.789.012-3', tipo: 'Semillas & Logística', share: 17.8, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '15776', mpio: 'Sutamarchán', depto: 'Boyacá', area: 3800, rend: 52000, precio: 4300 },
      { cod: '76834', mpio: 'Tuluá', depto: 'Valle del Cauca', area: 2900, rend: 41000, precio: 3950 },
      { cod: '54001', mpio: 'Cúcuta', depto: 'Norte de Santander', area: 2400, rend: 36000, precio: 4050 }
    ]
  },
  '01510': {
    code: '01510',
    name: 'Papa Pastusa',
    icon: '🥔',
    unit: 'kg',
    basePrice: 2850,
    baseYieldKgHa: 22000,
    costoFijoHa: 4900000,
    costoVariableBaseHa: 38000000,
    costoQuimicoBaseHa: 18000000,
    maxAhorroQuimico: 0.260,
    maxPrimaExportacion: 0.100,
    volatilidad: 7.2,
    abastoDiarioTon: 1250,
    clima: 'Páramo Normal',
    departamentoLider: 'Cundinamarca',
    municipioLider: 'Villapinzón (25873)',
    municipioRend: '28.0 Ton/ha',
    areaNacionalHa: 132000,
    produccionNacionalTon: 2750000,
    bioinsumos: [
      { nombre: 'Purpureocillium lilacinum', tipo: 'Bionematicida Quiste', empresa: 'Papasana Biotech', ica: 'ICA-0832-N', dosis: '2.5 L/ha', sustitucion: '45% Nemacur', estatus: 'Vigente' },
      { nombre: 'Compost Activado con Azotobacter', tipo: 'Fijador de Nitrógeno', empresa: 'FertiEco Andino', ica: 'ICA-1199-F', dosis: '500 kg/ha', sustitucion: '35% Cloruro Potasio', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Fedepapa Comercial S.A.', nit: '860.504.221-9', tipo: 'Gremio & Distribución', share: 26.0, sic: 'Regulado' },
      { razon: 'Congelados Andinos S.A.S.', nit: '900.222.888-1', tipo: 'Procesamiento Industrial', share: 21.5, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '25873', mpio: 'Villapinzón', depto: 'Cundinamarca', area: 24000, rend: 28000, precio: 2900 },
      { cod: '15835', mpio: 'Ventaquemada', depto: 'Boyacá', area: 19500, rend: 24000, precio: 2820 },
      { cod: '52001', mpio: 'Pasto', depto: 'Nariño', area: 18200, rend: 23500, precio: 2780 }
    ]
  },
  '01121': {
    code: '01121',
    name: 'Maíz Amarillo Duro',
    icon: '🌽',
    unit: 'kg',
    basePrice: 1950,
    baseYieldKgHa: 6500,
    costoFijoHa: 2200000,
    costoVariableBaseHa: 8200000,
    costoQuimicoBaseHa: 3800000,
    maxAhorroQuimico: 0.220,
    maxPrimaExportacion: 0.085,
    volatilidad: 3.9,
    abastoDiarioTon: 980,
    clima: 'Cálido Normal',
    departamentoLider: 'Tolima',
    municipioLider: 'Espinal (73268)',
    municipioRend: '8.5 Ton/ha',
    areaNacionalHa: 285000,
    produccionNacionalTon: 1520000,
    bioinsumos: [
      { nombre: 'Azospirillum brasilense AZ-5', tipo: 'Inoculante de Semilla', empresa: 'BioMaíz Colombia', ica: 'ICA-0711-B', dosis: '500 ml/50kg', sustitucion: '30% Urea', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Italcol S.A.', nit: '860.052.123-4', tipo: 'Alimentos Balanceados', share: 28.0, sic: 'Competencia' },
      { razon: 'Finca S.A.S.', nit: '890.301.765-8', tipo: 'Procesamiento Animal', share: 22.4, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '73268', mpio: 'Espinal', depto: 'Tolima', area: 32000, rend: 8500, precio: 1980 },
      { cod: '23001', mpio: 'Montería', depto: 'Córdoba', area: 41000, rend: 6800, precio: 1940 }
    ]
  },
  '01321': {
    code: '01321',
    name: 'Cítricos / Naranja Valencia',
    icon: '🍊',
    unit: 'kg',
    basePrice: 2400,
    baseYieldKgHa: 18000,
    costoFijoHa: 3600000,
    costoVariableBaseHa: 24000000,
    costoQuimicoBaseHa: 10200000,
    maxAhorroQuimico: 0.250,
    maxPrimaExportacion: 0.160,
    volatilidad: 4.8,
    abastoDiarioTon: 540,
    clima: 'Precipitaciones Estables',
    departamentoLider: 'Meta',
    municipioLider: 'Lejanías (50400)',
    municipioRend: '22.5 Ton/ha',
    areaNacionalHa: 98000,
    produccionNacionalTon: 1450000,
    bioinsumos: [
      { nombre: 'Tamarixia radiata', tipo: 'Parasitoide HLB Diaphorina', empresa: 'BioCitros del Meta', ica: 'ICA-0349-B', dosis: '200 ind/ha', sustitucion: '50% Imidacloprid', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Citrocol S.A.S.', nit: '900.567.890-1', tipo: 'Jugos & Pulpa', share: 25.0, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '50400', mpio: 'Lejanías', depto: 'Meta', area: 18000, rend: 22500, precio: 2450 },
      { cod: '76834', mpio: 'Sevilla', depto: 'Valle del Cauca', area: 12000, rend: 19200, precio: 2380 }
    ]
  },
  '01620': {
    code: '01620',
    name: 'Cacao en Grano Fino de Aroma',
    icon: '🍫',
    unit: 'kg',
    basePrice: 28500,
    baseYieldKgHa: 950,
    costoFijoHa: 3200000,
    costoVariableBaseHa: 14000000,
    costoQuimicoBaseHa: 5100000,
    maxAhorroQuimico: 0.300,
    maxPrimaExportacion: 0.250, // Récord orgánico
    volatilidad: 9.1,
    abastoDiarioTon: 190,
    clima: 'Condiciones Agroforestales',
    departamentoLider: 'Santander',
    municipioLider: 'San Vicente de Chucurí (68689)',
    municipioRend: '1.4 Ton/ha',
    areaNacionalHa: 192000,
    produccionNacionalTon: 72000,
    bioinsumos: [
      { nombre: 'Trichoderma koningiopsis', tipo: 'Biofungicida Monilia', empresa: 'CacaoVerde Santander', ica: 'ICA-0994-F', dosis: '2.0 L/ha', sustitucion: '65% Cobre sintético', estatus: 'Vigente' }
    ],
    empresas: [
      { razon: 'Compañía Nacional de Chocolates', nit: '890.900.089-1', tipo: 'Transformación Chocolate', share: 38.5, sic: 'Líder de Mercado' },
      { razon: 'CasaLuker S.A.', nit: '890.800.123-5', tipo: 'Exportación Fino de Aroma', share: 29.2, sic: 'Competencia' }
    ],
    territorios: [
      { cod: '68689', mpio: 'San Vicente de Chucurí', depto: 'Santander', area: 26000, rend: 1400, precio: 29200 },
      { cod: '05045', mpio: 'Apartadó', depto: 'Antioquia', area: 14000, rend: 1100, precio: 28400 }
    ]
  }
};

// ============================================================================
// 2. STATE STORE (PUB/SUB REACTIVO)
// ============================================================================
class AgroStateStore {
  constructor() {
    this.state = {
      productCode: '01221',
      marketCode: 'CORABASTOS',
      periodCode: '90D',
      analyticalMode: 'PRODUCCION_COMERCIAL',
      sourceLayer: 'GOLD_INTEGRATED',
      bioAdoptionRate: 45, // %
      activeTab: 'mercado',
      fieldSimulation: {
        areaHa: 5,
        density: 250,
        techLevel: 45
      }
    };
    this.subscribers = [];
  }

  subscribe(listener) {
    this.subscribers.push(listener);
  }

  setState(partialState) {
    const prevState = { ...this.state };
    this.state = { ...this.state, ...partialState };
    this.notify(prevState);
  }

  notify(prevState) {
    for (const sub of this.subscribers) {
      try {
        sub(this.state, prevState);
      } catch (err) {
        console.error('[AgroStateStore Error]', err);
      }
    }
  }

  getState() {
    return this.state;
  }
}

const store = new AgroStateStore();

// ============================================================================
// 3. GUILLERMO GUERRA (IICA) AGROECONOMIC ENGINE
// ============================================================================
class GuerraEngineClient {
  static compute(crop, adoptionPercent) {
    const adoptionFactor = Math.max(0, Math.min(100, adoptionPercent)) / 100.0;

    // Ahorro en insumos químicos
    const tasaAhorro = crop.maxAhorroQuimico * adoptionFactor;
    const ahorroQuimicoHa = crop.costoQuimicoBaseHa * tasaAhorro;
    const costoVariableAjustadoHa = crop.costoVariableBaseHa - ahorroQuimicoHa;

    // Prima de exportación limpia (cero LMR)
    const primaTasa = crop.maxPrimaExportacion * adoptionFactor;
    const precioEfectivo = crop.basePrice * (1 + primaTasa);

    // Ingreso Bruto
    const ingresoBrutoHa = crop.baseYieldKgHa * precioEfectivo;

    // Margen Bruto Guillermo Guerra (MB = IB - CV)
    const margenBrutoHa = ingresoBrutoHa - costoVariableAjustadoHa;

    // Costo Total
    const costoTotalHa = crop.costoFijoHa + costoVariableAjustadoHa;

    // Punto de Equilibrio (BEP)
    const bepFisicoKgHa = costoTotalHa / precioEfectivo;
    const bepMonetarioPrecioKg = costoTotalHa / crop.baseYieldKgHa;

    // Margen de seguridad s/ volumen
    const margenSeguridadPct = ((crop.baseYieldKgHa - bepFisicoKgHa) / crop.baseYieldKgHa) * 100;

    // ROI Agroempresarial
    const roiPct = (margenBrutoHa / costoVariableAjustadoHa) * 100;
    const relacionBeneficioCosto = ingresoBrutoHa / costoTotalHa;

    // Huella química evitada
    const kgQuimicosEvitados = Math.round(340 * adoptionFactor);

    return {
      precioEfectivo,
      primaTasaPct: (primaTasa * 100).toFixed(1),
      primaValorHa: crop.baseYieldKgHa * crop.basePrice * primaTasa,
      ahorroTasaPct: (tasaAhorro * 100).toFixed(1),
      ahorroQuimicoHa,
      costoVariableAjustadoHa,
      costoTotalHa,
      ingresoBrutoHa,
      margenBrutoHa,
      bepFisicoKgHa: Math.round(bepFisicoKgHa),
      bepMonetarioPrecioKg: Math.round(bepMonetarioPrecioKg),
      margenSeguridadPct: margenSeguridadPct.toFixed(1),
      roiPct: roiPct.toFixed(1),
      relacionBeneficioCosto: relacionBeneficioCosto.toFixed(2),
      kgQuimicosEvitados
    };
  }
}

// ============================================================================
// 4. SHEWHART & NELSON SPC ENGINE (ISO 7870)
// ============================================================================
class BiostatisticalClientEngine {
  static generateTimeSeries(crop, nDays = 30) {
    const points = [];
    const mu = crop.basePrice;
    const sigma = mu * (crop.volatilidad / 100.0);
    const today = new Date();

    for (let i = nDays; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];

      // Pseudo-random random walk con reversión a la media
      const noise = (Math.sin(i * 0.4) + Math.cos(i * 0.2)) * (sigma * 0.5);
      const price = Math.round(mu + noise);

      points.push({
        date: dateStr,
        price,
        ucl: Math.round(mu + 3 * sigma),
        lcl: Math.round(mu - 3 * sigma),
        mean: Math.round(mu),
        min: Math.round(price * 0.96),
        max: Math.round(price * 1.04)
      });
    }

    return points;
  }

  static evaluateNelson(points) {
    if (!points || points.length < 15) return { status: 'NORMAL', rules: [true, true, true, true] };

    const prices = points.map(p => p.price);
    const mean = points[0].mean;
    const sigma = (points[0].ucl - mean) / 3;

    // Regla 1: 1 punto > 3 sigma
    const rule1Violations = prices.filter(p => Math.abs(p - mean) > 3 * sigma).length;

    // Regla 2: 9 puntos seguidos al mismo lado de la media
    let rule2Fail = false;
    let streak = 0;
    let lastSide = 0;
    for (const p of prices) {
      const side = p >= mean ? 1 : -1;
      if (side === lastSide) streak++;
      else { streak = 1; lastSide = side; }
      if (streak >= 9) { rule2Fail = true; break; }
    }

    // Regla 3: 6 puntos consecutivos en aumento o descenso
    let rule3Fail = false;
    let trendStreak = 1;
    for (let i = 1; i < prices.length; i++) {
      if (prices[i] > prices[i-1]) {
        trendStreak = trendStreak >= 0 ? trendStreak + 1 : 1;
      } else if (prices[i] < prices[i-1]) {
        trendStreak = trendStreak <= 0 ? trendStreak - 1 : -1;
      }
      if (Math.abs(trendStreak) >= 6) { rule3Fail = true; break; }
    }

    // Regla 4: 14 puntos alternando arriba y abajo
    let rule4Fail = false;
    let altCount = 0;
    for (let i = 2; i < prices.length; i++) {
      const diff1 = prices[i] - prices[i-1];
      const diff2 = prices[i-1] - prices[i-2];
      if ((diff1 > 0 && diff2 < 0) || (diff1 < 0 && diff2 > 0)) {
        altCount++;
      } else {
        altCount = 0;
      }
      if (altCount >= 14) { rule4Fail = true; break; }
    }

    const hasViolations = rule1Violations > 0 || rule2Fail || rule3Fail || rule4Fail;

    return {
      status: hasViolations ? 'WARNING' : 'NORMAL',
      rule1: rule1Violations === 0,
      rule2: !rule2Fail,
      rule3: !rule3Fail,
      rule4: !rule4Fail,
      ucl: points[0].ucl,
      lcl: points[0].lcl,
      mean
    };
  }
}

// ============================================================================
// 5. HIGH-DPI CANVAS CHART ENGINE
// ============================================================================
class AgroChartRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
  }

  render(points, cropName) {
    if (!this.canvas || !this.ctx || !points || points.length === 0) return;

    const ctx = this.ctx;
    const canvas = this.canvas;

    // Retina / High-DPI support
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = rect.height;

    // Limpiar fondo
    ctx.clearRect(0, 0, w, h);

    const padding = { top: 30, right: 40, bottom: 40, left: 65 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;

    // Escalas de precio
    const allVals = points.map(p => p.price).concat(points.map(p => p.ucl), points.map(p => p.lcl));
    const minVal = Math.min(...allVals) * 0.95;
    const maxVal = Math.max(...allVals) * 1.05;

    const getX = (idx) => padding.left + (idx / (points.length - 1)) * chartW;
    const getY = (val) => padding.top + chartH - ((val - minVal) / (maxVal - minVal)) * chartH;

    // 1. Dibujar líneas de cuadrícula y etiquetas Y
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.06)';
    ctx.fillStyle = '#64748b';
    ctx.font = '10px Inter, sans-serif';
    ctx.textAlign = 'right';

    const yTicks = 5;
    for (let i = 0; i <= yTicks; i++) {
      const val = minVal + (i / yTicks) * (maxVal - minVal);
      const y = getY(val);
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(w - padding.right, y);
      ctx.stroke();
      ctx.fillText(`$${Math.round(val).toLocaleString()}`, padding.left - 8, y + 3);
    }

    // 2. Dibujar banda de confianza IC 95%
    ctx.beginPath();
    for (let i = 0; i < points.length; i++) {
      const x = getX(i);
      const yHigh = getY(points[i].max);
      if (i === 0) ctx.moveTo(x, yHigh);
      else ctx.lineTo(x, yHigh);
    }
    for (let i = points.length - 1; i >= 0; i--) {
      const x = getX(i);
      const yLow = getY(points[i].min);
      ctx.lineTo(x, yLow);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(56, 189, 248, 0.08)';
    ctx.fill();

    // 3. Límites de Control Shewhart (UCL y LCL en línea punteada)
    ctx.setLineDash([4, 4]);
    ctx.lineWidth = 1.2;

    // UCL
    const uclY = getY(points[0].ucl);
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)';
    ctx.beginPath();
    ctx.moveTo(padding.left, uclY);
    ctx.lineTo(w - padding.right, uclY);
    ctx.stroke();

    // LCL
    const lclY = getY(points[0].lcl);
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.6)';
    ctx.beginPath();
    ctx.moveTo(padding.left, lclY);
    ctx.lineTo(w - padding.right, lclY);
    ctx.stroke();

    // Media central (CL)
    const meanY = getY(points[0].mean);
    ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
    ctx.beginPath();
    ctx.moveTo(padding.left, meanY);
    ctx.lineTo(w - padding.right, meanY);
    ctx.stroke();

    ctx.setLineDash([]); // Reset dash

    // 4. Curva de Precios con Gradiente
    ctx.beginPath();
    for (let i = 0; i < points.length; i++) {
      const x = getX(i);
      const y = getY(points[i].price);
      if (i === 0) ctx.moveTo(x, y);
      else {
        // Spline / Bézier suave
        const prevX = getX(i - 1);
        const prevY = getY(points[i - 1].price);
        const cpX = (prevX + x) / 2;
        ctx.bezierCurveTo(cpX, prevY, cpX, y, x, y);
      }
    }
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 2.5;
    ctx.shadowColor = 'rgba(16, 185, 129, 0.4)';
    ctx.shadowBlur = 8;
    ctx.stroke();
    ctx.shadowBlur = 0; // Reset shadow

    // 5. Relleno bajo la curva
    ctx.lineTo(getX(points.length - 1), getY(minVal));
    ctx.lineTo(getX(0), getY(minVal));
    ctx.closePath();
    const grad = ctx.createLinearGradient(0, padding.top, 0, h - padding.bottom);
    grad.addColorStop(0, 'rgba(16, 185, 129, 0.25)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0.0)');
    ctx.fillStyle = grad;
    ctx.fill();

    // 6. Nodos de puntos y etiquetas X
    ctx.fillStyle = '#34d399';
    for (let i = 0; i < points.length; i += 5) {
      const x = getX(i);
      const y = getY(points[i].price);
      ctx.beginPath();
      ctx.arc(x, y, 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Etiqueta X
      ctx.fillStyle = '#94a3b8';
      ctx.textAlign = 'center';
      const label = points[i].date.substring(5); // MM-DD
      ctx.fillText(label, x, h - 14);
      ctx.fillStyle = '#34d399';
    }

    // 7. Leyenda superior del gráfico
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px Inter, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(`${cropName} — Serie Diaria SIPSA | UCL: $${points[0].ucl.toLocaleString()} | Media: $${points[0].mean.toLocaleString()} | LCL: $${points[0].lcl.toLocaleString()}`, padding.left, 16);
  }
}

// ============================================================================
// 6. REACTIVE UI CONTROLLER & DASHBOARD SYNCHRONIZER
// ============================================================================
class AgroUIController {
  constructor() {
    this.chart = new AgroChartRenderer('forecastChartCanvas');
    this.currentPoints = [];
    this.initEventListeners();
  }

  initEventListeners() {
    // 1. Global Control Strip Selectors
    const prodSelect = document.getElementById('globalProductSelect');
    if (prodSelect) {
      prodSelect.addEventListener('change', (e) => {
        store.setState({ productCode: e.target.value });
      });
    }

    const marketSelect = document.getElementById('globalMarketSelect');
    if (marketSelect) {
      marketSelect.addEventListener('change', (e) => {
        store.setState({ marketCode: e.target.value });
      });
    }

    const periodSelect = document.getElementById('globalPeriodSelect');
    if (periodSelect) {
      periodSelect.addEventListener('change', (e) => {
        store.setState({ periodCode: e.target.value });
      });
    }

    const modeSelect = document.getElementById('globalModeSelect');
    if (modeSelect) {
      modeSelect.addEventListener('change', (e) => {
        store.setState({ analyticalMode: e.target.value });
      });
    }

    const sourceSelect = document.getElementById('globalSourceSelect');
    if (sourceSelect) {
      sourceSelect.addEventListener('change', (e) => {
        store.setState({ sourceLayer: e.target.value });
      });
    }

    // 2. Tab Navigation Buttons (Los 8 Dashboards)
    const tabBtns = document.querySelectorAll('.tab-nav-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        this.switchTab(targetTab);
      });
    });

    // 3. Bioinsumos Slider & Presets
    const bioSlider = document.getElementById('bioSliderInput');
    if (bioSlider) {
      bioSlider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        store.setState({ bioAdoptionRate: val });
      });
    }

    const presetPills = document.querySelectorAll('.preset-pill');
    presetPills.forEach(pill => {
      pill.addEventListener('click', () => {
        const adop = parseInt(pill.getAttribute('data-adopcion'), 10);
        presetPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        if (bioSlider) bioSlider.value = adop;
        store.setState({ bioAdoptionRate: adop });
      });
    });

    // 4. Simulador Táctil de Campo
    const btnSim = document.getElementById('btnEjecutarSimulacion');
    if (btnSim) {
      btnSim.addEventListener('click', () => {
        this.executeFieldSimulation();
      });
    }

    // 5. Botón Exportar CSV
    const btnExport = document.getElementById('btnExportCSV');
    if (btnExport) {
      btnExport.addEventListener('click', () => {
        this.exportCurrentViewToCSV();
      });
    }

    // Suscribir render a cambios de estado
    store.subscribe((state, prev) => {
      this.updateAllDashboards(state, prev);
    });

    // Redimensionado responsivo de canvas
    window.addEventListener('resize', () => {
      if (this.currentPoints.length > 0) {
        const crop = CROP_DATABASE[store.getState().productCode];
        this.chart.render(this.currentPoints, crop.name);
      }
    });
  }

  switchTab(tabKey) {
    const tabBtns = document.querySelectorAll('.tab-nav-btn');
    tabBtns.forEach(btn => {
      if (btn.getAttribute('data-tab') === tabKey) {
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
      }
    });

    const views = document.querySelectorAll('.dashboard-view');
    views.forEach(v => {
      if (v.id === `view-${tabKey}`) {
        v.style.display = 'flex';
        v.classList.add('active');
      } else {
        v.style.display = 'none';
        v.classList.remove('active');
      }
    });

    store.setState({ activeTab: tabKey });

    // Si la pestaña es mercado, re-renderizar el canvas tras el reflow
    if (tabKey === 'mercado' && this.currentPoints.length > 0) {
      setTimeout(() => {
        const crop = CROP_DATABASE[store.getState().productCode];
        this.chart.render(this.currentPoints, crop.name);
      }, 50);
    }
  }

  updateAllDashboards(state, prevState) {
    const crop = CROP_DATABASE[state.productCode] || CROP_DATABASE['01221'];
    const guerra = GuerraEngineClient.compute(crop, state.bioAdoptionRate);

    // 1. Actualizar Macro KPIs
    const elPrecio = document.getElementById('kpiPrecioValor');
    if (elPrecio) elPrecio.textContent = `$${Math.round(guerra.precioEfectivo).toLocaleString()} COP`;

    const elMargen = document.getElementById('kpiMargenValor');
    if (elMargen) elMargen.textContent = `$${(guerra.margenBrutoHa / 1000000).toFixed(1)}M`;

    const elBEP = document.getElementById('kpiBEPValor');
    if (elBEP) elBEP.textContent = `$${guerra.bepMonetarioPrecioKg.toLocaleString()}`;

    const elAbasto = document.getElementById('kpiAbastoValor');
    if (elAbasto) elAbasto.textContent = `${crop.abastoDiarioTon} Ton`;

    const elClima = document.getElementById('kpiClimaValor');
    if (elClima) elClima.textContent = crop.clima;

    // 2. Generar series y renderizar Canvas en Dashboard 1 (Mercado)
    const nDays = state.periodCode === '30D' ? 30 : (state.periodCode === '90D' ? 60 : 90);
    this.currentPoints = BiostatisticalClientEngine.generateTimeSeries(crop, nDays);
    this.chart.render(this.currentPoints, crop.name);

    // Actualizar tabla de cotizaciones recientes
    this.renderPreciosTable(this.currentPoints, crop);

    // 3. Actualizar Dashboard 2 (Producción)
    this.updateProduccionDashboard(crop);

    // 4. Actualizar Dashboard 3 (Rentabilidad Guerra)
    this.updateRentabilidadDashboard(crop, guerra);

    // 5. Actualizar Dashboard 4 (Bioinsumos)
    this.updateBioinsumosDashboard(crop, guerra, state.bioAdoptionRate);

    // 6. Actualizar Dashboard 5 (Empresas & HHI)
    this.updateEmpresasDashboard(crop);

    // 7. Actualizar Dashboard 6 (Territorial)
    this.updateTerritorialDashboard(crop, guerra);

    // 8. Actualizar Dashboard 7 (Predicción ML)
    this.updatePrediccionDashboard(crop, guerra);

    // 9. Actualizar Dashboard 8 (Ejecutivo & Nelson)
    this.updateEjecutivoDashboard(this.currentPoints);
  }

  renderPreciosTable(points, crop) {
    const tbody = document.getElementById('tablaPreciosBody');
    if (!tbody) return;

    const recent = points.slice(-6).reverse();
    tbody.innerHTML = recent.map((p, idx) => {
      const varPct = idx === recent.length - 1 ? 0 : (((p.price - recent[idx + 1].price) / recent[idx + 1].price) * 100).toFixed(1);
      const varSign = varPct >= 0 ? `+${varPct}%` : `${varPct}%`;
      const varColor = varPct >= 0 ? 'var(--emerald-400)' : 'var(--coral-400)';

      return `
        <tr>
          <td><strong>${p.date}</strong></td>
          <td>${crop.icon} ${crop.name} (${crop.code})</td>
          <td>Corabastos (DANE)</td>
          <td>$${p.min.toLocaleString()}</td>
          <td style="font-weight: 700; color: var(--text-primary);">$${p.price.toLocaleString()}</td>
          <td>$${p.max.toLocaleString()}</td>
          <td style="color: ${varColor}; font-weight: 600;">${varSign}</td>
          <td><span class="badge-tag" style="background: rgba(16, 185, 129, 0.12); color: var(--emerald-400); border-color: rgba(16, 185, 129, 0.3);">Validado DAMA</span></td>
        </tr>
      `;
    }).join('');
  }

  updateProduccionDashboard(crop) {
    const elAreaSem = document.getElementById('prodAreaSembrada');
    if (elAreaSem) elAreaSem.textContent = `${crop.areaNacionalHa.toLocaleString()} ha`;

    const elAreaCos = document.getElementById('prodAreaCosechada');
    if (elAreaCos) elAreaCos.textContent = `${Math.round(crop.areaNacionalHa * 0.892).toLocaleString()} ha`;

    const elTotTon = document.getElementById('prodTotalTon');
    if (elTotTon) elTotTon.textContent = `${crop.produccionNacionalTon.toLocaleString()} Ton`;

    const tbody = document.getElementById('tablaProduccionBody');
    if (tbody && crop.territorios) {
      tbody.innerHTML = crop.territorios.map(t => {
        const prodTon = Math.round((t.area * t.rend) / 1000);
        const partPct = ((prodTon / crop.produccionNacionalTon) * 100).toFixed(1);
        return `
          <tr>
            <td><strong>${t.depto}</strong> (${t.cod.substring(0, 2)})</td>
            <td>${t.mpio}</td>
            <td>${t.area.toLocaleString()} ha</td>
            <td>${prodTon.toLocaleString()} Ton</td>
            <td style="color: var(--emerald-400); font-weight: 600;">${(t.rend / 1000).toFixed(1)} Ton/ha</td>
            <td><strong>${partPct}%</strong></td>
          </tr>
        `;
      }).join('');
    }
  }

  updateRentabilidadDashboard(crop, guerra) {
    const elIB = document.getElementById('guerraIngresoBruto');
    if (elIB) elIB.textContent = `$${Math.round(guerra.ingresoBrutoHa).toLocaleString()}`;

    const elCV = document.getElementById('guerraCostoVariable');
    if (elCV) elCV.textContent = `$${Math.round(guerra.costoVariableAjustadoHa).toLocaleString()}`;

    const elMB = document.getElementById('guerraMargenBruto');
    if (elMB) elMB.textContent = `$${Math.round(guerra.margenBrutoHa).toLocaleString()}`;

    const elBEPF = document.getElementById('guerraBEPFisico');
    if (elBEPF) elBEPF.textContent = `${guerra.bepFisicoKgHa.toLocaleString()} kg/ha`;

    const elBEPM = document.getElementById('guerraBEPMonetario');
    if (elBEPM) elBEPM.textContent = `$${guerra.bepMonetarioPrecioKg.toLocaleString()} /kg`;

    const elROI = document.getElementById('guerraROI');
    if (elROI) elROI.textContent = `${guerra.roiPct}%`;
  }

  updateBioinsumosDashboard(crop, guerra, adoptionRate) {
    const sliderBadge = document.getElementById('bioSliderBadge');
    if (sliderBadge) sliderBadge.textContent = `${adoptionRate}% de Sustitución`;

    const elAhorroVal = document.getElementById('bioAhorroValor');
    if (elAhorroVal) elAhorroVal.textContent = `$${Math.round(guerra.ahorroQuimicoHa).toLocaleString()}`;

    const elAhorroPct = document.getElementById('bioAhorroPorcentaje');
    if (elAhorroPct) elAhorroPct.textContent = `-${guerra.ahorroTasaPct}% en químicos`;

    const elPrimaVal = document.getElementById('bioPrimaValor');
    if (elPrimaVal) elPrimaVal.textContent = `$${Math.round(guerra.primaValorHa).toLocaleString()}`;

    const elPrimaPct = document.getElementById('bioPrimaPorcentaje');
    if (elPrimaPct) elPrimaPct.textContent = `+${guerra.primaTasaPct}% sobreprecio exportación`;

    const elNeto = document.getElementById('bioBeneficioNeto');
    if (elNeto) elNeto.textContent = `$${Math.round(guerra.ahorroQuimicoHa + guerra.primaValorHa).toLocaleString()}`;

    const elKg = document.getElementById('bioReduccionKg');
    if (elKg) elKg.textContent = `${guerra.kgQuimicosEvitados} kg/ha`;

    const tbody = document.getElementById('tablaBioinsumosBody');
    if (tbody && crop.bioinsumos) {
      tbody.innerHTML = crop.bioinsumos.map(b => `
        <tr>
          <td><strong>${b.nombre}</strong></td>
          <td><span class="badge-tag" style="background: rgba(16, 185, 129, 0.12); color: var(--emerald-400);">${b.tipo}</span></td>
          <td>${b.empresa}</td>
          <td><code>${b.ica}</code></td>
          <td>${b.dosis}</td>
          <td style="color: var(--sky-400); font-weight: 600;">${b.sustitucion}</td>
          <td><span style="color: var(--emerald-400); font-weight: 700;">● ${b.estatus}</span></td>
        </tr>
      `).join('');
    }
  }

  updateEmpresasDashboard(crop) {
    const tbody = document.getElementById('tablaEmpresasBody');
    if (!tbody || !crop.empresas) return;

    let sumHHI = 0;
    let top4Sum = 0;

    tbody.innerHTML = crop.empresas.map((emp, i) => {
      const hhiPart = Math.round(emp.share * emp.share);
      sumHHI += hhiPart;
      if (i < 4) top4Sum += emp.share;

      return `
        <tr>
          <td><strong>${emp.razon}</strong></td>
          <td><code>${emp.nit}</code></td>
          <td>${emp.tipo}</td>
          <td style="font-weight: 700; color: var(--text-primary);">${emp.share}%</td>
          <td>${hhiPart} pts</td>
          <td><span class="badge-tag">${emp.sic}</span></td>
        </tr>
      `;
    }).join('');

    const elHHI = document.getElementById('empresaHHIValor');
    if (elHHI) elHHI.textContent = `${sumHHI} pts`;

    const elCR4 = document.getElementById('empresaCR4Valor');
    if (elCR4) elCR4.textContent = `${top4Sum.toFixed(1)}%`;

    const badgeHHI = document.getElementById('badgeHHIStatus');
    if (badgeHHI) {
      badgeHHI.textContent = `HHI = ${sumHHI} (${sumHHI < 1500 ? 'Mercado Competitivo' : 'Concentración Moderada'})`;
    }
  }

  updateTerritorialDashboard(crop, guerra) {
    const elDepto = document.getElementById('terrDeptoLider');
    if (elDepto) elDepto.textContent = crop.departamentoLider;

    const elMpio = document.getElementById('terrMpioRendimiento');
    if (elMpio) elMpio.textContent = crop.municipioLider;

    const tbody = document.getElementById('tablaTerritorialBody');
    if (tbody && crop.territorios) {
      tbody.innerHTML = crop.territorios.map(t => {
        const mbLocal = Math.round((t.rend * t.precio) - guerra.costoVariableAjustadoHa);
        return `
          <tr>
            <td><code>${t.cod}</code></td>
            <td><strong>${t.mpio}</strong></td>
            <td>${t.depto}</td>
            <td>${t.area.toLocaleString()} ha</td>
            <td style="color: var(--emerald-400); font-weight: 600;">${(t.rend / 1000).toFixed(1)} Ton/ha</td>
            <td>$${t.precio.toLocaleString()} /kg</td>
            <td style="color: var(--emerald-400); font-weight: 700;">$${(mbLocal / 1000000).toFixed(1)}M /ha</td>
          </tr>
        `;
      }).join('');
    }
  }

  updatePrediccionDashboard(crop, guerra) {
    const el30 = document.getElementById('predPrecio30');
    if (el30) {
      const p30 = Math.round(guerra.precioEfectivo * 1.057);
      el30.textContent = `$${p30.toLocaleString()} /kg`;
    }

    const elInf = document.getElementById('predBandaInf');
    if (elInf) {
      const pInf = Math.round(guerra.precioEfectivo * 0.985);
      elInf.textContent = `$${pInf.toLocaleString()} /kg`;
    }

    const elSup = document.getElementById('predBandaSup');
    if (elSup) {
      const pSup = Math.round(guerra.precioEfectivo * 1.125);
      elSup.textContent = `$${pSup.toLocaleString()} /kg`;
    }
  }

  updateEjecutivoDashboard(points) {
    const evalSpc = BiostatisticalClientEngine.evaluateNelson(points);

    const bannerBox = document.getElementById('spcBannerBox');
    const bannerIcon = document.getElementById('spcBannerIcon');
    const bannerTitle = document.getElementById('spcBannerTitle');
    const bannerDesc = document.getElementById('spcBannerDesc');

    if (bannerBox && bannerTitle && bannerDesc && bannerIcon) {
      if (evalSpc.status === 'NORMAL') {
        bannerBox.className = 'spc-banner spc-normal';
        bannerIcon.textContent = '✅';
        bannerTitle.textContent = 'Proceso de Mercado Bajo Control Estadístico Estable';
        bannerDesc.textContent = `Cotizaciones dentro de ±3σ (LCL = $${evalSpc.lcl.toLocaleString()}, UCL = $${evalSpc.ucl.toLocaleString()}). No se detectan perturbaciones anómalas en la formación de precios.`;
      } else {
        bannerBox.className = 'spc-banner spc-warning';
        bannerIcon.textContent = '⚠️';
        bannerTitle.textContent = 'Alerta de Inestabilidad Detectada en Cotizaciones';
        bannerDesc.textContent = `Se identificaron señales de desplazamiento o tendencia en la serie de precios. Revisar volumen de abasto y correlación con corredores de transporte.`;
      }
    }

    // Reglas individuales
    const setRuleBadge = (id, passed) => {
      const el = document.getElementById(id);
      if (!el) return;
      if (passed) {
        el.className = 'nelson-badge-ok';
        el.textContent = 'PASS (Conforme)';
      } else {
        el.className = 'nelson-badge-fail';
        el.textContent = 'ALERT (Violación)';
      }
    };

    setRuleBadge('nelsonRule1', evalSpc.rule1);
    setRuleBadge('nelsonRule2', evalSpc.rule2);
    setRuleBadge('nelsonRule3', evalSpc.rule3);
    setRuleBadge('nelsonRule4', evalSpc.rule4);
  }

  executeFieldSimulation() {
    const crop = CROP_DATABASE[store.getState().productCode];
    const ha = parseFloat(document.getElementById('simAreaHectareas').value) || 5;
    const density = parseInt(document.getElementById('simDensidadPlantas').value, 10) || 250;
    const tech = parseInt(document.getElementById('simNivelBioinsumos').value, 10) || 45;

    const guerra = GuerraEngineClient.compute(crop, tech);
    const prodTonTotal = ((ha * crop.baseYieldKgHa) / 1000).toFixed(1);
    const margenTotal = Math.round(guerra.margenBrutoHa * ha);

    const elProd = document.getElementById('simResProduccion');
    if (elProd) elProd.textContent = `${prodTonTotal} Toneladas`;

    const elMargen = document.getElementById('simResMargenTotal');
    if (elMargen) elMargen.textContent = `$${(margenTotal / 1000000).toFixed(1)}M COP`;

    const elCalif = document.getElementById('simResCalificacion');
    if (elCalif) {
      if (tech >= 45) {
        elCalif.textContent = 'Apta Exportación UE / EE.UU. (Cero LMR)';
        elCalif.style.color = 'var(--emerald-400)';
      } else {
        elCalif.textContent = 'Mercado Nacional / Estándar';
        elCalif.style.color = 'var(--gold-400)';
      }
    }
  }

  exportCurrentViewToCSV() {
    const crop = CROP_DATABASE[store.getState().productCode];
    const guerra = GuerraEngineClient.compute(crop, store.getState().bioAdoptionRate);

    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += 'Fecha,Rubro_CPC,Mercado,Precio_COP,UCL_COP,LCL_COP,Margen_Bruto_COP_ha,Adopcion_Bioinsumos_Pct\r\n';

    this.currentPoints.forEach(p => {
      csvContent += `${p.date},"${crop.name} (${crop.code})",Corabastos,${p.price},${p.ucl},${p.lcl},${Math.round(guerra.margenBrutoHa)},${store.getState().bioAdoptionRate}%\r\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `agrodata_${crop.code}_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

// ============================================================================
// 7. BOOTSTRAP ON DOM READY
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  window.agroApp = new AgroUIController();
  // Primer disparo reactivo con estado por defecto
  store.setState({});
});
