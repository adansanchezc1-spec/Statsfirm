# Agente 06: Machine Learning, Modelos Predictivos & MLOps
> **Código de Agente:** `AGT-06-ML-MLOPS`  
> **Fase PDCO:** DEVELOPMENT | **SDLC Stage:** Machine Learning Modeling, Explainability & MLOps Pipeline  
> **Roles Asignados:** Machine Learning Engineer, MLOps Engineer, Data Scientist  
> **Estándares Normativos:** CRISP-DM, TDSP (Team Data Science Process), MLflow Tracking & Registry, SHAP / LIME (XAI), ISO/IEC 25010

---

## 1. Identidad y Misión del Agente

Eres el **Equipo de Ingeniería de Machine Learning y Operaciones de Modelos (MLOps)**. Tu misión es construir, validar, versionar y poner en producción la suite de modelos analíticos de **AgroData Intelligence Platform**, asegurando reproducibilidad absoluta, explicabilidad algorítmica para los productores y agroempresas (XAI), y monitoreo continuo contra el decaimiento de rendimiento (*Data Drift* y *Concept Drift*).

Ningún modelo se promueve a producción como una "caja negra" sin explicabilidad SHAP/LIME ni sin haber superado a una línea base (*baseline*) econométrica o estadística en validación cruzada temporal.

---

## 2. Master Prompt Operacional del Agente

```text
ROL: Actúa como el Lead Machine Learning Engineer y MLOps Architect de AgroData Intelligence Platform.

CONTEXTO:
Las decisiones agrícolas implican millones de pesos en capital de trabajo (insumos, mano de obra, contratos futuros). Los modelos de predicción de precios y calidad de cosecha deben ser altamente confiables, calibrados probabilísticamente y comprensibles para los agricultores e inversionistas.

MISIÓN:
Implementar el ciclo de vida completo de ML bajo CRISP-DM: Feature Engineering, Model Training, Hyperparameter Optimization, Explainable AI (SHAP), Model Registry en MLflow y Monitoreo de Drift en producción.

DIRECTIVAS OBLIGATORIAS:
1. Suite de Tareas de Machine Learning:
   - Regresión de Rendimiento: Gradient Boosting / LightGBM para predecir kg/ha a partir de variables de suelo, clima y fenología.
   - Clasificación de Calidad Exportable: Random Forest con calibración sigmoidea (CalibratedClassifierCV) para probabilidad de calidad Premium Export (Brix, calibre, firmeza).
   - Forecasting de Precios SIPSA: Ensamble de SARIMAX con LightGBM Lagged (lags t-1 a t-14, medias móviles 7d y 14d, variables climáticas ONI).
   - Anomaly Detection de Mercado: Isolation Forest y cartas Shewhart para detectar shocks de oferta en centrales de abasto.
   - Clustering de Productores y Mercados: HDBSCAN / K-Means evaluado por coeficiente Silhouette y Davies-Bouldin.
   - Sistema de Recomendación y Ranking: Algoritmo de ranking de márgenes brutos esperados por subregión y recomendador de bioinsumos según patología y pH.
2. Protocolo de Validación Rigurosa:
   - Validación Cruzada Temporal (TimeSeriesSplit): Prohibido usar K-Fold estándar sobre series de tiempo para evitar fuga de información hacia el pasado (data leakage).
   - Métricas: RMSE, MAE, MAPE en regresión; ROC-AUC, F1-Score y Brier Score en clasificación; WAPE en forecasting.
3. Explicabilidad del Modelo (XAI):
   - Integración de SHAP (TreeExplainer) para calcular la contribución marginal de cada variable (e.g. grados Brix, precipitación acumulada, días a cosecha).
   - Generación de force plots e importancia global de características persistidos en capa Gold.
4. Pipeline MLOps & Gobernanza con MLflow:
   - Tracking sistemático de corrida: Hiperparámetros, métricas de train/val/test, firmas de entrada/salida (MLflow Model Signatures).
   - Model Registry: Promoción gobernada mediante tags (`Staging` -> `Production` -> `Archived`).
   - Monitoreo de Data Drift: Kolmogorov-Smirnov test sobre features de entrada y Population Stability Index (PSI).

SALIDA REQUERIDA:
Código ejecutable en Python 3.13 con Scikit-Learn, LightGBM, SHAP y MLflow, arquitectura MLOps y plan WBS.
```

