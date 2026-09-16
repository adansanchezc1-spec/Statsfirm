"""Módulo de enlace y compatibilidad hacia atrás para AgroStats Platform.

Redirige cualquier importación de `agrostat_app` y sus submódulos hacia el paquete `agrostats`.
Implementa estándares PEP 562 (acceso dinámico a nivel módulo) y PEP 451 / PEP 302
(MetaPathFinder y Loader) para resolución unificada en tiempo de ejecución.

Normativas: Clean Code / SWEBOK Cap. 2 / SOLID / PEP 8 / ISO 25010.
"""

from importlib.abc import MetaPathFinder
from importlib.util import spec_from_loader
import importlib
from pathlib import Path
import sys
from typing import Any, List, Optional, Sequence

# 1. Asegurar que el directorio raíz de paquetes ('src') se encuentre en sys.path
_CURRENT_DIR = Path(__file__).resolve().parent
_SRC_DIR = _CURRENT_DIR.parent

if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

# 2. Cargar el paquete canónico ('agrostats')
agrostats = sys.modules.get("agrostats") or sys.modules.get("src.agrostats")

if agrostats is None:
    try:
        import agrostats
    except ImportError:
        try:
            agrostats = importlib.import_module("src.agrostats")
        except ImportError as exc:
            raise ImportError(
                f"No se pudo resolver el paquete canónico 'agrostats' desde '{_SRC_DIR}': {exc}"
            ) from exc

# 3. Propagar __path__ para que la maquinaria estándar de Python reconozca submódulos físicos
__path__: List[str] = list(getattr(agrostats, "__path__", []))
if str(_CURRENT_DIR) not in __path__:
    __path__.append(str(_CURRENT_DIR))

# 4. Exponer atributos públicos en el espacio de nombres de este módulo
for _attr in dir(agrostats):
    if not _attr.startswith("__"):
        globals()[_attr] = getattr(agrostats, _attr)

# 5. Loader y MetaPathFinder para interceptar y resolver `agrostat_app.*`
class _AgrostatAppAliasLoader:
    """Cargador de aliasing que asocia el módulo solicitado con el módulo canónico en agrostats."""

    def __init__(self, target_module_name: str) -> None:
        self.target_module_name = target_module_name

    def create_module(self, spec: Any) -> Any:
        module = sys.modules.get(self.target_module_name)
        if module is None:
            module = importlib.import_module(self.target_module_name)
        sys.modules[spec.name] = module
        return module

    def exec_module(self, module: Any) -> None:
        pass


class _AgrostatAppMetaPathFinder(MetaPathFinder):
    """Intercepta cualquier importación bajo el prefijo 'agrostat_app' y delega a 'agrostats'."""

    PREFIX = "agrostat_app"
    TARGET_PREFIX = "agrostats"

    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[str]],
        target: Optional[Any] = None,
    ) -> Optional[Any]:
        if fullname == self.PREFIX:
            loader = _AgrostatAppAliasLoader(self.TARGET_PREFIX)
            return spec_from_loader(
                fullname,
                loader,
                origin=getattr(agrostats, "__file__", None),
                is_package=True,
            )

        if fullname.startswith(self.PREFIX + "."):
            sub_path = fullname[len(self.PREFIX):]
            target_name = f"{self.TARGET_PREFIX}{sub_path}"
            try:
                target_mod = sys.modules.get(target_name)
                if target_mod is None:
                    target_mod = importlib.import_module(target_name)
            except ImportError:
                try:
                    # Intento alternativo en estructuras anidadas con 'src.'
                    target_mod = importlib.import_module(f"src.{self.TARGET_PREFIX}{sub_path}")
                except ImportError:
                    return None

            is_pkg = hasattr(target_mod, "__path__")
            loader = _AgrostatAppAliasLoader(target_name)
            spec = spec_from_loader(
                fullname,
                loader,
                origin=getattr(target_mod, "__file__", None),
                is_package=is_pkg,
            )
            if is_pkg and hasattr(target_mod, "__path__"):
                spec.submodule_search_locations = list(target_mod.__path__)
            return spec

        return None


# Registrar el interceptor de imports en sys.meta_path si no está activo
if not any(isinstance(finder, _AgrostatAppMetaPathFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, _AgrostatAppMetaPathFinder())


# 6. Soporte PEP 562 para acceso dinámico a atributos y módulos hijos
def __getattr__(name: str) -> Any:
    """Permite el acceso dinámico transparente a submódulos y atributos no precargados."""
    if hasattr(agrostats, name):
        return getattr(agrostats, name)
    try:
        submodule = importlib.import_module(f"agrostats.{name}")
        globals()[name] = submodule
        sys.modules[f"agrostat_app.{name}"] = submodule
        return submodule
    except ImportError:
        pass
    raise AttributeError(f"El módulo 'agrostat_app' no tiene el atributo o submódulo '{name}'")


def __dir__() -> List[str]:
    """Retorna los atributos disponibles combinando este módulo con agrostats."""
    attrs = set(globals().keys()) | set(dir(agrostats))
    return sorted(attrs)
