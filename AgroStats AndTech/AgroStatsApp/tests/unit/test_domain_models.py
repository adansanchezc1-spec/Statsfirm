"""
Pruebas Unitarias de Objetos de Valor y Entidades de Dominio
Clean Architecture / Principios DDD / Validación de Invariantes
"""
import unittest
from src.agrostats.domain.value_objects import (
    DineroCOP, RendimientoKgHa, PorcentajeAdopcion, CodigoCpc, CodigoDivipola
)
from src.agrostats.domain.entities import CultivoRentabilidad
from src.agrostats.domain.exceptions import DomainException

class TestDomainValueObjects(unittest.TestCase):
    def test_dinero_cop_valid(self):
        dinero = DineroCOP(15000.0)
        self.assertEqual(dinero.valor, 15000.0)
        self.assertIn("$15.000", dinero.formatear_pesos())

    def test_dinero_cop_negative_raises(self):
        with self.assertRaises(ValueError):
            DineroCOP(-100.0)

    def test_rendimiento_kg_ha(self):
        rend = RendimientoKgHa(12500.0)
        self.assertEqual(rend.kilos_por_hectarea, 12500.0)

    def test_rendimiento_negative_raises(self):
        with self.assertRaises(ValueError):
            RendimientoKgHa(-50.0)

    def test_porcentaje_adopcion_bounds(self):
        adop = PorcentajeAdopcion(45.0)
        self.assertEqual(adop.porcentaje, 45.0)
        self.assertAlmostEqual(adop.factor, 0.45)

        with self.assertRaises(ValueError):
            PorcentajeAdopcion(105.0)

        with self.assertRaises(ValueError):
            PorcentajeAdopcion(-5.0)

    def test_codigo_cpc_validation(self):
        cpc = CodigoCpc("01221")
        self.assertEqual(cpc.codigo, "01221")

        with self.assertRaises(ValueError):
            CodigoCpc("1") # < 3 caracteres

    def test_codigo_divipola_validation(self):
        divipola = CodigoDivipola("05756")
        self.assertEqual(divipola.codigo_dane, "05756")

        with self.assertRaises(ValueError):
            CodigoDivipola("123")  # != 5 dígitos

class TestCultivoRentabilidadEntity(unittest.TestCase):
    def test_cultivo_rentabilidad_properties(self):
        cultivo = CultivoRentabilidad(
            codigo_cpc="01221",
            nombre_producto="Aguacate Hass",
            rendimiento_kg_ha=10500.0,
            precio_base_cop_kg=6450.0,
            costos_fijos_ha=5200000.0,
            costos_variables_quimicos_ha=15500000.0,
            costos_variables_otros_ha=23825000.0,
            tasa_ahorro_max_bio_pct=0.248,
            prima_verde_max_pct=0.125
        )
        self.assertEqual(cultivo.costos_variables_totales_convencional, 15500000.0 + 23825000.0)
        self.assertGreater(cultivo.costos_fijos_ha, 0)

if __name__ == '__main__':
    unittest.main()
