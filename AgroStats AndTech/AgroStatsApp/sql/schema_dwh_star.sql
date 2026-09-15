-- ============================================================================
-- DATA WAREHOUSE ANALÍTICO — ESQUEMA ESTRELLA OLAP
-- Metodología: Ralph Kimball (Dimensional Modeling) / ANSI SQL:2023
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS dwh_star;

-- 1. Dimensión Tiempo
CREATE TABLE dwh_star.dim_tiempo (
    tiempo_id INT PRIMARY KEY, -- Formato: YYYYMMDD
    fecha DATE NOT NULL UNIQUE,
    anio SMALLINT NOT NULL,
    mes SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    nombre_mes VARCHAR(15) NOT NULL,
    trimestre SMALLINT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    dia_semana SMALLINT NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
    es_festivo_colombia BOOLEAN NOT NULL DEFAULT FALSE,
    temporada_climatica VARCHAR(20) NOT NULL
);
CREATE INDEX idx_dim_tiempo_anio ON dwh_star.dim_tiempo (anio);

-- 2. Dimensión Producto CPC v2.1
CREATE TABLE dwh_star.dim_producto_cpc (
    codigo_cpc VARCHAR(10) PRIMARY KEY,
    nombre_producto VARCHAR(150) NOT NULL,
    categoria_agricola VARCHAR(80) NOT NULL,
    unidad_comercial VARCHAR(30) NOT NULL DEFAULT 'KILOGRAMO',
    es_perecedero BOOLEAN NOT NULL DEFAULT TRUE
);

-- 3. Dimensión Territorio DIVIPOLA (DANE)
CREATE TABLE dwh_star.dim_territorio_divipola (
    codigo_municipio VARCHAR(10) PRIMARY KEY,
    nombre_municipio VARCHAR(100) NOT NULL,
    codigo_departamento VARCHAR(5) NOT NULL,
    nombre_departamento VARCHAR(100) NOT NULL,
    region_natural VARCHAR(50),
    latitud NUMERIC(9, 6),
    longitud NUMERIC(9, 6),
    altitud_msnm INT
);

-- 4. Dimensión Central de Abasto
CREATE TABLE dwh_star.dim_mercado_abasto (
    mercado_id SERIAL PRIMARY KEY,
    codigo_mercado VARCHAR(30) NOT NULL UNIQUE,
    nombre_central VARCHAR(120) NOT NULL,
    ciudad_sede VARCHAR(100) NOT NULL
);

-- 5. Dimensión Bioinsumos
CREATE TABLE dwh_star.dim_bioinsumo (
    bioinsumo_id SERIAL PRIMARY KEY,
    nombre_comercial VARCHAR(150) NOT NULL,
    tipo_bioinsumo VARCHAR(80) NOT NULL,
    ingrediente_activo VARCHAR(150) NOT NULL,
    empresa_titular VARCHAR(150) NOT NULL,
    registro_ica VARCHAR(50) NOT NULL UNIQUE
);

-- 6. Tabla de Hechos: Cotizaciones Diarias Mayoristas (Particionada)
CREATE TABLE dwh_star.fact_cotizaciones_mayoristas (
    cotizacion_id BIGSERIAL,
    tiempo_id INT NOT NULL REFERENCES dwh_star.dim_tiempo(tiempo_id),
    codigo_cpc VARCHAR(10) NOT NULL REFERENCES dwh_star.dim_producto_cpc(codigo_cpc),
    codigo_municipio VARCHAR(10) NOT NULL REFERENCES dwh_star.dim_territorio_divipola(codigo_municipio),
    mercado_id INT NOT NULL REFERENCES dwh_star.dim_mercado_abasto(mercado_id),
    precio_min_cop_kg NUMERIC(12, 2) NOT NULL,
    precio_max_cop_kg NUMERIC(12, 2) NOT NULL,
    precio_promedio_cop_kg NUMERIC(12, 2) NOT NULL,
    volumen_transado_ton NUMERIC(10, 2) DEFAULT 0.00,
    variacion_7d_pct NUMERIC(6, 2) DEFAULT 0.00,
    PRIMARY KEY (tiempo_id, cotizacion_id)
) PARTITION BY RANGE (tiempo_id);

CREATE TABLE dwh_star.fact_cotizaciones_2026 PARTITION OF dwh_star.fact_cotizaciones_mayoristas
    FOR VALUES FROM (20260101) TO (20270101);

CREATE INDEX idx_fact_cotiz_brin_tiempo ON dwh_star.fact_cotizaciones_mayoristas USING BRIN (tiempo_id);
CREATE INDEX idx_fact_cotiz_prod ON dwh_star.fact_cotizaciones_mayoristas (codigo_cpc);

-- 7. Tabla de Hechos: Rentabilidad y Bioinsumos (Guillermo Guerra IICA)
CREATE TABLE dwh_star.fact_rentabilidad_guerra (
    liquidacion_id BIGSERIAL PRIMARY KEY,
    tiempo_id INT NOT NULL REFERENCES dwh_star.dim_tiempo(tiempo_id),
    codigo_cpc VARCHAR(10) NOT NULL REFERENCES dwh_star.dim_producto_cpc(codigo_cpc),
    codigo_municipio VARCHAR(10) NOT NULL REFERENCES dwh_star.dim_territorio_divipola(codigo_municipio),
    rendimiento_kg_ha NUMERIC(10, 2) NOT NULL,
    precio_base_cop_kg NUMERIC(12, 2) NOT NULL,
    costos_fijos_ha NUMERIC(14, 2) NOT NULL,
    costos_variables_convencional_ha NUMERIC(14, 2) NOT NULL,
    costos_variables_bioinsumos_ha NUMERIC(14, 2) NOT NULL,
    margen_bruto_convencional_ha NUMERIC(14, 2) NOT NULL,
    margen_bruto_bioinsumos_ha NUMERIC(14, 2) NOT NULL,
    ganancia_neta_adicional_ha NUMERIC(14, 2) NOT NULL,
    bep_precio_bioinsumos_cop_kg NUMERIC(12, 2) NOT NULL,
    roi_operativo_bioinsumos_pct NUMERIC(6, 2) NOT NULL
);
