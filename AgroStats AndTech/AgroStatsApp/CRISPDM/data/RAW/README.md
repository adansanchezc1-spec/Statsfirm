# Ingesta completa de las 10 fuentes
python -m imputer.cli --download-all --limit 500

# Descarga individual de una fuente
python -m imputer.cli --source sipsa_precios
python -m imputer.cli --source ideam_pluvio --limit 1000

# Demostración del torneo de imputación inteligente con métricas de varianza
python -m imputer.cli --impute-sample
