"""Unit Tests: FeatureEngineeringService Domain Service.

Tests feature extraction, cyclical date transformations, and imputations.
Normative: SWEBOK Chapter 5 / Feature Engineering Verification.
"""

from datetime import date
import unittest

from agrostat_app.domain.entities import HarvestBatch
from agrostat_app.domain.services.feature_engineering import FeatureEngineeringService


class TestFeatureEngineeringService(unittest.TestCase):
    """Test suite for feature engineering transformations."""

    def setUp(self) -> None:
        self.service = FeatureEngineeringService()

    def test_feature_extraction_dimensions_match(self) -> None:
        """Matrix X rows must match batch count, and columns must match FEATURE_NAMES length."""
        batches = [
            HarvestBatch(
                batch_id=f"B-{i}",
                lote_id="LOTE-01",
                fecha_cosecha=date(2026, 6, 15),
                hectareas_lote=10.0,
                kilos_totales=15000.0,
                kilos_exportables=13000.0,
                calibre_promedio=52.0,
                grados_brix=14.0,
                responsable_registro="Auditor",
            )
            for i in range(5)
        ]

        X, y, feature_names = self.service.extract_features(batches)

        self.assertEqual(len(X), 5)
        self.assertEqual(len(y), 5)
        self.assertEqual(len(feature_names), len(self.service.FEATURE_NAMES))
        self.assertEqual(len(X[0]), len(self.service.FEATURE_NAMES))
        self.assertEqual(y[0], 1500.0)  # 15000 / 10 = 1500 kg/ha

    def test_none_values_are_imputed_with_domain_defaults(self) -> None:
        """Entities with null environmental parameters should receive domain defaults."""
        batch = HarvestBatch(
            batch_id="B-NULL",
            lote_id="LOTE-02",
            fecha_cosecha=date(2026, 3, 1),
            hectareas_lote=5.0,
            kilos_totales=8000.0,
            kilos_exportables=7000.0,
            calibre_promedio=40.0,
            grados_brix=11.0,
            responsable_registro="Auditor",
            ph_suelo=None,
            humedad_relativa=None,
        )

        vector = self.service.extract_single_instance(batch)
        ph_index = self.service.FEATURE_NAMES.index("ph_suelo")
        hum_index = self.service.FEATURE_NAMES.index("humedad_relativa")

        self.assertEqual(vector[ph_index], self.service.DEFAULT_IMPUTATIONS["ph_suelo"])
        self.assertEqual(vector[hum_index], self.service.DEFAULT_IMPUTATIONS["humedad_relativa"])


if __name__ == "__main__":
    unittest.main()
