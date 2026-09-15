"""
Master Test Runner — AgroData Intelligence Platform Enterprise v1.0
Ejecuta todas las pruebas unitarias y de integración de la plataforma
"""
import os
import sys
import unittest
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Asegurar que el directorio raíz de la aplicación esté en el PYTHONPATH
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)

def run_all_tests():
    print("=" * 80)
    print("🌱 AGRODATA INTELLIGENCE PLATFORM — ENTERPRISE TEST SUITE v1.0")
    print("=" * 80)
    print(f"Directorio de Aplicación: {APP_ROOT}")
    print(f"Python Version: {sys.version.split()[0]}")
    print("-" * 80)

    loader = unittest.TestLoader()
    start_dir = os.path.join(APP_ROOT, "tests")

    suite = loader.discover(start_dir=start_dir, pattern="test_*.py", top_level_dir=APP_ROOT)

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    duration = time.time() - start_time

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors

    print("-" * 80)
    print("📊 RESUMEN EJECUTIVO DE CONTROL DE CALIDAD:")
    print(f"  • Total Pruebas Ejecutadas: {total_tests}")
    print(f"  • Pruebas Exitosas:         {passed} ({'100.0%' if total_tests > 0 and failures == 0 and errors == 0 else f'{(passed/total_tests)*100:.1f}%'})")
    print(f"  • Fallos (Failures):         {failures}")
    print(f"  • Errores Técnicos (Errors): {errors}")
    print(f"  • Tiempo Total de Ejecución: {duration:.3f} s")
    print("=" * 80)

    if failures == 0 and errors == 0:
        print("✅ CONFORMIDAD 100%: Todos los modelos y motores bioeconómicos pasaron las aserciones.")
        return 0
    else:
        print("❌ NO CONFORME: Se detectaron fallos o errores en la suite de pruebas.")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
