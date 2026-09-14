"""Application Configuration.

Resolves base directories, storage paths, and environment settings.
Normative: 12-Factor App / SWEBOK Chapter 2.
"""

import os
from pathlib import Path


class Config:
    """Central configuration class for Agrostat Data Science Application."""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = Path(os.environ.get("AGROSTAT_DATA_DIR", BASE_DIR / "data"))

    BRONZE_DIR = DATA_DIR / "bronze"
    SILVER_DIR = DATA_DIR / "silver"
    GOLD_DIR = DATA_DIR / "gold"
    DLQ_DIR = DATA_DIR / "dlq"
    MODELS_DIR = DATA_DIR / "models"

    SQL_DIR = BASE_DIR / "sql"
    SQL_SCHEMA_FILE = SQL_DIR / "schema_agro_dw.sql"
    SQL_SEEDS_FILE = SQL_DIR / "seeds_mercados_y_productos.sql"
    DUCKDB_FILE = GOLD_DIR / "agro_dw.duckdb"

    LOG_LEVEL = os.environ.get("AGROSTAT_LOG_LEVEL", "INFO")
    DEFAULT_ALGORITHM = os.environ.get("AGROSTAT_MODEL_ALGO", "random_forest")

    # API Tokens
    SOCRATA_APP_TOKEN = os.environ.get("SOCRATA_APP_TOKEN")

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensures all physical Lakehouse directories exist."""
        for path in [
            cls.DATA_DIR,
            cls.BRONZE_DIR,
            cls.SILVER_DIR,
            cls.GOLD_DIR,
            cls.DLQ_DIR,
            cls.MODELS_DIR,
        ]:
            path.mkdir(parents=True, exist_ok=True)
