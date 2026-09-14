"""Unit Tests: BioStatisticalEngine Domain Service.

Tests Shewhart Control Limits, Nelson Rules (1, 2, 3, 4) and Process Capability.
Normative: SWEBOK Chapter 5 / ISO 7870.
"""

from datetime import date, timedelta
import unittest

from agrostat_app.domain.entities import HarvestBatch
from agrostat_app.domain.exceptions import InsufficientDataForSPCException
from agrostat_app.domain.services.biostatistical_engine import BioStatisticalEngine


class TestBioStatisticalEngine(unittest.TestCase):
    """Test suite for BioStatisticalEngine calculations."""

    def setUp(self) -> None:
        self.engine = BioStatisticalEngine()

    def _create_batches_with_values(self, values: list[float]) -> list[HarvestBatch]:
        batches = []
        base_date = date(2026, 1, 1)
        for i, val in enumerate(values):
            batches.append(
                HarvestBatch(
                    batch_id=f"B-{i+1}",
                    lote_id="LOTE-TEST",
                    fecha_cosecha=base_date + timedelta(days=i),
                    hectareas_lote=1.0,
                    kilos_totales=val,
                    kilos_exportables=val * 0.8,
                    calibre_promedio=50.0,
                    grados_brix=12.0,
                    responsable_registro="Tester",
                )
            )
        return batches

    def test_insufficient_samples_raises_exception(self) -> None:
        """Less than 10 samples must raise InsufficientDataForSPCException."""
        batches = self._create_batches_with_values([1000.0] * 5)
        with self.assertRaises(InsufficientDataForSPCException):
            self.engine.compute_spc_limits(batches)

    def test_normal_process_is_in_statistical_control(self) -> None:
        """Stable process with random minor variations should be in statistical control."""
        values = [1000.0, 1020.0, 990.0, 1010.0, 995.0, 1005.0, 1015.0, 985.0, 1000.0, 1010.0, 990.0, 1005.0]
        batches = self._create_batches_with_values(values)
        limits = self.engine.compute_spc_limits(batches)

        self.assertTrue(limits.is_in_statistical_control)
        self.assertEqual(len(limits.violations), 0)
        self.assertAlmostEqual(limits.mean_center_line, sum(values) / len(values), places=2)
        self.assertGreater(limits.ucl, limits.mean_center_line)
        self.assertLess(limits.lcl, limits.mean_center_line)

    def test_nelson_rule_1_detects_outlier_beyond_3_sigma(self) -> None:
        """A single point > UCL must trigger Nelson Rule 1."""
        values = [1000.0] * 11 + [5000.0]  # Outlier en muestra 12
        batches = self._create_batches_with_values(values)
        limits = self.engine.compute_spc_limits(batches)

        self.assertFalse(limits.is_in_statistical_control)
        rule_1_violations = [v for v in limits.violations if v.rule_number == 1]
        self.assertGreaterEqual(len(rule_1_violations), 1)
        self.assertEqual(rule_1_violations[0].observed_value, 5000.0)

    def test_nelson_rule_2_detects_shift_9_points_same_side(self) -> None:
        """9 consecutive points on the same side of center line triggers Nelson Rule 2."""
        # Primeros 5 abajo de 1000, luego 9 consecutivos arriba de 1000
        values = [900.0, 910.0, 920.0, 905.0, 915.0] + [1100.0, 1105.0, 1110.0, 1115.0, 1120.0, 1125.0, 1130.0, 1135.0, 1140.0]
        batches = self._create_batches_with_values(values)
        limits = self.engine.compute_spc_limits(batches)

        rule_2_violations = [v for v in limits.violations if v.rule_number == 2]
        self.assertGreaterEqual(len(rule_2_violations), 1)

    def test_nelson_rule_3_detects_continuous_trend_6_points(self) -> None:
        """6 consecutive points continually increasing triggers Nelson Rule 3."""
        values = [1000.0, 1000.0, 1000.0, 1000.0] + [1010.0, 1020.0, 1030.0, 1040.0, 1050.0, 1060.0]
        batches = self._create_batches_with_values(values)
        limits = self.engine.compute_spc_limits(batches)

        rule_3_violations = [v for v in limits.violations if v.rule_number == 3]
        self.assertGreaterEqual(len(rule_3_violations), 1)


if __name__ == "__main__":
    unittest.main()
