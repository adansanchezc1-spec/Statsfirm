# Reporte de Calidad de Datos: `ica_inventario_pecuario`
**Estándar**: ISO/IEC 25010 & DAMA-DMBOK 2 | **Fecha**: 2026-10-02T08:26:49.983737  
**Estado General**: ⚠️ WARNING | **Score Global**: `90.0%`  
**Volumen**: 11 filas × 7 columnas

---
## 1. Desempeño por Dimensión de Calidad (DAMA-DMBOK 2)

| Dimensión | Puntuación | Estado |
|---|:---:|:---:|
| **Completeness** | 100.0% | ✅ Óptimo |
| **Uniqueness** | 100.0% | ✅ Óptimo |
| **Validity** | 50.0% | ❌ Crítico |
| **Consistency** | 100.0% | ✅ Óptimo |
| **Timeliness** | 100.0% | ✅ Óptimo |
| **Accuracy** | 100.0% | ✅ Óptimo |

---
## 2. Detalle de Pruebas de Calidad (Quality Checks)

| Regla / Chequeo | Dimensión | Columna | Severidad | Métrica | Umbral | Resultado |
|---|---|---|:---:|:---:|:---:|:---:|
| null_rate_codigo_divipola | Completeness | `codigo_divipola` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_departamento | Completeness | `departamento` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_municipio | Completeness | `municipio` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_especie | Completeness | `especie` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_categoria | Completeness | `categoria` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_anio | Completeness | `anio` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_inventario | Completeness | `inventario` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| row_deduplication_check | Uniqueness | `Global` | MEDIUM | 0.000 | 0.010 | ✅ PASS |
| primary_key_uniqueness | Uniqueness | `codigo_divipola+especie+anio` | CRITICAL | 0.000 | 0.000 | ✅ PASS |
| range_check_inventario | Validity | `inventario` | HIGH | 0.000 | 0.010 | ✅ PASS |
| regex_divipola_codigo_divipola | Validity | `codigo_divipola` | HIGH | 1.000 | 0.050 | ⚠️ WARN |
| timeliness_bounds_anio | Timeliness | `anio` | MEDIUM | 0.000 | 0.010 | ✅ PASS |
| extreme_outliers_iqr_inventario | Accuracy | `inventario` | LOW | 0.000 | 0.050 | ✅ PASS |