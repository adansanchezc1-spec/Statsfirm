"""Use Case: Train, Evaluate, and Register Yield AI Model.

Implements ModelTrainingPipelinePort.
Applies Feature Engineering, trains regression model, tracks metrics, and registers artifacts.
Normative: SWEBOK Chapter 2 / MLOps Pipeline Best Practices.
"""

from datetime import datetime
import math
from typing import Any, Dict, Optional

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from agrostat_app.application.dtos import TrainingSummaryDTO
from agrostat_app.domain.exceptions import InsufficientDataForSPCException
from agrostat_app.domain.services.feature_engineering import FeatureEngineeringService
from agrostat_app.ports.in_training_port import ModelTrainingPipelinePort
from agrostat_app.ports.out_notification_port import NotificationPort
from agrostat_app.ports.out_registry_port import ModelRegistryPort
from agrostat_app.ports.out_repository_port import HarvestRepositoryPort


class TrainYieldModelUseCase(ModelTrainingPipelinePort):
    """Use Case coordinating the ML training pipeline on curated Silver layer data."""

    MIN_TRAINING_SAMPLES = 12

    def __init__(
        self,
        repository: HarvestRepositoryPort,
        feature_service: FeatureEngineeringService,
        registry: ModelRegistryPort,
        notifier: NotificationPort,
    ) -> None:
        self._repository = repository
        self._feature_service = feature_service
        self._registry = registry
        self._notifier = notifier

    def train_and_register(
        self,
        lote_id: Optional[str] = None,
        test_size: float = 0.25,
        model_algorithm: str = "random_forest",
    ) -> Dict[str, Any]:
        """Runs the model training pipeline."""
        self._notifier.send_alert(
            level="INFO",
            title="Iniciando Pipeline de Entrenamiento ML",
            message=f"Algoritmo: {model_algorithm} | Lote: {lote_id or 'Consolidado Global'}",
        )

        # 1. Recuperación de Entidades Curadas de la Capa Silver
        batches = self._repository.get_silver_batches(lote_id)
        if len(batches) < self.MIN_TRAINING_SAMPLES:
            msg = (
                f"Datos insuficientes en Capa Silver para entrenar el modelo. "
                f"Requeridos: {self.MIN_TRAINING_SAMPLES}, Disponibles: {len(batches)}"
            )
            self._notifier.send_alert("WARNING", "Entrenamiento Cancelado", msg)
            raise InsufficientDataForSPCException(msg)

        # 2. Extracción de Features Agronómicas y Target Vector
        X_matrix, y_vector, feature_names = self._feature_service.extract_features(batches)
        X = np.array(X_matrix)
        y = np.array(y_vector)

        # 3. Particionamiento Train / Test Estratificado por Tiempo / Aleatorio con Semilla Fija
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # 4. Instanciación y Ajuste del Modelo Seleccionado
        if model_algorithm == "gradient_boosting":
            model = GradientBoostingRegressor(
                n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42
            )
        else:
            model = RandomForestRegressor(
                n_estimators=120, max_depth=6, min_samples_split=3, random_state=42
            )

        model.fit(X_train, y_train)

        # 5. Evaluación Exhaustiva en Conjunto de Prueba
        y_pred = model.predict(X_test)
        r2 = float(r2_score(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(math.sqrt(mse))
        mae = float(mean_absolute_error(y_test, y_pred))

        # Cálculo de MAPE evitando división por cero
        non_zero_mask = y_test > 0
        if np.any(non_zero_mask):
            mape = float(np.mean(np.abs((y_test[non_zero_mask] - y_pred[non_zero_mask]) / y_test[non_zero_mask])) * 100.0)
        else:
            mape = 0.0

        # 6. Feature Importances
        importances = {}
        if hasattr(model, "feature_importances_"):
            for feat, imp in zip(feature_names, model.feature_importances_):
                importances[feat] = round(float(imp), 4)

        metrics = {
            "r2_score": r2,
            "rmse": rmse,
            "mae": mae,
            "mape": mape,
        }

        # 7. Versionado y Registro de Modelo
        version = f"v{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        model_name = f"yield_forecast_{lote_id}" if lote_id else "yield_forecast_global"

        registry_path = self._registry.save_model(
            model=model,
            model_name=model_name,
            version=version,
            metrics=metrics,
            feature_names=feature_names,
            parameters={
                "algorithm": model_algorithm,
                "n_samples_train": len(X_train),
                "n_samples_test": len(X_test),
            },
        )

        # 8. Persistencia de Features en Capa Gold (Feature Store / Data Mart)
        gold_features = []
        for i, b in enumerate(batches):
            row = b.to_dict()
            row["feature_vector"] = X_matrix[i]
            gold_features.append(row)

        self._repository.save_gold_features(gold_features, "yield_training_features")

        summary = TrainingSummaryDTO(
            model_name=model_name,
            version=version,
            algorithm=model_algorithm,
            total_samples=len(batches),
            train_samples=len(X_train),
            test_samples=len(X_test),
            r2_score=r2,
            rmse=rmse,
            mae=mae,
            mape=mape,
            is_registered=True,
            registry_path=registry_path,
            feature_importances=importances,
        )

        self._notifier.send_alert(
            level="INFO",
            title="Modelo Registrado Exitosamente",
            message=f"Modelo {model_name}:{version} | R2: {r2:.3f} | RMSE: {rmse:.1f} kg/ha",
            metadata=summary.to_dict(),
        )

        return summary.to_dict()
