-- ============================================================================
-- SEMILLAS MAESTRAS: DIVIPOLA, CPC v2.1 Y BIOINSUMOS
-- Fuentes: DANE / ICA / SIPSA
-- ============================================================================

-- 1. Insertar Productos CPC v2.1
INSERT INTO dwh_star.dim_producto_cpc (codigo_cpc, nombre_producto, categoria_agricola, unidad_comercial, es_perecedero) VALUES
('01211', 'Aguacate Hass', 'Frutales', 'KILOGRAMO', TRUE),
('01311', 'Café Verde Grano', 'Café y Té', 'KILOGRAMO', FALSE),
('01212', 'Plátano Hartón', 'Plátano y Banano', 'KILOGRAMO', TRUE),
('01221', 'Tomate Chonto', 'Hortalizas', 'KILOGRAMO', TRUE),
('01231', 'Papa Pastusa', 'Tubérculos', 'KILOGRAMO', TRUE),
('01121', 'Maíz Amarillo Tecnificado', 'Cereales', 'KILOGRAMO', FALSE),
('01214', 'Cítricos Naranja Valencia', 'Frutales', 'KILOGRAMO', TRUE),
('01321', 'Cacao en Grano Seco', 'Cacao', 'KILOGRAMO', FALSE)
ON CONFLICT (codigo_cpc) DO NOTHING;

-- 2. Insertar Centrales de Abasto Mayoristas
INSERT INTO dwh_star.dim_mercado_abasto (codigo_mercado, nombre_central, ciudad_sede) VALUES
('CORABASTOS', 'Corabastos Bogotá D.C.', 'Bogotá D.C.'),
('CMA_MEDELLIN', 'Central Mayorista de Antioquia', 'Medellín'),
('CAVASA', 'Cavasa Valle del Cauca', 'Cali')
ON CONFLICT (codigo_mercado) DO NOTHING;

-- 3. Insertar Catálogo de Bioinsumos ICA
INSERT INTO dwh_star.dim_bioinsumo (nombre_comercial, tipo_bioinsumo, ingrediente_activo, empresa_titular, registro_ica) VALUES
('BioNitrogen-Fix Plus', 'Biofertilizante Fijador N', 'Azospirillum brasilense', 'BioAgro Colombia S.A.S.', 'ICA-FERT-2021-0045'),
('FosfoSolubil Pro', 'Biofertilizante Solubilizador P', 'Pseudomonas putida + Bacillus subtilis', 'MicroBioTech Andina', 'ICA-FERT-2020-0089'),
('TrichoShield Max', 'Biocontrolador Fúngico', 'Trichoderma harzianum cepa TH-01', 'AgroBiológicos del Huila', 'ICA-BIOC-2022-0112'),
('BacillusThur Control', 'Biocontrolador Larvicida', 'Bacillus thuringiensis kurstaki', 'EcoAgro Soluciones', 'ICA-BIOC-2019-0033')
ON CONFLICT (registro_ica) DO NOTHING;
