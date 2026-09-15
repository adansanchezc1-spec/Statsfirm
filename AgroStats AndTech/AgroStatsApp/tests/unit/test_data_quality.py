"""
Pruebas Unitarias del Validador de Calidad DAMA-DMBOK 2
6 Dimensiones: Completitud, Validez, Consistencia, Unicidad, Exactitud, Oportunidad
"""
import unittest
from src.agrostats.domain.services.data_quality_validator import DataQualityValidator

class TestDataQualityValidator(unittest.TestCase):
    def setUp(self):
        self.valid_record = {
            "fecha": "2025-06-15",
            "codigo_cpc": "01221",
            "central_abasto": "CORABASTOS",
            "precio_min": 6000.0,
            "precio_promedio": 6450.0,
            "precio_max": 6900.0
        }

    def test_record_completamente_valido(self):
        records = [self.valid_record]
        res = DataQualityValidator.evaluate_cotizacion_stream(records)

        self.assertEqual(res["total_evaluated"], 1)
        self.assertEqual(res["valid_count"], 1)
        self.assertEqual(res["quarantine_count"], 0)
        self.assertEqual(res["quality_rate_pct"], 100.0)
        self.assertTrue(res["is_production_ready"])

    def test_falla_completitud_campo_faltante(self):
        bad_rec = self.valid_record.copy()
        del bad_rec["precio_promedio"]
        res = DataQualityValidator.evaluate_cotizacion_stream([bad_rec])

        self.assertEqual(res["valid_count"], 0)
        self.assertEqual(res["quarantine_count"], 1)
        self.assertIn("Falla Completitud", res["quarantine_records"][0]["reasons"][0])

    def test_falla_validez_precios_negativos(self):
        bad_rec = self.valid_record.copy()
        bad_rec["precio_min"] = -500.0
        res = DataQualityValidator.evaluate_cotizacion_stream([bad_rec])

        self.assertEqual(res["quarantine_count"], 1)
        reasons_text = " ".join(res["quarantine_records"][0]["reasons"])
        self.assertIn("Falla Validez", reasons_text)

    def test_falla_consistencia_jerarquia_precios(self):
        # min > max
        bad_rec = self.valid_record.copy()
        bad_rec["precio_min"] = 8000.0
        bad_rec["precio_max"] = 5000.0
        bad_rec["precio_promedio"] = 6000.0
        res = DataQualityValidator.evaluate_cotizacion_stream([bad_rec])

        self.assertEqual(res["quarantine_count"], 1)
        reasons_text = " ".join(res["quarantine_records"][0]["reasons"])
        self.assertIn("Falla Consistencia", reasons_text)

    def test_falla_unicidad_duplicados(self):
        records = [self.valid_record, self.valid_record.copy()]
        res = DataQualityValidator.evaluate_cotizacion_stream(records)

        self.assertEqual(res["valid_count"], 1)
        self.assertEqual(res["quarantine_count"], 1)
        self.assertIn("Falla Unicidad", res["quarantine_records"][0]["reasons"][0])

if __name__ == '__main__':
    unittest.main()