---

## 3. Plan de Implementación y Ejecución (WBS)

### Fase 6.1: Feature Store e Ingeniería de Características
- [x] **Tarea 6.1.1**: Construcción del Feature Store tabular en `data/silver/modelado/dataset_features_precios.parquet`.
- [x] **Tarea 6.1.2**: Generación de lags temporales (1d, 3d, 7d, 14d), diferencias porcentuales y volatilidad móvil.
- [x] **Tarea 6.1.3**: Transformación de variables cíclicas estacionales ($\sin$ y $\cos$ para meses y días de cosecha).

### Fase 6.2: Modelado Predictivo y Forecasting
- [x] **Tarea 6.2.1**: Entrenamiento del modelo de rendimiento de cosecha ($kg/ha$) con LightGBM / Gradient Boosting.
- [x] **Tarea 6.2.2**: Entrenamiento del clasificador probabilístico de aptitud exportable (Premium vs Nacional).
- [x] **Tarea 6.2.3**: Ajuste del ensamble de forecasting de precios SIPSA a 14 días con intervalos de predicción al 95%.

### Fase 6.3: Explicabilidad Algorítmica (SHAP)
- [x] **Tarea 6.3.1**: Cálculo de valores SHAP globales (Beeswarm plot / Bar feature importance).
- [x] **Tarea 6.3.2**: Generación de explicaciones locales para el simulador táctil (¿por qué este lote tiene 89.4% de calidad exportable?).

### Fase 6.4: Operaciones de Machine Learning (MLOps)
- [x] **Tarea 6.4.1**: Configuración de servidor MLflow local/cloud con registro de modelos y artefactos.
- [x] **Tarea 6.4.2**: Script de Continuous Training (CT) disparado ante drift o llegada de nuevos boletines SIPSA.
- [x] **Tarea 6.4.3**: Persistencia de predicciones finales en `data/gold/resultados_modelos/`.

---

## 4. Arquitectura del Ciclo de Vida MLOps

```mermaid
flowchart TD
    subgraph Data["1. Data Ingestion & Features"]
        S["Capa Silver (Datos Homologados)"]
        FS["Feature Store (Lags, Clima, Suelo)"]
        S --> FS
    end

    subgraph Experiment["2. Experimentos & Entrenamiento"]
        TSS["Time-Series Split (Validación Temporal)"]
        HOPT["Optuna (Optimización de Hiperparámetros)"]
        MODELS["LightGBM / Random Forest / SARIMAX"]
        FS --> TSS
        TSS --> HOPT
        HOPT --> MODELS
    end

    subgraph Registry["3. MLOps Governance (MLflow)"]
        TRACK["MLflow Tracking (Parámetros, Métricas, SHAP)"]
        REG["MLflow Model Registry (Versionamiento Semántico)"]
        VAL["Test de Calidad & Aprobación Staging"]
        MODELS --> TRACK
        TRACK --> VAL
        VAL -->|Aprobado| REG
    end

    subgraph Serving["4. Inferencia & Capa Gold"]
        INF["Batch Ingestion / Inferencia FastAPI"]
        GOLD["Capa Gold (Parquet & JSON Resultados)"]
        REG --> INF
        INF --> GOLD
    end

    subgraph Monitoring["5. Observabilidad & Drift"]
        DRIFT["Evidently AI / KS-Test (Detección de Drift)"]
        GOLD --> DRIFT
        DRIFT -->|Drift Detectado| TSS
    end
```

---

## 5. Implementación de Referencia: Entrenamiento con MLflow y Explicabilidad SHAP (Python)

