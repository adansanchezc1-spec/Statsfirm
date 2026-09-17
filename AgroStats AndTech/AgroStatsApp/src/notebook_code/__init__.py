"""
Paquete de Utilidades y Exploración para Notebooks CRISP-DM
==========================================================
Permite cargar de forma transparente los datasets desde data/RAW,
realizar un perfilamiento informático multidimensional (nulos, duplicados,
granularidad y tipos de datos) y ejecutar el motor de imputación inteligente.

Exporta:
- `RawDataLoader`: Lector inteligente de archivos crudos CSV/JSON/XLSX.
- `DatasetProfiler`: Motor de análisis informático y diagnóstico de calidad.
- `NotebookImputerBridge`: Puente para ejecutar el torneo de imputación en notebooks.
- Funciones de acceso rápido: `load_raw_dataset`, `load_all_raw_datasets`, `explore_dataset`.
"""

import pandas as pd
from typing import Any, Dict

from .data_loader import RawDataLoader, find_raw_data_dir
from .data_profiler import DatasetProfiler
from .imputer_helper import NotebookImputerBridge


def load_raw_dataset(dataset_id: str, clean_column_names: bool = True) -> pd.DataFrame:
    """Función de una sola línea para cargar un dataset de data/RAW por su ID."""
    loader = RawDataLoader()
    return loader.load_dataset(dataset_id, clean_column_names=clean_column_names)


def load_all_raw_datasets() -> Dict[str, pd.DataFrame]:
    """Carga todos los datasets disponibles en data/RAW en un diccionario."""
    loader = RawDataLoader()
    return loader.load_all_datasets()


def explore_dataset(df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
    """Genera el diagnóstico informático completo para un DataFrame."""
    return DatasetProfiler.inspect(df, dataset_name=dataset_name)


__all__ = [
    "RawDataLoader",
    "DatasetProfiler",
    "NotebookImputerBridge",
    "find_raw_data_dir",
    "load_raw_dataset",
    "load_all_raw_datasets",
    "explore_dataset",
]