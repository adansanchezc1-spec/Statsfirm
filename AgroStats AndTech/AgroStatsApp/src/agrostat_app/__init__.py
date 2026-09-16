"""Módulo de enlace y compatibilidad hacia atrás.
Redirige cualquier importación de `agrostat_app` hacia `agrostats`.
"""

import sys
from src import agrostats

# Inyectar submódulos en sys.modules
sys.modules["agrostat_app"] = agrostats
for attr in dir(agrostats):
    if not attr.startswith("__"):
        globals()[attr] = getattr(agrostats, attr)
