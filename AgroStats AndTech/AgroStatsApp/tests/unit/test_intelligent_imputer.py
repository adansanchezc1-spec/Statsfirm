"""
Pruebas Unitarias del Motor Inteligente de Imputación
Normas: Rubin Missing Data Framework / Benchmark Competitivo de RMSE
"""
import unittest
import numpy as np
import pandas as pd
from src.agrostats.domain.services.intelligent_imputer import IntelligentAgroImputer

class TestIntelligentAgroImputer(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)
        n = 60
        self.df = pd.DataFrame({
            "precio_min": np.linspace(4000, 6000, n) + np.random.normal(0, 50, n),
            "precio_max": np.linspace(5000, 7000, n) + np.random.normal(0, 50, n),
            "precio_promedio": np.linspace(4500, 6500, n) + np.random.normal(0, 50, n)
        })

    def test_imputacion_sin_faltantes(self):
        imputer = IntelligentAgroImputer(random_state=42)
        df_res, meta = imputer.benchmark_and_impute(self.df, "precio_promedio")

        self.assertEqual(meta["missing_count"], 0)
        self.assertEqual(meta["selected_method"], "none")
        self.assertEqual(df_res["precio_promedio"].isna().sum(), 0)

    def test_benchmark_competitivo_con_faltantes(self):
        df_corrupt = self.df.copy()
        # Introducir 10 nulos
        df_corrupt.loc[10:19, "precio_promedio"] = np.nan
        self.assertEqual(df_corrupt["precio_promedio"].isna().sum(), 10)

        imputer = IntelligentAgroImputer(random_state=42)
        df_clean, meta = imputer.benchmark_and_impute(df_corrupt, "precio_promedio")

        # Debe haber 0 nulos al terminar
        self.assertEqual(df_clean["precio_promedio"].isna().sum(), 0)
        self.assertEqual(meta["imputed_records"], 10)
        self.assertIn("benchmark_rmse_scores", meta)
        self.assertIn(meta["selected_imputer"], ["knn_k5", "interpolacion_lineal", "mediana_estratificada"])

if __name__ == '__main__':
    unittest.main()
