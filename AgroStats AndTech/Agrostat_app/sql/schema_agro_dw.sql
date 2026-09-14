-- ==============================================================================
-- AGROSTAT DATA INTELLIGENCE PLATFORM — DATA WAREHOUSE DDL SCHEMA
-- Arquitectura Dimensional Kimball (Star Schema) / Capa Gold
-- Compatible con: PostgreSQL 14+ y DuckDB 0.9+
-- Normativa: DAMA-BOK (Data Modeling & Quality) / SWEBOK Cap. 2 / ISO 7870 (SPC)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. DIMENSIONES CONFORMADAS (CANONICAL DIMENSIONS)
-- ------------------------------------------------------------------------------

-- Dimensión 1: Tiempo (Granularidad diaria con jerarquías)
CREATE TABLE IF NOT EXISTS dim_tiempo (
    fecha_key INT PRIMARY KEY,                       -- Formato YYYYMMDD (ej. 20260914)
    fecha_completa DATE NOT NULL UNIQUE,
    anio INT NOT NULL CHECK (anio >= 2000 AND anio <= 2100),
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12),
    nombre_mes VARCHAR(20) NOT NULL,
    dia_mes INT NOT NULL CHECK (dia_mes >= 1 AND dia_mes <= 31),
    dia_semana INT NOT NULL CHECK (dia_semana >= 1 AND dia_semana <= 7),
    nombre_dia VARCHAR(20) NOT NULL,
    semana_anio INT NOT NULL CHECK (semana_anio >= 1 AND semana_anio <= 53),
    trimestre INT NOT NULL CHECK (trimestre >= 1 AND trimestre <= 4),
    semestre INT NOT NULL CHECK (semestre >= 1 AND semestre <= 2),
    es_fin_semana BOOLEAN NOT NULL DEFAULT FALSE,
    es_festivo_colombia BOOLEAN NOT NULL DEFAULT FALSE
);

