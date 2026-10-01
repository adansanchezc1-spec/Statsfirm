# Arquitectura de la Capa Gold, Feature Store y Suite de Cuadernos Jupyter
**Proyecto**: AgroStats AndTech — Plataforma de Inteligencia Agrícola Colombiana  
**Fase PDCO**: DEVELOPMENT  
**Fase SDLC**: Implementation  
**Normas y Estándares**: DAMA-BOK (Feature Engineering & Lakehouse Data Marts), ISO/IEC 25010, SWEBOK Cap. 3, PEP 8  

---

## 1. Visión General del Feature Store y Capa Gold

La **Capa Gold** de AgroStats consolida un diseño híbrido de alto rendimiento para analítica descriptiva, diagnóstica y predictiva:
1. **Motor OLAP Dimensional**: `data/gold/agro_dw.duckdb`, estructurado bajo el Modelo Dimensional de Ralph Kimball (Star Schema) con 6 dimensiones conformadas y 5 tablas de hechos.
2. **Feature Store Analítico**: Persistido en `data/gold/features/` en formato Apache Parquet particionado y tipado, optimizado para entrenamiento distribuido y análisis con Scikit-Learn y Statsmodels:
   - `features_yield_prediction.parquet`: 29 lotes de cosecha con variables edafológicas, biométricas y físico-químicas (`calibre_promedio`, `grados_brix`, `ratio_brix_calibre`, `indice_estres_hidrico`, `indice_calidad_suelo`, `clase_exportacion`).
   - `features_market_forecasting.parquet`: 2,700 observaciones de series temporales diarias de SIPSA (Corabastos, CMA Medellín, Cavasa) acopladas con covariables climáticas IDEAM, rezagos temporales ($t-1, t-7, t-14$), promedios móviles y volatilidad móvil.
   - `features_spc_stability.parquet`: 2,700 registros con límites de control Shewhart ($\bar{X} \pm 3\sigma$) y marcas booleanas vectorizadas de violación para las **Reglas de Nelson 1, 2, 3 y 4**.

---

## 2. Suite de 4 Jupyter Notebooks Especializados

Ubicados en el directorio raíz `notebooks/`, organizados modularmente por capa y propósito analítico:

```
notebooks/
├── 01_silver_curation_eda/
│   └── 01_silver_data_quality_and_eda.ipynb
├── 02_gold_market_forecasting/
│   └── 02_market_price_forecasting_ml.ipynb
├── 03_gold_yield_ml/
│   └── 03_crop_yield_and_exportability_ml.ipynb
└── 04_gold_spc_biostatistics/
    └── 04_spc_biostatistical_process_control.ipynb
```

### 2.1. `01_silver_data_quality_and_eda.ipynb`
- **Enfoque**: Auditoría y Perfilamiento de Calidad de Datos según **DAMA-BOK** y EDA Multivariado.
- **Técnicas**: Evaluación cuantitativa de completitud, unicidad y validez (DIVIPOLA, CPC v2.1). Visualización de dispersión inter-centrales (Seaborn boxplots), mapas de correlación de Pearson y matrices de calor.
- **Outputs**: Diagnóstico 100% libre de duplicados en llaves compuestas y validación de las rutas de promoción a Gold.

### 2.2. `02_market_price_forecasting_ml.ipynb`
- **Enfoque**: Proyección de Series de Tiempo de Precios y Abastecimiento Mayorista con Covariables Meteorológicas.
- **Técnicas**:
  - Descomposición aditiva de series temporales (Tendencia, Estacionalidad, Residuos).
  - Test Aumentado de Dickey-Fuller (ADF) para evaluar estacionariedad.
  - Modelo Econométrico 1: **Holt-Winters** con estacionalidad semanal.
  - Modelo Econométrico 2: **SARIMAX** $(1,1,1) \times (1,0,1)_7$ con precipitación y temperatura como covariables exógenas e intervalos de predicción al 95%.
  - Modelo ML: **Random Forest Lagged Regressor** con ventanas móviles de 7 y 14 días.
- **Outputs**: Tabla comparativa de métricas $MAE, RMSE, MAPE, R^2$ y gráfico proyectivo a 14 días.

### 2.3. `03_crop_yield_and_exportability_ml.ipynb`
- **Enfoque**: Machine Learning Supervisado para Predicción de Rendimiento ($kg/ha$) y Calidad de Exportación.
- **Técnicas**:
  - Ingeniería de características agronómicas (ratios de azúcar/calibre, estrés hídrico, proximidad a pH neutro).
  - Benchmark de modelos mediante **5-Fold Cross Validation**: Ridge Regression, Random Forest Regressor y Gradient Boosting Regressor.
  - Análisis de importancia de variables (**MDI y Permutation Importance**): identificación de los factores limitantes de la cosecha.
  - Clasificación supervisada con **Random Forest Classifier** para categorizar lotes en `PREMIUM_EXPORT`, `ESTANDAR_EXPORT` y `MERCADO_NACIONAL` con matriz de confusión y curvas de calibración.
- **Outputs**: Serialización del modelo óptimo en `data/models/yield_rf_production/` con artefactos `.pkl` y `metadata.json`.

### 2.4. `04_spc_biostatistical_process_control.ipynb`
- **Enfoque**: Control Estadístico de Procesos (SPC) Bioestadístico y Detección de Inestabilidad según **ISO 7870**.
- **Técnicas**:
  - Gráficos Shewhart Individuales ($I-MR$) con bandas visuales $\pm 1\sigma, \pm 2\sigma, \pm 3\sigma$.
  - Implementación vectorial y visualización de las **4 Reglas de Nelson**:
    - *Regla 1*: Outlier extremo $> 3\sigma$ (Shock agudo de oferta).
    - *Regla 2*: 9 puntos consecutivos del mismo lado de la media (Desplazamiento estructural del nivel de precios).
    - *Regla 3*: 6 puntos consecutivos en aumento o descenso continuo (Tendencia).
    - *Regla 4*: 14 puntos alternando arriba y abajo (Oscilación o inestabilidad logística).
  - Evaluación bioestadística de cosechas e **Índices de Capacidad de Proceso ($C_p, C_{pk}$)** frente a tolerancias de exportación aduanera ($10.0^\circ$ a $18.0^\circ$ Brix).

---

## 3. Verificación Automatizada

Todos los cuadernos cuentan con un arnés de verificación automatizado (`scratch/verify_notebooks.py`) que ejecuta programáticamente mediante `nbconvert.preprocessors.ExecutePreprocessor` e `ipykernel` cada celda de código, asegurando cero excepciones, persistencia de outputs gráficos y total reproducibilidad.
