-- ==============================================================================
-- AGROSTAT DATA INTELLIGENCE PLATFORM — SEEDS INICIALES
-- Mercados Mayoristas Principales y Taxonomía Base de Productos Agrícolas (DANE)
-- ==============================================================================

-- 1. Mercados Mayoristas Principales de Colombia
INSERT INTO dim_geografia (divipola_codigo, departamento_codigo, departamento_nombre, municipio_nombre, region_natural, latitud, longitud)
VALUES 
    ('11001', '11', 'Bogotá D.C.', 'Bogotá, D.C.', 'Andina', 4.7110, -74.0721),
    ('76001', '76', 'Valle del Cauca', 'Cali', 'Pacífica', 3.4516, -76.5320),
    ('05001', '05', 'Antioquia', 'Medellín', 'Andina', 6.2442, -75.5812),
    ('08001', '08', 'Atlántico', 'Barranquilla', 'Caribe', 10.9685, -74.7813),
    ('54001', '54', 'Norte de Santander', 'Cúcuta', 'Andina', 7.8939, -72.5078),
    ('68001', '68', 'Santander', 'Bucaramanga', 'Andina', 7.1254, -73.1198)
ON CONFLICT (divipola_codigo) DO NOTHING;

INSERT INTO dim_mercado_abasto (mercado_id, nombre_central, divipola_municipio, tipo_mercado, capacidad_toneladas_dia)
VALUES 
    ('CORABASTOS', 'Corporación de Abastos de Bogotá S.A. (Corabastos)', '11001', 'Central Mayorista Nacional', 12500.0),
    ('CAVASA', 'Central de Abastecimientos del Valle del Cauca (Cavasa)', '76001', 'Central Mayorista Regional', 3500.0),
    ('CMA_MEDELLIN', 'Central Mayorista de Antioquia (Itagüí / Medellín)', '05001', 'Central Mayorista Regional', 4500.0),
    ('GRANABASTOS', 'Gran Central de Abastos del Caribe (Granabastos)', '08001', 'Central Mayorista Regional', 2000.0),
    ('CENABASTOS', 'Central de Abastos de Cúcuta (Cenabastos)', '54001', 'Central Mayorista Fronteriza', 1800.0),
    ('CENTROABASTOS_BGA', 'Centroabastos Bucaramanga', '68001', 'Central Mayorista Regional', 2200.0)
ON CONFLICT (mercado_id) DO NOTHING;

-- 2. Productos Agrícolas Estratégicos (Taxonomía CPC Ver. 2.1 A.C.)
INSERT INTO dim_producto (producto_cpc_codigo, nombre_comun, nombre_cientifico, grupo_agricola, subgrupo_agricola, es_perecedero, factor_conversion_kg)
VALUES 
    ('01221.01', 'Aguacate Hass', 'Persea americana Mill. cv. Hass', 'Frutas', 'Frutas Tropicales y Subtropicales', TRUE, 1.0),
    ('01221.02', 'Aguacate Papelillo / Lorena', 'Persea americana Mill.', 'Frutas', 'Frutas Tropicales', TRUE, 1.0),
    ('01211.01', 'Plátano Hartón Verde', 'Musa paradisiaca L.', 'Frutas / Musáceas', 'Plátanos', TRUE, 1.0),
    ('01212.01', 'Banano Común / Cavendish', 'Musa acuminata Colla', 'Frutas / Musáceas', 'Bananos', TRUE, 1.0),
    ('01510.01', 'Papa Pastusa', 'Solanum tuberosum L.', 'Tubérculos', 'Papas', TRUE, 1.0),
    ('01510.02', 'Papa Diacol Capiro (Industrial)', 'Solanum tuberosum L.', 'Tubérculos', 'Papas', TRUE, 1.0),
    ('01241.01', 'Cebolla Cabezona Roja', 'Allium cepa L.', 'Hortalizas', 'Hortalizas de Bulbo', TRUE, 1.0),
    ('01241.02', 'Cebolla Junca / Larga', 'Allium fistulosum L.', 'Hortalizas', 'Hortalizas de Tallo', TRUE, 1.0),
    ('01231.01', 'Tomate Chonto', 'Solanum lycopersicum L.', 'Hortalizas', 'Hortalizas de Fruto', TRUE, 1.0),
    ('01111.01', 'Arroz Paddy Verde', 'Oryza sativa L.', 'Cereales', 'Arroz', FALSE, 1.0),
    ('01121.01', 'Maíz Amarillo Tecnificado', 'Zea mays L.', 'Cereales', 'Maíz', FALSE, 1.0),
    ('01611.01', 'Café Pergamino Seco', 'Coffea arabica L.', 'Cultivos Agroindustriales', 'Café', FALSE, 1.0),
    ('01441.01', 'Cacao en Grano Fermentado', 'Theobroma cacao L.', 'Cultivos Agroindustriales', 'Cacao', FALSE, 1.0)
ON CONFLICT (producto_cpc_codigo) DO NOTHING;
