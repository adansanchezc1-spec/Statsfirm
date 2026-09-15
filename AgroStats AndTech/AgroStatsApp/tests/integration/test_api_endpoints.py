"""
Pruebas de Integración de Endpoints REST — FastAPI
OpenAPI 3.1 / RFC 7807 Error Handling
"""
import unittest
from fastapi.testclient import TestClient
from src.agrostats.adapters.driving.api.server import app

class TestFastAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertIn("DuckDB", data["engine"])

    def test_mercado_precios(self):
        response = self.client.get("/api/v1/mercado/precios?codigo_cpc=01211&mercado=CORABASTOS")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["data"]["producto"], "Aguacate Hass")
        self.assertIn("forecast_14d", data["data"])
        self.assertEqual(len(data["data"]["forecast_14d"]), 14)

    def test_guerra_simulation_endpoint(self):
        payload = {
            "codigo_cpc": "01211",
            "nombre_producto": "Aguacate Hass",
            "rendimiento_kg_ha": 12500.0,
            "precio_base_cop_kg": 7200.0,
            "costos_fijos_ha": 4500000.0,
            "costo_quimicos_ha": 13000000.0,
            "costos_otros_variables_ha": 16700000.0,
            "tasa_adopcion_bio_pct": 50.0
        }
        response = self.client.post("/api/v1/agroeconomia/guerra-simulation", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        res = data["resultado"]
        self.assertGreater(res["margen_bruto_bioinsumos_ha"], res["margen_bruto_convencional_ha"])
        self.assertGreater(res["ahorro_insumos_quimicos_ha"], 0)

    def test_cosecha_field_simulation(self):
        payload = {
            "grados_brix": 14.2,
            "calibre_mm": 48.0,
            "ph_suelo": 6.2,
            "precipitacion_semanal_mm": 35.0
        }
        response = self.client.post("/api/v1/cosecha/field-simulation", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("probabilidad_calidad_exportable", data)
        self.assertIn("rendimiento_proyectado_kg_ha", data)

    def test_bioinsumos_catalogo(self):
        response = self.client.get("/api/v1/bioinsumos/catalogo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIsInstance(data["catalog"], list)
        self.assertGreater(len(data["catalog"]), 0)

    def test_empresas_concentracion(self):
        response = self.client.get("/api/v1/empresas/concentracion")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("hhi_total", data)
        self.assertIsInstance(data["empresas"], list)

    def test_error_rfc7807_formato(self):
        # Enviar parámetro inválido que dispare DomainException
        payload = {
            "codigo_cpc": "01211",
            "nombre_producto": "Aguacate Hass",
            "rendimiento_kg_ha": -50.0, # Inválido!
            "precio_base_cop_kg": 7200.0,
            "costos_fijos_ha": 4500000.0,
            "costo_quimicos_ha": 13000000.0,
            "costos_otros_variables_ha": 16700000.0,
            "tasa_adopcion_bio_pct": 50.0
        }
        response = self.client.post("/api/v1/agroeconomia/guerra-simulation", json=payload)
        # Debe retornar 422 (pydantic gt=0) o 400 (RFC 7807)
        self.assertIn(response.status_code, [400, 422])

if __name__ == '__main__':
    unittest.main()
