"""
Pruebas Unitarias del Motor Bioeconómico de Guillermo Guerra (IICA)
Manual de Administración de Empresas Agropecuarias
"""
import unittest
from src.agrostats.domain.entities import CultivoRentabilidad
from src.agrostats.domain.value_objects import PorcentajeAdopcion
from src.agrostats.domain.services.guerra_agroeconomics_engine import GuillermoGuerraEngine

class TestGuillermoGuerraEngine(unittest.TestCase):
    def setUp(self):
        self.cultivo = CultivoRentabilidad(
            codigo_cpc="01221",
            nombre_producto="Aguacate Hass",
            rendimiento_kg_ha=10500.0,
            precio_base_cop_kg=6450.0,
            costos_fijos_ha=5200000.0,
            costos_variables_quimicos_ha=15500000.0,
            costos_variables_otros_ha=23825000.0,
            tasa_ahorro_max_bio_pct=0.248,  # 24.8% max ahorro en insumos
            prima_verde_max_pct=0.125       # 12.5% max sobreprecio exportación
        )

    def test_evaluacion_cero_adopcion(self):
        adopcion = PorcentajeAdopcion(0.0)
        res = GuillermoGuerraEngine.calcular_rentabilidad(self.cultivo, adopcion)

        self.assertEqual(res["ahorro_insumos_quimicos_ha"], 0.0)
        self.assertEqual(res["precio_efectivo_cop_kg"], 6450.0)
        self.assertEqual(res["margen_bruto_convencional_ha"], res["margen_bruto_bioinsumos_ha"])
        self.assertEqual(res["ganancia_neta_adicional_ha"], 0.0)

    def test_evaluacion_cuarenta_y_cinco_adopcion(self):
        adopcion = PorcentajeAdopcion(45.0)
        res = GuillermoGuerraEngine.calcular_rentabilidad(self.cultivo, adopcion)

        # Debe generar ahorro químico estricto > 0
        self.assertGreater(res["ahorro_insumos_quimicos_ha"], 0.0)
        # El precio efectivo debe ser mayor al base por la prima verde
        self.assertGreater(res["precio_efectivo_cop_kg"], 6450.0)
        # El margen bruto con bioinsumos debe superar al convencional
        self.assertGreater(res["margen_bruto_bioinsumos_ha"], res["margen_bruto_convencional_ha"])
        # Ganancia neta adicional positiva
        self.assertGreater(res["ganancia_neta_adicional_ha"], 1000000.0)
        # El Punto de Equilibrio Físico y Monetario debe reducirse con bioinsumos
        self.assertLess(res["bep_precio_bioinsumos_cop_kg"], res["bep_precio_convencional_cop_kg"])
        self.assertLess(res["bep_kilos_bioinsumos_ha"], res["bep_kilos_convencional_ha"])
        # ROI con bioinsumos debe ser superior
        self.assertGreater(res["roi_operativo_bioinsumos_pct"], res["roi_operativo_convencional_pct"])

    def test_evaluacion_cien_adopcion_organica(self):
        adopcion = PorcentajeAdopcion(100.0)
        res = GuillermoGuerraEngine.calcular_rentabilidad(self.cultivo, adopcion)

        expected_ahorro = 15500000.0 * 0.248
        self.assertAlmostEqual(res["ahorro_insumos_quimicos_ha"], expected_ahorro, places=1)
        expected_precio = 6450.0 * (1 + 0.125)
        self.assertAlmostEqual(res["precio_efectivo_cop_kg"], expected_precio, places=1)

if __name__ == '__main__':
    unittest.main()
