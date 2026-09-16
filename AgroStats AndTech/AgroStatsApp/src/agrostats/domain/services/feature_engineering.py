"""Feature Engineering Domain Service.

Pure mathematical domain transformations for preparing agronomic tabular data
for Machine Learning without framework dependencies.
Normative:
- Clean Code (SRP, Pure Functions)
- Feature Engineering for Tabular Data
"""

import math
from typing import Any, Dict, List, Tuple

from agrostat_app.domain.entities import HarvestBatch


class FeatureEngineeringService:
    """Domain service for generating ML features from agronomic entities."""

    FEATURE_NAMES = [
        "calibre_promedio",
        "grados_brix",
        "ratio_brix_calibre",
        "tasa_exportabilidad",
        "ph_suelo",
        "humedad_relativa",
        "precipitacion_mm",
        "temperatura_celsius",
        "mes_cosecha_sin",
        "mes_cosecha_cos",
    ]

    DEFAULT_IMPUTATIONS = {
        "ph_suelo": 6.5,
        "humedad_relativa": 72.0,
        "precipitacion_mm": 18.0,
        "temperatura_celsius": 21.5,
    }

    def extract_features(
        self, batches: List[HarvestBatch]
    ) -> Tuple[List[List[float]], List[float], List[str]]:
        """Transforms harvest entities into numeric matrix X and target vector y.

        Returns:
            Tuple of:
            - X: List of feature vectors (each vector aligns with FEATURE_NAMES).
            - y: List of target values (rendimiento_kg_ha).
            - feature_names: List of strings.
        """
        X: List[List[float]] = []
        y: List[float] = []

        for b in batches:
            # 1. Cyclical date features
            month = b.fecha_cosecha.month
            mes_sin = math.sin(2.0 * math.pi * month / 12.0)
            mes_cos = math.cos(2.0 * math.pi * month / 12.0)

            # 2. Imputations
            ph = b.ph_suelo if b.ph_suelo is not None else self.DEFAULT_IMPUTATIONS["ph_suelo"]
            hum = b.humedad_relativa if b.humedad_relativa is not None else self.DEFAULT_IMPUTATIONS["humedad_relativa"]
            prec = b.precipitacion_mm if b.precipitacion_mm is not None else self.DEFAULT_IMPUTATIONS["precipitacion_mm"]
            temp = b.temperatura_celsius if b.temperatura_celsius is not None else self.DEFAULT_IMPUTATIONS["temperatura_celsius"]

            vector = [
                float(b.calibre_promedio),
                float(b.grados_brix),
                float(b.ratio_brix_calibre),
                float(b.tasa_exportabilidad),
                float(ph),
                float(hum),
                float(prec),
                float(temp),
                round(mes_sin, 6),
                round(mes_cos, 6),
            ]

            X.append(vector)
            y.append(float(b.rendimiento_kg_ha))

        return X, y, list(self.FEATURE_NAMES)

    def extract_single_instance(self, batch: HarvestBatch) -> List[float]:
        """Extracts feature vector for a single batch entity for live inference."""
        X, _, _ = self.extract_features([batch])
        return X[0]
