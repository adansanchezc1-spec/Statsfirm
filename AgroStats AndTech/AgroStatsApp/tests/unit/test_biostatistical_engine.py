"""
Pruebas Unitarias del Motor Bioestadístico (SPC) y 4 Reglas de Nelson
Normas: ISO 7870 / Control Estadístico de Procesos Shewhart
"""
import unittest
import numpy as np
from src.agrostats.domain.services.biostatistical_engine import BioStatisticalEngine
from src.agrostats.domain.exceptions import InsufficientDataForSPCException

class TestBiostatisticalEngine(unittest.TestCase):
    def test_datos_insuficientes_lanza_excepcion(self):
        few_points = [100.0, 102.0, 101.0]
        with self.assertRaises(InsufficientDataForSPCException):
            BioStatisticalEngine.evaluate_nelson_rules(few_points, min_samples=10)

    def test_proceso_estable_bajo_control(self):
        # 30 puntos oscilando con ruido gaussiano pequeño alrededor de 6000
        np.random.seed(42)
        normal_series = (6000.0 + np.random.normal(0, 50, 30)).tolist()

        res = BioStatisticalEngine.evaluate_nelson_rules(normal_series)
        self.assertEqual(res["status"], "NORMAL")
        self.assertFalse(res["rule_1_violated"])
        self.assertFalse(res["rule_2_violated"])
        self.assertFalse(res["rule_3_violated"])
        self.assertFalse(res["rule_4_violated"])
        self.assertGreater(res["ucl"], res["mean"])
        self.assertLess(res["lcl"], res["mean"])

    def test_violacion_regla_1_punto_fuera_de_tres_sigma(self):
        np.random.seed(42)
        series = (5000.0 + np.random.normal(0, 50, 25)).tolist()
        # Inyectar shock extremo > 3 sigma
        series.append(9000.0)

        res = BioStatisticalEngine.evaluate_nelson_rules(series)
        self.assertTrue(res["rule_1_violated"])
        self.assertEqual(res["status"], "DANGER")

    def test_violacion_regla_2_desplazamiento_de_nivel_9_puntos(self):
        # 10 puntos claramente por encima de la media
        series = [100.0] * 10 + [200.0] * 10
        res = BioStatisticalEngine.evaluate_nelson_rules(series)
        self.assertTrue(res["rule_2_violated"])
        self.assertIn(res["status"], ["WARNING", "DANGER"])

    def test_violacion_regla_3_tendencia_6_puntos_consecutivos(self):
        # 6 puntos estrictamente crecientes
        series = [100.0, 102.0, 101.0, 103.0, 102.0, 104.0, 106.0, 108.0, 110.0, 112.0, 114.0]
        res = BioStatisticalEngine.evaluate_nelson_rules(series)
        self.assertTrue(res["rule_3_violated"])

if __name__ == '__main__':
    unittest.main()
