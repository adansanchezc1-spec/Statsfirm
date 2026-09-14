"""Integration Tests for Agrostat Hexagonal Pipeline Use Cases.

Validates end-to-end interactions across Application Use Cases, Domain Services,
and Driven Adapters (Repository, DLQ, Model Registry, Telemetry) in an isolated filesystem.

Normative: SWEBOK Chapter 5 (Software Testing) / ISO/IEC 25010 (Reliability & Functional Suitability).
"""

from pathlib import Path
import tempfile
import unittest

from agrostat_app.container import Container
from tests.conftest import get_sample_dataset, get_sample_valid_batch


class TestPipelineUseCasesIntegration(unittest.TestCase):
    """Integration test suite executing application use cases through Container composition root."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_data_dir = Path(self.temp_dir.name)
        self.container = Container(custom_data_dir=self.test_data_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_ingestion_separates_silver_and_dlq(self) -> None:
        """Ingestion use case should persist valid batches to Silver and invalid records to DLQ."""
        valid_records = get_sample_dataset(count=5)
        invalid_record_1 = get_sample_valid_batch(batch_id="BAD-001", brix=99.0)  # Violates brix range
        invalid_record_2 = get_sample_valid_batch(batch_id="BAD-002", kilos_totales=500.0, kilos_exportables=800.0)

        mixed_stream = valid_records + [invalid_record_1, invalid_record_2]

        summary = self.container.ingestion_use_case.execute_ingestion(
            raw_records=mixed_stream,
            source_tag="IntegrationTestHarvester",
        )

        self.assertEqual(summary["total_received"], 7)
        self.assertEqual(summary["valid_count"], 5)
        self.assertEqual(summary["quarantined_count"], 2)
        self.assertFalse(summary["is_production_ready"])

        # Verify silver persistence
        stored_batches = self.container.repository.get_silver_batches()
        self.assertEqual(len(stored_batches), 5)

        # Verify DLQ persistence
        quarantined_records = self.container.dlq.get_quarantined_records()
        self.assertEqual(len(quarantined_records), 2)
        quarantined_ids = [q["payload"]["batch_id"] for q in quarantined_records]
        self.assertIn("BAD-001", quarantined_ids)
        self.assertIn("BAD-002", quarantined_ids)

    def test_train_yield_model_persists_to_registry(self) -> None:
        """Training use case should fit model on Silver data, register artifact, and compute metrics."""
        records = get_sample_dataset(count=20)
        self.container.ingestion_use_case.execute_ingestion(
            raw_records=records, source_tag="FieldSensors"
        )

        train_summary = self.container.training_use_case.train_and_register(
            model_algorithm="random_forest",
            test_size=0.25,
        )

        self.assertIsNotNone(train_summary["version"])
        self.assertGreater(train_summary["sample_counts"]["total"], 0)
        self.assertIn("r2_score", train_summary["evaluation_metrics"])
        self.assertIn("rmse", train_summary["evaluation_metrics"])
        self.assertTrue(train_summary["is_registered"])

        # Verify model artifact is discoverable in the registry
        active_models = self.container.registry.list_models()
        self.assertGreater(len(active_models), 0)

    def test_predict_yield_using_registered_model(self) -> None:
        """Prediction use case should return estimated yield with 95% confidence intervals."""
        # 1. Ingest and Train
        records = get_sample_dataset(count=20)
        self.container.ingestion_use_case.execute_ingestion(
            raw_records=records, source_tag="FieldSensors"
        )
        self.container.training_use_case.train_and_register(model_algorithm="random_forest")

        # 2. Predict on new sample
        sample_batch = get_sample_valid_batch(
            batch_id="PRED-TEST-001",
            kilos_totales=15000.0,
            brix=15.0,
            calibre=52.0,
        )
        prediction = self.container.prediction_use_case.predict_harvest_yield(sample_batch)

        self.assertEqual(prediction.lote_id, sample_batch["lote_id"])
        self.assertGreater(prediction.predicted_yield_kg_ha, 0.0)
        self.assertLessEqual(prediction.lower_bound_95, prediction.predicted_yield_kg_ha)
        self.assertGreaterEqual(prediction.upper_bound_95, prediction.predicted_yield_kg_ha)
        self.assertIsNotNone(prediction.model_version)

    def test_spc_analysis_on_curated_data(self) -> None:
        """SPC analysis use case should compute Shewhart limits and Nelson rules on curated silver data."""
        records = get_sample_dataset(count=15)
        self.container.ingestion_use_case.execute_ingestion(
            raw_records=records, source_tag="FieldSensors"
        )

        limits = self.container.spc_use_case.analyze_process_stability()

        self.assertEqual(limits.sample_count, 15)
        self.assertGreater(limits.ucl, limits.mean_center_line)
        self.assertLess(limits.lcl, limits.mean_center_line)
        self.assertIsInstance(limits.is_in_statistical_control, bool)

    def test_end_to_end_master_pipeline(self) -> None:
        """Master orchestrator should execute Ingestion -> Train -> Predict -> SPC in one run."""
        records = get_sample_dataset(count=22)
        sample = get_sample_valid_batch(batch_id="INFER-SAMPLE")
        summary = self.container.pipeline_use_case.run_pipeline(
            raw_dataset=records,
            source_tag="MasterIntegration",
            sample_batch_for_inference=sample,
        )

        self.assertEqual(summary.ingestion.total_received, 22)
        self.assertEqual(summary.ingestion.valid_count, 22)
        self.assertEqual(summary.ingestion.quarantined_count, 0)
        self.assertIsNotNone(summary.training)
        self.assertIsNotNone(summary.training.version)
        self.assertEqual(summary.predictions_generated, 1)
        self.assertGreater(summary.execution_duration_sec, 0.0)


if __name__ == "__main__":
    unittest.main()
