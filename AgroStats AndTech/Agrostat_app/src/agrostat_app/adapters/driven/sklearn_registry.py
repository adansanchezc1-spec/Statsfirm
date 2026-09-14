"""Driven Adapter: Scikit-Learn Model Registry.

Implements ModelRegistryPort.
Stores serialized model binaries (via pickle/joblib) alongside tracking metadata.
Normative: MLOps / SWEBOK Software Construction.
"""

from datetime import datetime
import json
from pathlib import Path
import pickle
from typing import Any, Dict, List, Optional, Tuple

from agrostat_app.domain.exceptions import ModelNotTrainedException
from agrostat_app.ports.out_registry_port import ModelRegistryPort


class SklearnModelRegistryAdapter(ModelRegistryPort):
    """Adapter managing serialized models and tracking metadata on disk."""

    def __init__(self, models_base_dir: Path) -> None:
        self._models_dir = Path(models_base_dir)
        self._models_dir.mkdir(parents=True, exist_ok=True)
        self._registry_index_file = self._models_dir / "registry_index.json"

    def save_model(
        self,
        model: Any,
        model_name: str,
        version: str,
        metrics: Dict[str, float],
        feature_names: List[str],
        parameters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Serializes and registers a trained model artifact."""
        model_folder = self._models_dir / model_name / version
        model_folder.mkdir(parents=True, exist_ok=True)

        model_file = model_folder / "model.pkl"
        metadata_file = model_folder / "metadata.json"

        # Serialización del artefacto
        with open(model_file, "wb") as f:
            pickle.dump(model, f)

        metadata = {
            "model_name": model_name,
            "version": version,
            "metrics": metrics,
            "feature_names": feature_names,
            "parameters": parameters or {},
            "registered_at": datetime.utcnow().isoformat(),
            "status": "ACTIVE",
        }

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Actualización del índice global de modelos activos
        index = self._read_index()
        index[model_name] = {
            "active_version": version,
            "path": str(model_file),
            "metadata_path": str(metadata_file),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._write_index(index)

        return str(model_folder)

    def load_model(
        self, model_name: str = "yield_forecast", version: Optional[str] = None
    ) -> Tuple[Any, Dict[str, Any]]:
        """Loads a model artifact and its metadata dictionary."""
        index = self._read_index()

        if model_name not in index:
            # Si no está en el índice, buscar si existe alguna versión en el disco
            matching_dirs = list(self._models_dir.glob(f"{model_name}/*"))
            if not matching_dirs:
                raise ModelNotTrainedException(
                    f"No existe ningún modelo registrado con el identificador '{model_name}'"
                )
            target_folder = sorted(matching_dirs)[-1]
        else:
            selected_version = version or index[model_name]["active_version"]
            target_folder = self._models_dir / model_name / selected_version

        model_file = target_folder / "model.pkl"
        metadata_file = target_folder / "metadata.json"

        if not model_file.exists():
            raise ModelNotTrainedException(f"Archivo de modelo no encontrado en: {model_file}")

        with open(model_file, "rb") as f:
            model = pickle.load(f)

        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return model, metadata

    def list_models(self) -> List[Dict[str, Any]]:
        """Returns all registered models and their active versions."""
        index = self._read_index()
        results = []
        for name, info in index.items():
            meta_path = Path(info["metadata_path"])
            meta = {}
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            results.append({
                "model_name": name,
                "active_version": info["active_version"],
                "metrics": meta.get("metrics", {}),
                "registered_at": meta.get("registered_at"),
            })
        return results

    def _read_index(self) -> Dict[str, Any]:
        if not self._registry_index_file.exists():
            return {}
        try:
            with open(self._registry_index_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_index(self, index: Dict[str, Any]) -> None:
        with open(self._registry_index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
