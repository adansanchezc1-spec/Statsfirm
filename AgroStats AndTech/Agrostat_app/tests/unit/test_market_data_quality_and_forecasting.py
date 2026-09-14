"""Unit Tests for Market Data Quality Validation and Time Series Forecasting.

Normative:
- SWEBOK Chapter 5 (Software Testing)
- ISO/IEC 25010 (Functional Suitability & Reliability)
- IEEE 830 / ISO 29148 Requerimientos RF-006 a RF-010, RF-014, RF-015
"""

from datetime import date, timedelta
import unittest

from agrostat_app.domain.entities import CotizacionMayorista, ObservacionClimatica
from agrostat_app.domain.exceptions import InsufficientDataForSPCException, InvariantViolationException
from agrostat_app.domain.services.data_quality_validator import DataQualityValidator
from agrostat_app.domain.services.forecasting_engine import TimeSeriesForecastingEngine
from agrostat_app.domain.value_objects import CpcProductCode, DivipolaCode


class TestMarketDataQualityValidator(unittest.TestCase):
    """Test suite verifying DAMA-BOK quality rules on market datasets."""

    def setUp(self) -> None:
        self.validator = DataQualityValidator()
        self.today = date(2026, 9, 14)

    def test_valid_cotizacion_stream_passes_all_dama_dimensions(self) -> None:
        """Valid price records should pass completeness, validity, consistency, and uniqueness."""
        raw_stream = [
            {
                "id_cotizacion": "cot_001",
                "fecha": "2026-09-14",
                "mercado_id": "CORABASTOS",
                "codigo_cpc": "01211",
                "nombre_producto": "Papa Pastusa",
                "grupo_cpc": "Tubérculos",
                "variedad": "Pastusa Primera",
                "codigo_mpio_origen": "25843",
                "nombre_mpio_origen": "Villapinzón",
                "precio_min_kg": 2500.0,
                "precio_prom_kg": 2800.0,
                "precio_max_kg": 3100.0,
                "volumen_transado_kg": 12500.0,
            },
            {
                "id_cotizacion": "cot_002",
                "fecha": "2026-09-14",
                "mercado_id": "CORABASTOS",
                "codigo_cpc": "01222",
                "nombre_producto": "Tomate Chonto",
                "grupo_cpc": "Hortalizas",
                "variedad": "Chonto Maduro",
                "codigo_mpio_origen": "15759",
                "nombre_mpio_origen": "Sogamoso",
                "precio_min_kg": 3000.0,
                "precio_prom_kg": 3400.0,
                "precio_max_kg": 3800.0,
                "volumen_transado_kg": 8500.0,
            },
        ]

        valid_items, quarantined, report = self.validator.validate_cotizaciones_stream(raw_stream)

        self.assertEqual(len(valid_items), 2)
        self.assertEqual(len(quarantined), 0)
        self.assertEqual(report.completeness_rate, 1.0)
        self.assertEqual(report.validity_rate, 1.0)
        self.assertEqual(report.consistency_rate, 1.0)
        self.assertTrue(report.is_production_ready)

    def test_inconsistent_price_hierarchy_routes_to_dlq(self) -> None:
        """Records where precio_min > precio_max must be quarantined."""
        raw_stream = [
            {
                "id_cotizacion": "cot_bad_01",
                "fecha": "2026-09-14",
                "mercado_id": "CAVASA",
                "codigo_cpc": "01211",
                "precio_min_kg": 4500.0,  # Min mayor que Max
                "precio_prom_kg": 3000.0,
                "precio_max_kg": 2800.0,
                "volumen_transado_kg": 5000.0,
            }
        ]

        valid_items, quarantined, report = self.validator.validate_cotizaciones_stream(raw_stream)

        self.assertEqual(len(valid_items), 0)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Consistencia: Violación de jerarquía de precios", quarantined[0]["errors"][0])
        self.assertEqual(report.valid_records, 0)
        self.assertEqual(report.quarantined_records, 1)

    def test_duplicate_natural_key_is_quarantined(self) -> None:
        """Duplicate records with same date, market, product, and variety must be quarantined."""
        raw_stream = [
            {
                "id_cotizacion": "cot_dup_1",
                "fecha": "2026-09-14",
                "mercado_id": "CORABASTOS",
                "codigo_cpc": "01211",
                "variedad": "Pastusa",
                "precio_min_kg": 2000.0,
                "precio_prom_kg": 2200.0,
                "precio_max_kg": 2500.0,
            },
            {
                "id_cotizacion": "cot_dup_2",
                "fecha": "2026-09-14",
                "mercado_id": "CORABASTOS",
                "codigo_cpc": "01211",
                "variedad": "Pastusa",
                "precio_min_kg": 2100.0,
                "precio_prom_kg": 2300.0,
                "precio_max_kg": 2600.0,
            },
        ]

        valid_items, quarantined, report = self.validator.validate_cotizaciones_stream(raw_stream)

        self.assertEqual(len(valid_items), 1)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Unicidad: Registro duplicado", quarantined[0]["errors"][0])

    def test_clima_stream_validates_thermal_consistency(self) -> None:
        """Climate observation with temp_min > temp_max must be quarantined."""
        raw_stream = [
            {
                "id_observacion": "obs_thermal_error",
                "estacion_id": "EST-999",
                "fecha": "2026-09-14",
                "codigo_mpio": "25843",
                "precipitacion_mm": 15.4,
                "temp_max_celsius": 12.0,
                "temp_min_celsius": 18.5,  # Min mayor que Max
                "temp_media_celsius": 15.0,
                "humedad_relativa_pct": 75.0,
            }
        ]

        valid_items, quarantined, report = self.validator.validate_clima_stream(raw_stream)

        self.assertEqual(len(valid_items), 0)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Consistencia térmica: T_min (18.5) > T_max (12.0)", quarantined[0]["errors"][0])


