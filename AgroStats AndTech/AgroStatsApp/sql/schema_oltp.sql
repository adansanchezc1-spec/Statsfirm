-- ============================================================================
-- ESQUEMA TRANSACCIONAL OLTP (3NF) — AGRODATA INTELLIGENCE PLATFORM
-- Normas: Codd 3NF Relational Theory / PostgreSQL 16 / ISO 27001
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS oltp_core;

-- 1. Tabla de Roles de Usuario (RBAC)
CREATE TABLE oltp_core.roles (
    rol_id SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE, -- 'ADMIN', 'ANALISTA_SENIOR', 'PRODUCTOR', 'AUDITOR'
    descripcion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Usuarios
CREATE TABLE oltp_core.usuarios (
    usuario_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    correo VARCHAR(150) NOT NULL UNIQUE,
    hash_password VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    organizacion VARCHAR(150),
    rol_id INT NOT NULL REFERENCES oltp_core.roles(rol_id),
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bitácora de Ingesta & DataOps Audit
CREATE TABLE oltp_core.bitacora_ingesta (
    pipeline_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fuente_datos VARCHAR(50) NOT NULL, -- 'SIPSA', 'IDEAM', 'UPRA', 'ICA'
    tipo_ingesta VARCHAR(30) NOT NULL, -- 'BATCH_DIARIO', 'STREAMING'
    registros_recibidos INT NOT NULL,
    registros_validos INT NOT NULL,
    registros_cuarentena INT NOT NULL,
    estado_ejecucion VARCHAR(30) NOT NULL, -- 'SUCCESS', 'FAILED', 'WARNING'
    checksum_sha256 VARCHAR(64) NOT NULL,
    mensaje_error TEXT,
    duracion_segundos NUMERIC(8, 2) NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Alertas de Mercado y Eventos Críticos (Reglas de Nelson)
CREATE TABLE oltp_core.alertas_mercado (
    alerta_id BIGSERIAL PRIMARY KEY,
    fecha_alerta DATE NOT NULL,
    codigo_cpc VARCHAR(10) NOT NULL,
    central_abasto VARCHAR(100) NOT NULL,
    tipo_alerta VARCHAR(50) NOT NULL, -- 'SHOCK_3SIGMA', 'CAMBIO_MEDIA', 'TENDENCIA'
    severidad VARCHAR(20) NOT NULL,   -- 'INFO', 'WARNING', 'DANGER'
    detalle JSONB NOT NULL,
    ha_sido_notificada BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alertas_cpc_fecha ON oltp_core.alertas_mercado (codigo_cpc, fecha_alerta);
