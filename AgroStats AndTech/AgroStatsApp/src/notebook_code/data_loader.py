"""
Cargador Inteligente de Datasets Agropecuarios para Notebooks
Fase PDCO: DEVELOPMENT | Active Skill: 03-development
Estándares: DAMA-DMBOK 2, SWEBOK, PEP 8, Pandas I/O
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd

logger = logging.getLogger(__name__)


def find_raw_data_dir() -> Path:
    """
    Localiza de forma resiliente el directorio data/RAW buscando en jerarquías relativas
    desde la carpeta actual de ejecución, notebooks o src.
    """
    candidate_paths = [
        # Desde notebooks/ (CRISPDM/notebooks/ -> CRISPDM/data/RAW)
        Path.cwd().parent / "data" / "RAW",
        # Desde la raíz del proyecto AgroStatsApp/
        Path.cwd() / "CRISPDM" / "data" / "RAW",
        Path.cwd() / "data" / "RAW",
        # Relativo a este archivo fuente (src/notebook_code/ -> CRISPDM/data/RAW)
        Path(__file__).resolve().parent.parent.parent / "CRISPDM" / "data" / "RAW",
        Path(__file__).resolve().parent.parent.parent / "data" / "RAW",
    ]

    for p in candidate_paths:
        if p.exists() and p.is_dir():
            return p.resolve()

    # Si no existe, crear la ruta canónica en CRISPDM/data/RAW
    default_dir = Path(__file__).resolve().parent.parent.parent / "CRISPDM" / "data" / "RAW"
    default_dir.mkdir(parents=True, exist_ok=True)
    return default_dir.resolve()


class RawDataLoader:
    """
    Lector y estandarizador de conjuntos de datos crudos (CSV, JSON, XLSX)
    almacenados en data/RAW para su uso en notebooks de investigación.
    """

    def __init__(self, raw_dir: Optional[Union[str, Path]] = None) -> None:
        self.raw_dir = Path(raw_dir) if raw_dir else find_raw_data_dir()
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Carga el manifiesto de auditoría SHA-256 generado durante la ingesta."""
        manifest_file = self.raw_dir / "raw_manifest.json"
        if manifest_file.exists():
            try:
                with open(manifest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("No se pudo parsear raw_manifest.json: %s", e)
        return {}

    def list_available_datasets(self) -> List[str]:
        """Lista los IDs de datasets encontrados en data/RAW."""
        files = list(self.raw_dir.glob("*.*"))
        dataset_ids = set()
        for f in files:
            if f.name == "raw_manifest.json" or f.name.startswith("temp_") or f.suffix.lower() in [".md", ".txt", ".gitignore"]:
                continue
            # El nombre típicamente sigue el patrón {dataset_id}_{timestamp}.ext
            parts = f.stem.split("_")
            if len(parts) >= 2:
                # Tomar los tokens previos a la fecha numérica
                prefix = []
                for p in parts:
                    if p.isdigit() and len(p) >= 8:
                        break
                    prefix.append(p)
                if prefix:
                    dataset_ids.add("_".join(prefix))
            else:
                dataset_ids.add(f.stem)
        return sorted(list(dataset_ids))

    def _find_latest_file(self, dataset_id: str, preferred_exts: Tuple[str, ...] = (".csv", ".json", ".xlsx")) -> Optional[Path]:
        """Encuentra el archivo más reciente para un dataset_id dado según la extensión preferida."""
        for ext in preferred_exts:
            candidates = list(self.raw_dir.glob(f"{dataset_id}_*{ext}")) + list(self.raw_dir.glob(f"{dataset_id}{ext}"))
            if candidates:
                # Ordenar por fecha de modificación descendente
                candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return candidates[0]
        return None

    def load_dataset(self, dataset_id: str, clean_column_names: bool = True) -> pd.DataFrame:
        """
        Carga el dataset especificado en un DataFrame de pandas.
        Aplica autodetección de encabezados y conversión de tipos inicial.
        """
        filepath = self._find_latest_file(dataset_id)
        if not filepath:
            raise FileNotFoundError(
                f"No se encontró ningún archivo para el dataset '{dataset_id}' en {self.raw_dir}."
            )

        suffix = filepath.suffix.lower()
        logger.info("Cargando dataset [%s] desde %s", dataset_id, filepath.name)

        if suffix == ".csv":
            try:
                # Intentar lectura estándar con codificación UTF-8
                df = pd.read_csv(filepath, encoding="utf-8")
            except UnicodeDecodeError:
                # Fallback a latin-1 para compatibilidad DANE
                df = pd.read_csv(filepath, encoding="latin-1")
        elif suffix == ".json":
            df = pd.read_json(filepath)
        elif suffix in [".xlsx", ".xls"]:
            # Autodetección de filas de encabezado en formatos DANE
            df_raw = pd.read_excel(filepath, header=None)
            header_row = 0
            # Buscar la primera fila con suficiente número de strings no nulos
            for idx in range(min(15, len(df_raw))):
                row_vals = df_raw.iloc[idx].dropna()
                if len(row_vals) >= 3 and any(isinstance(v, str) and len(v) > 2 for v in row_vals):
                    header_row = idx
                    break
            df = pd.read_excel(filepath, header=header_row)
        else:
            raise ValueError(f"Formato no soportado: {suffix}")

        # Limpieza estándar de nombres de columnas
        if clean_column_names:
            df.columns = [
                str(c).strip().replace(" ", "_").replace(".", "_").replace("/", "_").lower()
                for c in df.columns
            ]

        # Inyectar atributo con metadatos de linaje
        df.attrs["dataset_id"] = dataset_id
        df.attrs["source_path"] = str(filepath)
        df.attrs["file_name"] = filepath.name

        return df

    def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Carga todos los conjuntos de datos presentes en data/RAW en un diccionario.
        """
        available = self.list_available_datasets()
        loaded: Dict[str, pd.DataFrame] = {}

        for ds_id in available:
            try:
                loaded[ds_id] = self.load_dataset(ds_id)
                logger.info("Dataset [%s] cargado con éxito: %d filas, %d columnas", ds_id, len(loaded[ds_id]), len(loaded[ds_id].columns))
            except Exception as e:
                logger.warning("No se pudo cargar el dataset %s: %s", ds_id, e)

        return loaded
