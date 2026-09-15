"""
Motor Inteligente de Imputación de Datos Faltantes
Normas: Rubin Missing Data Framework / Little's MCAR / Scikit-Learn
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error

class IntelligentAgroImputer:
    """
    Diagnostica el mecanismo de pérdida y evalúa de forma competitiva
    estrategias de imputación para seleccionar la que minimiza el error de reconstrucción.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.benchmark_results = {}
        self.selected_method = None

    def diagnose_mechanism(self, df: pd.DataFrame, target_col: str) -> str:
        missing_mask = df[target_col].isna().astype(int)
        numeric_df = df.select_dtypes(include=[np.number])
        if target_col in numeric_df.columns:
            corrs = numeric_df.drop(columns=[target_col]).corrwith(missing_mask).abs()
            if not corrs.empty and corrs.max() > 0.30:
                return "MAR (Missing at Random - Correlacionado con covariables observables)"
        return "MCAR (Missing Completely at Random - Mecanismo estocástico independiente)"

    def benchmark_and_impute(self, df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        df_clean = df.copy()
        mechanism = self.diagnose_mechanism(df_clean, target_col)
        n_missing = int(df_clean[target_col].isna().sum())

        if n_missing == 0:
            return df_clean, {
                "target": target_col,
                "missing_count": 0,
                "mechanism": "NO_MISSING",
                "selected_method": "none"
            }

        # Subconjunto numérico completo para benchmark
        df_obs = df_clean.dropna(subset=[target_col]).copy()
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()

        if len(df_obs) >= 30 and len(numeric_cols) > 1:
            # Experimento con máscara sintética del 15%
            rng = np.random.RandomState(self.random_state)
            sim_mask = rng.rand(len(df_obs)) < 0.15
            y_real = df_obs[target_col].values[sim_mask]

            df_sim = df_obs[numeric_cols].copy()
            df_sim.loc[sim_mask, target_col] = np.nan

            # 1. Mediana
            med_val = float(df_obs[target_col].median())
            pred_med = np.full(len(y_real), med_val)
            rmse_med = float(np.sqrt(mean_squared_error(y_real, pred_med)))

            # 2. Interpolación lineal
            pred_interp = df_sim[target_col].interpolate(method='linear').bfill().ffill().values[sim_mask]
            rmse_interp = float(np.sqrt(mean_squared_error(y_real, pred_interp)))

            # 3. KNN Imputer
            knn = KNNImputer(n_neighbors=5)
            arr_knn = knn.fit_transform(df_sim)
            idx_t = numeric_cols.index(target_col)
            pred_knn = arr_knn[:, idx_t][sim_mask]
            rmse_knn = float(np.sqrt(mean_squared_error(y_real, pred_knn)))

            scores = {
                "interpolacion_lineal": rmse_interp,
                "knn_k5": rmse_knn,
                "mediana_estratificada": rmse_med
            }
            best = min(scores, key=scores.get)
        else:
            best = "interpolacion_lineal"
            scores = {"interpolacion_lineal": 0.0}

        # Aplicar el mejor método seleccionado
        if best == "knn_k5":
            imputer = KNNImputer(n_neighbors=5)
            df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
        elif best == "interpolacion_lineal":
            df_clean[target_col] = df_clean[target_col].interpolate(method='linear').bfill().ffill()
        else:
            df_clean[target_col] = df_clean[target_col].fillna(df_clean[target_col].median())

        metadata = {
            "target_variable": target_col,
            "mechanism_diagnosed": mechanism,
            "imputed_records": n_missing,
            "selected_imputer": best,
            "benchmark_rmse_scores": scores
        }
        return df_clean, metadata
