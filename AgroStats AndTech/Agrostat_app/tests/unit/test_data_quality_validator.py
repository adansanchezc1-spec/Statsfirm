"""Unit Tests: DataQualityValidator Domain Service.

Tests DAMA-BOK quality dimensions: Completeness, Validity, Consistency, and Uniqueness.
Normative: SWEBOK Chapter 5 (Software Testing) / Clean Code Unit Testing.
"""

import unittest

from agrostat_app.domain.services.data_quality_validator import DataQualityValidator
from tests.conftest import get_sample_valid_batch


class TestDataQualityValidator(unittest.TestCase):
    """Test suite for Data Quality Validator domain service."""

    def setUp(self) -> None:
        self.validator = DataQualityValidator()

    def test_valid_record_passes_contract(self) -> None:
        """Valid record should produce 1 valid batch and 0 quarantined."""
        record = get_sample_valid_batch()
        batches, quarantined, report = self.validator.validate_batch_stream([record])

        self.assertEqual(len(batches), 1)
        self.assertEqual(len(quarantined), 0)
        self.assertEqual(report.total_records, 1)
        self.assertEqual(report.valid_records, 1)
        self.assertEqual(report.completeness_rate, 1.0)
        self.assertTrue(report.is_production_ready)

    def test_missing_required_field_is_quarantined(self) -> None:
        """Record missing required field should be quarantined (Completeness dimension)."""
        record = get_sample_valid_batch()
        del record["grados_brix"]

        batches, quarantined, report = self.validator.validate_batch_stream([record])

        self.assertEqual(len(batches), 0)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Completitud violada", quarantined[0]["errors"][0])
        self.assertEqual(report.completeness_rate, 0.0)

    def test_out_of_range_brix_is_quarantined(self) -> None:
        """Record with out of range brix (> 32) should fail Validity dimension."""
        record = get_sample_valid_batch(brix=48.0)

        batches, quarantined, report = self.validator.validate_batch_stream([record])

        self.assertEqual(len(batches), 0)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("grados_brix", quarantined[0]["errors"][0])

    def test_inconsistent_exportable_kilos_is_quarantined(self) -> None:
        """Record where exportable kilos > total kilos should fail Consistency dimension."""
        record = get_sample_valid_batch(kilos_totales=5000.0, kilos_exportables=6000.0)

        batches, quarantined, report = self.validator.validate_batch_stream([record])

        self.assertEqual(len(batches), 0)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Consistencia violada", quarantined[0]["errors"][0])

    def test_duplicate_batch_id_is_quarantined(self) -> None:
        """Duplicate batch_id in the same stream should fail Uniqueness dimension."""
        r1 = get_sample_valid_batch(batch_id="DUPLICATE-001")
        r2 = get_sample_valid_batch(batch_id="DUPLICATE-001")

        batches, quarantined, report = self.validator.validate_batch_stream([r1, r2])

        self.assertEqual(len(batches), 1)
        self.assertEqual(len(quarantined), 1)
        self.assertIn("Unicidad violada", quarantined[0]["errors"][0])


if __name__ == "__main__":
    unittest.main()