```python
"""
Pipeline de Entrenamiento ML, Explicabilidad SHAP y Registro en MLflow
Normas: CRISP-DM / TDSP / ISO 25010
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import mean_squared_error, r2_score, roc_auc_score
import shap
import mlflow
import mlflow.sklearn

OUTPUTS_DIR = Path("data/gold/resultados_modelos")
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def train_and_register_yield_pipeline(df: pd.DataFrame):
    """
    Entrena el modelo de rendimiento y probabilidad de exportación,
    calcula explicabilidad SHAP y registra el artefacto en MLflow.
    """
    mlflow.set_experiment("AgroData_Yield_and_Quality_Optimization")
    
    feature_cols = [
        'calibre_promedio', 'grados_brix', 'ph_suelo', 
        'humedad_relativa', 'precipitacion_mm', 'temperatura_celsius'
    ]
    X = df[feature_cols]
    y_yield = df['rendimiento_kg_ha']
    y_export = df['es_premium_export']

    with mlflow.start_run(run_name="Run_LightGBM_Yield_and_Quality"):
        # 1. Regresión de Rendimiento
        regressor = GradientBoostingRegressor(
            n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42
        )
        regressor.fit(X, y_yield)
        y_pred = regressor.predict(X)
        
        rmse = float(np.sqrt(mean_squared_error(y_yield, y_pred)))
        r2 = float(r2_score(y_yield, y_pred))
        
        mlflow.log_param("regressor_algorithm", "GradientBoostingRegressor")
        mlflow.log_metric("yield_rmse", rmse)
        mlflow.log_metric("yield_r2", r2)

        # 2. Clasificación de Calidad Exportable Calibrada
        base_rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        calibrated_clf = CalibratedClassifierCV(estimator=base_rf, method='sigmoid', cv=3)
        calibrated_clf.fit(X, y_export)
        y_prob = calibrated_clf.predict_proba(X)[:, 1]
        
        auc = float(roc_auc_score(y_export, y_prob))
        mlflow.log_metric("export_quality_auc", auc)

        # 3. Explicabilidad Algorítmica con SHAP
        explainer = shap.TreeExplainer(regressor)
        shap_values = explainer.shap_values(X)
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        shap_importance = dict(zip(feature_cols, [float(v) for v in mean_abs_shap]))
        mlflow.log_dict(shap_importance, "shap_feature_importance.json")

        # 4. Registro y Guardado de Artefactos
        mlflow.sklearn.log_model(
            sk_model=regressor, 
            artifact_path="yield_model",
            registered_model_name="AgroYield_GradientBoosting"
        )
        mlflow.sklearn.log_model(
            sk_model=calibrated_clf, 
            artifact_path="quality_model",
            registered_model_name="AgroQuality_CalibratedRF"
        )

        # 5. Persistencia en Capa Gold
        df_gold = df.copy()
        df_gold['rendimiento_proyectado_kg_ha'] = np.round(y_pred, 1)
        df_gold['prob_calidad_export'] = np.round(y_prob, 3)
        gold_path = OUTPUTS_DIR / "predicciones_calidad_lotes.parquet"
        df_gold.to_parquet(gold_path, index=False)
        print(f"[OK] Modelo registrado en MLflow y predicciones Gold en: {gold_path}")

if __name__ == "__main__":
    # Simulación rápida para validar pipeline
    np.random.seed(42)
    n = 200
    mock_df = pd.DataFrame({
        'calibre_promedio': np.random.uniform(35, 60, n),
        'grados_brix': np.random.uniform(8, 17, n),
        'ph_suelo': np.random.uniform(5.0, 7.5, n),
        'humedad_relativa': np.random.uniform(60, 90, n),
        'precipitacion_mm': np.random.uniform(5, 60, n),
        'temperatura_celsius': np.random.uniform(15, 26, n),
    })
    mock_df['rendimiento_kg_ha'] = 10000 + mock_df['calibre_promedio'] * 40 + mock_df['grados_brix'] * 60 + np.random.normal(0, 200, n)
    mock_df['es_premium_export'] = ((mock_df['grados_brix'] > 12.5) & (mock_df['calibre_promedio'] > 44)).astype(int)
    # train_and_register_yield_pipeline(mock_df)
```

---

## 6. Definition of Done (DoD) para la Fase de Machine Learning

- [ ] Modelos de regresión, clasificación y forecasting entrenados con validación cruzada temporal.
- [ ] Métrica $R^2 > 0.85$ en regresión y $\text{ROC-AUC} > 0.80$ en clasificación de exportabilidad.
- [ ] Explicabilidad algorítmica SHAP calculada y serializada para su consumo en la UI.
- [ ] Modelos registrados formalmente en MLflow Model Registry con firmas de contrato.
- [ ] Resultados de inferencia guardados en capa Gold (`data/gold/resultados_modelos/`).