-- Dimensión 2: Geografía (DIVIPOLA DANE - División Político-Administrativa)
CREATE TABLE IF NOT EXISTS dim_geografia (
    divipola_codigo VARCHAR(10) PRIMARY KEY,        -- Código DANE 5 dígitos (ej. '11001' Bogotá)
    departamento_codigo VARCHAR(5) NOT NULL,         -- Código DANE 2 dígitos (ej. '11' Bogotá D.C.)
    departamento_nombre VARCHAR(100) NOT NULL,
    municipio_nombre VARCHAR(100) NOT NULL,
    subregion VARCHAR(100),
    region_natural VARCHAR(50) NOT NULL,            -- Andina, Caribe, Pacífica, Orinoquía, Amazonía
    latitud NUMERIC(9, 6),
    longitud NUMERIC(9, 6),
    altitud_cabecera_msnm INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensión 3: Producto Agrícola (Taxonomía CPC Ver. 2.1 A.C. adaptada para Colombia)
CREATE TABLE IF NOT EXISTS dim_producto (
    producto_cpc_codigo VARCHAR(20) PRIMARY KEY,    -- Código Clasificación Central de Productos
    nombre_comun VARCHAR(150) NOT NULL,
    nombre_cientifico VARCHAR(150),
    grupo_agricola VARCHAR(80) NOT NULL,            -- Frutas, Tubérculos, Hortalizas, Cereales, Leguminosas
    subgrupo_agricola VARCHAR(80) NOT NULL,
    es_perecedero BOOLEAN NOT NULL DEFAULT TRUE,
    unidad_comercial_base VARCHAR(30) NOT NULL DEFAULT 'Kilogramo',
    factor_conversion_kg NUMERIC(10, 4) NOT NULL DEFAULT 1.0000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensión 4: Mercado Mayorista (Centrales de Abastos / Plazas)
CREATE TABLE IF NOT EXISTS dim_mercado_abasto (
    mercado_id VARCHAR(30) PRIMARY KEY,             -- CORABASTOS, CAVASA, CENABASTOS, etc.
    nombre_central VARCHAR(150) NOT NULL,
    divipola_municipio VARCHAR(10) NOT NULL,
    tipo_mercado VARCHAR(50) NOT NULL DEFAULT 'Central Mayorista Principal',
    capacidad_toneladas_dia NUMERIC(12, 2),
    direccion VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mercado_geografia FOREIGN KEY (divipola_municipio) REFERENCES dim_geografia(divipola_codigo)
);

-- Dimensión 5: Red Climatológica (Estaciones IDEAM / Reanálisis Satelital)
CREATE TABLE IF NOT EXISTS dim_estacion_clima (
    estacion_codigo VARCHAR(30) PRIMARY KEY,        -- Código IDEAM o ID satelital NASA POWER
    nombre_estacion VARCHAR(150) NOT NULL,
    divipola_municipio VARCHAR(10) NOT NULL,
    tipo_estacion VARCHAR(60) NOT NULL,             -- Pluviométrica, Climatológica Principal, Satélite
    latitud NUMERIC(9, 6) NOT NULL,
    longitud NUMERIC(9, 6) NOT NULL,
    altitud_msnm NUMERIC(8, 2),
    entidad_operadora VARCHAR(50) NOT NULL DEFAULT 'IDEAM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_estacion_geografia FOREIGN KEY (divipola_municipio) REFERENCES dim_geografia(divipola_codigo)
);

-- Dimensión 6: Actores de la Cadena de Valor Agropecuaria
CREATE TABLE IF NOT EXISTS dim_actor_cadena (
    actor_id VARCHAR(30) PRIMARY KEY,               -- NIT o Identificador Registrado
    razon_social VARCHAR(200) NOT NULL,
    tipo_actor VARCHAR(60) NOT NULL,                -- Productor Individual, Asociación, Agroexportador, Mayorista
    gremio_afiliado VARCHAR(100),                   -- Fedearroz, FENALCE, Fedegan, Asocolflores, etc.
    divipola_sede VARCHAR(10),
    es_operador_bmc BOOLEAN NOT NULL DEFAULT FALSE, -- Registrado en Bolsa Mercantil de Colombia
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_actor_geografia FOREIGN KEY (divipola_sede) REFERENCES dim_geografia(divipola_codigo)
);

-- ------------------------------------------------------------------------------
-- 2. TABLAS DE HECHOS (FACT TABLES)
-- ------------------------------------------------------------------------------

-- Hecho 1: Precios Mayoristas Diarios (DANE SIPSA_P)
CREATE TABLE IF NOT EXISTS fact_precios_sipsa (
    precio_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INT NOT NULL,
    producto_cpc_codigo VARCHAR(20) NOT NULL,
    mercado_id VARCHAR(30) NOT NULL,
    precio_minimo_kg NUMERIC(12, 2) NOT NULL CHECK (precio_minimo_kg >= 0),
    precio_medio_kg NUMERIC(12, 2) NOT NULL CHECK (precio_medio_kg >= 0),
    precio_maximo_kg NUMERIC(12, 2) NOT NULL CHECK (precio_maximo_kg >= 0),
    desviacion_estandar NUMERIC(10, 4) DEFAULT 0.0,
    fuente_boletin VARCHAR(50) NOT NULL DEFAULT 'DANE_SIPSA_P',
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fp_tiempo FOREIGN KEY (fecha_key) REFERENCES dim_tiempo(fecha_key),
    CONSTRAINT fk_fp_producto FOREIGN KEY (producto_cpc_codigo) REFERENCES dim_producto(producto_cpc_codigo),
    CONSTRAINT fk_fp_mercado FOREIGN KEY (mercado_id) REFERENCES dim_mercado_abasto(mercado_id),
    CONSTRAINT chk_consistencia_precios CHECK (precio_minimo_kg <= precio_medio_kg AND precio_medio_kg <= precio_maximo_kg)
);

-- Hecho 2: Abastecimiento y Flujo de Alimentos (DANE SIPSA_A)
CREATE TABLE IF NOT EXISTS fact_abastecimiento_sipsa (
    abastecimiento_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INT NOT NULL,
    producto_cpc_codigo VARCHAR(20) NOT NULL,
    mercado_destino_id VARCHAR(30) NOT NULL,
    municipio_origen_divipola VARCHAR(10) NOT NULL,
    volumen_toneladas NUMERIC(12, 3) NOT NULL CHECK (volumen_toneladas >= 0),
    volumen_kilos NUMERIC(15, 2) GENERATED ALWAYS AS (volumen_toneladas * 1000) STORED,
    participacion_mercado_pct NUMERIC(6, 3),
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fa_tiempo FOREIGN KEY (fecha_key) REFERENCES dim_tiempo(fecha_key),
    CONSTRAINT fk_fa_producto FOREIGN KEY (producto_cpc_codigo) REFERENCES dim_producto(producto_cpc_codigo),
    CONSTRAINT fk_fa_mercado_destino FOREIGN KEY (mercado_destino_id) REFERENCES dim_mercado_abasto(mercado_id),
    CONSTRAINT fk_fa_origen_geografia FOREIGN KEY (municipio_origen_divipola) REFERENCES dim_geografia(divipola_codigo)
);

-- Hecho 3: Evaluaciones Agropecuarias Municipales (Agronet / UPRA - EVA)
CREATE TABLE IF NOT EXISTS fact_produccion_agronet (
    produccion_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    anio INT NOT NULL CHECK (anio >= 2000),
    ciclo_periodo VARCHAR(20) NOT NULL,              -- 'Semestre A', 'Semestre B', 'Anual Consolidado'
    producto_cpc_codigo VARCHAR(20) NOT NULL,
    divipola_municipio VARCHAR(10) NOT NULL,
    area_sembrada_ha NUMERIC(12, 2) NOT NULL CHECK (area_sembrada_ha >= 0),
    area_cosechada_ha NUMERIC(12, 2) NOT NULL CHECK (area_cosechada_ha >= 0),
    produccion_toneladas NUMERIC(14, 2) NOT NULL CHECK (produccion_toneladas >= 0),
    rendimiento_t_ha NUMERIC(8, 2) NOT NULL CHECK (rendimiento_t_ha >= 0),
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fpa_producto FOREIGN KEY (producto_cpc_codigo) REFERENCES dim_producto(producto_cpc_codigo),
    CONSTRAINT fk_fpa_geografia FOREIGN KEY (divipola_municipio) REFERENCES dim_geografia(divipola_codigo),
    CONSTRAINT chk_area_cosechada_sembrada CHECK (area_cosechada_ha <= area_sembrada_ha)
);

-- Hecho 4: Climatología y Meteorología Diaria (IDEAM / NASA POWER)
CREATE TABLE IF NOT EXISTS fact_clima_diario (
    clima_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INT NOT NULL,
    estacion_codigo VARCHAR(30) NOT NULL,
    precipitacion_mm NUMERIC(8, 2) NOT NULL CHECK (precipitacion_mm >= 0),
    temperatura_max_celsius NUMERIC(5, 2),
    temperatura_min_celsius NUMERIC(5, 2),
    temperatura_media_celsius NUMERIC(5, 2) NOT NULL,
    humedad_relativa_pct NUMERIC(5, 2) CHECK (humedad_relativa_pct >= 0 AND humedad_relativa_pct <= 100),
    radiacion_solar_mj_m2 NUMERIC(8, 2) CHECK (radiacion_solar_mj_m2 >= 0),
    evapotranspiracion_mm NUMERIC(8, 2) CHECK (evapotranspiracion_mm >= 0),
    indice_anomalia_enso VARCHAR(20) DEFAULT 'NEUTRO', -- 'EL_NINO', 'LA_NINA', 'NEUTRO'
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fc_tiempo FOREIGN KEY (fecha_key) REFERENCES dim_tiempo(fecha_key),
    CONSTRAINT fk_fc_estacion FOREIGN KEY (estacion_codigo) REFERENCES dim_estacion_clima(estacion_codigo)
);

-- Hecho 5: Transacciones Mercantiles y Contratos (Bolsa Mercantil de Colombia - BMC)
CREATE TABLE IF NOT EXISTS fact_transacciones_bmc (
    transaccion_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_key INT NOT NULL,
    producto_cpc_codigo VARCHAR(20) NOT NULL,
    actor_vendedor_id VARCHAR(30) NOT NULL,
    actor_comprador_id VARCHAR(30) NOT NULL,
    volumen_negociado_kg NUMERIC(14, 2) NOT NULL CHECK (volumen_negociado_kg > 0),
    precio_cierre_kg NUMERIC(12, 2) NOT NULL CHECK (precio_cierre_kg > 0),
    valor_total_contrato NUMERIC(16, 2) GENERATED ALWAYS AS (volumen_negociado_kg * precio_cierre_kg) STORED,
    modalidad_rueda VARCHAR(50) NOT NULL DEFAULT 'Registro Factura',
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ft_tiempo FOREIGN KEY (fecha_key) REFERENCES dim_tiempo(fecha_key),
    CONSTRAINT fk_ft_producto FOREIGN KEY (producto_cpc_codigo) REFERENCES dim_producto(producto_cpc_codigo),
    CONSTRAINT fk_ft_vendedor FOREIGN KEY (actor_vendedor_id) REFERENCES dim_actor_cadena(actor_id),
    CONSTRAINT fk_ft_comprador FOREIGN KEY (actor_comprador_id) REFERENCES dim_actor_cadena(actor_id)
);

-- ------------------------------------------------------------------------------
-- 3. ÍNDICES DE RENDIMIENTO (PERFORMANCE & ANALYTICAL INDEXES)
-- ------------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_precios_sipsa_lookup 
    ON fact_precios_sipsa (producto_cpc_codigo, mercado_id, fecha_key);

CREATE INDEX IF NOT EXISTS idx_abastecimiento_sipsa_lookup 
    ON fact_abastecimiento_sipsa (producto_cpc_codigo, mercado_destino_id, fecha_key);

CREATE INDEX IF NOT EXISTS idx_clima_diario_lookup 
    ON fact_clima_diario (estacion_codigo, fecha_key);

CREATE INDEX IF NOT EXISTS idx_produccion_agronet_lookup 
    ON fact_produccion_agronet (producto_cpc_codigo, divipola_municipio, anio);

-- ------------------------------------------------------------------------------
-- 4. VISTAS ANALÍTICAS Y CONTROL ESTADÍSTICO (VIEWS & SPC ANALYTICS)
-- ------------------------------------------------------------------------------

-- Vista 1: Balance Oferta-Demanda y Precios en Centrales Mayoristas
CREATE OR REPLACE VIEW vw_balance_mercado_diario AS
SELECT 
    t.fecha_completa,
    t.anio,
    t.mes,
    t.semana_anio,
    p.producto_cpc_codigo,
    p.nombre_comun AS producto_nombre,
    p.grupo_agricola,
    m.mercado_id,
    m.nombre_central,
    pr.precio_medio_kg,
    COALESCE(ab.volumen_toneladas, 0) AS volumen_ingreso_toneladas,
    (pr.precio_medio_kg * 1000 * COALESCE(ab.volumen_toneladas, 0)) AS valor_estimado_mercado_cop
FROM fact_precios_sipsa pr
JOIN dim_tiempo t ON pr.fecha_key = t.fecha_key
JOIN dim_producto p ON pr.producto_cpc_codigo = p.producto_cpc_codigo
JOIN dim_mercado_abasto m ON pr.mercado_id = m.mercado_id
LEFT JOIN fact_abastecimiento_sipsa ab 
    ON pr.fecha_key = ab.fecha_key 
    AND pr.producto_cpc_codigo = ab.producto_cpc_codigo 
    AND pr.mercado_id = ab.mercado_destino_id;

-- Vista 2: Métricas de Estabilidad y Control Estadístico Shewhart de Precios (3-Sigma)
CREATE OR REPLACE VIEW vw_estabilidad_precios_spc AS
WITH estadisticas_base AS (
    SELECT 
        producto_cpc_codigo,
        mercado_id,
        t.anio,
        t.mes,
        AVG(precio_medio_kg) AS precio_promedio_mensual,
        STDDEV(precio_medio_kg) AS desv_estandar_precio,
        COUNT(*) AS numero_cotizaciones
    FROM fact_precios_sipsa pr
    JOIN dim_tiempo t ON pr.fecha_key = t.fecha_key
    GROUP BY producto_cpc_codigo, mercado_id, t.anio, t.mes
)
SELECT 
    producto_cpc_codigo,
    mercado_id,
    anio,
    mes,
    numero_cotizaciones,
    ROUND(precio_promedio_mensual, 2) AS center_line_media,
    ROUND(precio_promedio_mensual + (3 * COALESCE(desv_estandar_precio, 0)), 2) AS ucl_limite_superior,
    ROUND(GREATEST(0, precio_promedio_mensual - (3 * COALESCE(desv_estandar_precio, 0))), 2) AS lcl_limite_inferior
FROM estadisticas_base;
