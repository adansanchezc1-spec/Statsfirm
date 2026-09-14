"""Agrostat Automated Test Runner.

Executes all unit and integration test suites using Python's standard unittest framework.
Generates an ISO/IEC 25010 compliance summary with execution metrics and exit code.

Usage:
    python tests/run_tests.py
    python -m unittest discover -s tests -p "test_*.py"

Normative: SWEBOK Chapter 5 (Software Testing) / ISO/IEC 25010 (Quality in Use).
"""

import os
import sys
import time
import unittest

# Ensure src/ is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def run_all_tests() -> bool:
    """Discovers and executes all test suites under the tests/ directory."""
    print("=" * 70)
    print(" [AGROSTAT TEST SUITE] - EXECUTING AUTOMATED QUALITY ASSURANCE")
    print(f" Standard: ISO/IEC 25010 & SWEBOK Chapter 5")
    print(f" Target Root: {PROJECT_ROOT}")
    print("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=os.path.dirname(__file__),
        pattern="test_*.py",
        top_level_dir=PROJECT_ROOT,
    )

    start_time = time.perf_counter()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    duration = time.perf_counter() - start_time

    print("\n" + "=" * 70)
    print(f" [RESULTADOS DE PRUEBAS]")
    print(f" - Pruebas Ejecutadas: {result.testsRun}")
    print(f" - Exitosas:           {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" - Fallos (Failures):  {len(result.failures)}")
    print(f" - Errores (Errors):   {len(result.errors)}")
    print(f" - Tiempo Total:       {duration:.3f} s")
    print("=" * 70)

    if result.wasSuccessful():
        print(" [ESTADO]: COBERTURA EXITOSA - 100% de aserciones aprobadas.")
        return True
    else:
        print(" [ESTADO]: FALLAS DETECTADAS - Revisar traceback superior.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