class TestTimeSeriesForecastingEngine(unittest.TestCase):
    """Test suite verifying statistical forecasting engine."""

    def setUp(self) -> None:
        self.forecaster = TimeSeriesForecastingEngine(confidence_level=0.95)
        self.base_date = date(2026, 9, 14)

    def test_forecast_generates_weekly_projections_with_confidence_bands(self) -> None:
        """Forecaster should generate 4 weekly points with expanding 95% confidence intervals."""
        historical_prices = [2500.0, 2550.0, 2620.0, 2680.0, 2750.0, 2810.0, 2900.0, 2980.0]

        results = self.forecaster.forecast_weekly_series(
            historical_values=historical_prices,
            last_date=self.base_date,
            codigo_cpc="01211",
            mercado_id="CORABASTOS",
            horizonte_semanas=4,
        )

        self.assertEqual(len(results), 4)
        for i, res in enumerate(results, start=1):
            self.assertEqual(res.horizonte_semanas, i)
            self.assertEqual(res.fecha_proyeccion, self.base_date + timedelta(weeks=i))
            self.assertGreater(res.valor_proyectado, 0)
            self.assertLessEqual(res.intervalo_inferior_95, res.valor_proyectado)
            self.assertGreaterEqual(res.intervalo_superior_95, res.valor_proyectado)
            self.assertEqual(res.tendencia, "ALCISTA")

    def test_insufficient_samples_raises_domain_exception(self) -> None:
        """Less than 4 historical points must raise InsufficientDataForSPCException."""
        with self.assertRaises(InsufficientDataForSPCException):
            self.forecaster.forecast_weekly_series(
                historical_values=[2500.0, 2600.0],
                last_date=self.base_date,
                codigo_cpc="01211",
                mercado_id="CORABASTOS",
                horizonte_semanas=2,
            )


if __name__ == "__main__":
    unittest.main()
