# Reporte de Calidad de Datos: `ideam_telemetria_realtime`
**Estándar**: ISO/IEC 25010 & DAMA-DMBOK 2 | **Fecha**: 2026-10-02T08:26:44.742026  
**Estado General**: ❌ FAILED | **Score Global**: `78.7%`  
**Volumen**: 1,000 filas × 14 columnas

---
## 1. Desempeño por Dimensión de Calidad (DAMA-DMBOK 2)

| Dimensión | Puntuación | Estado |
|---|:---:|:---:|
| **Completeness** | 99.9% | ✅ Óptimo |
| **Uniqueness** | 53.1% | ❌ Crítico |
| **Validity** | 50.0% | ❌ Crítico |
| **Consistency** | 100.0% | ✅ Óptimo |
| **Timeliness** | 100.0% | ✅ Óptimo |
| **Accuracy** | 81.3% | ⚠️ Aceptable |

---
## 2. Detalle de Pruebas de Calidad (Quality Checks)

| Regla / Chequeo | Dimensión | Columna | Severidad | Métrica | Umbral | Resultado |
|---|---|---|:---:|:---:|:---:|:---:|
| null_rate_codigoestacion | Completeness | `codigoestacion` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_codigosensor | Completeness | `codigosensor` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_fechaobservacion | Completeness | `fechaobservacion` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_valorobservado | Completeness | `valorobservado` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_nombreestacion | Completeness | `nombreestacion` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_departamento | Completeness | `departamento` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_municipio | Completeness | `municipio` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_zonahidrografica | Completeness | `zonahidrografica` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_latitud | Completeness | `latitud` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_longitud | Completeness | `longitud` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_descripcionsensor | Completeness | `descripcionsensor` | MEDIUM | 0.006 | 0.400 | ✅ PASS |
| null_rate_unidadmedida | Completeness | `unidadmedida` | MEDIUM | 0.006 | 0.400 | ✅ PASS |
| null_rate_entidad | Completeness | `entidad` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| null_rate_codigo_divipola | Completeness | `codigo_divipola` | MEDIUM | 0.000 | 0.400 | ✅ PASS |
| row_deduplication_check | Uniqueness | `Global` | MEDIUM | 0.000 | 0.010 | ✅ PASS |
| primary_key_uniqueness | Uniqueness | `codigoestacion+fechaobservacion` | CRITICAL | 0.469 | 0.000 | ❌ FAIL |
| range_check_valorobservado | Validity | `valorobservado` | HIGH | 0.000 | 0.010 | ✅ PASS |
| regex_divipola_codigo_divipola | Validity | `codigo_divipola` | HIGH | 1.000 | 0.050 | ⚠️ WARN |
| colombia_geobounds_consistency | Consistency | `latitud,longitud` | MEDIUM | 0.000 | 0.100 | ✅ PASS |
| timeliness_bounds_fechaobservacion | Timeliness | `fechaobservacion` | MEDIUM | 0.000 | 0.010 | ✅ PASS |
| extreme_outliers_iqr_codigoestacion | Accuracy | `codigoestacion` | LOW | 0.000 | 0.050 | ✅ PASS |
| extreme_outliers_iqr_codigosensor | Accuracy | `codigosensor` | LOW | 0.246 | 0.050 | ⚠️ WARN |
| extreme_outliers_iqr_valorobservado | Accuracy | `valorobservado` | LOW | 0.054 | 0.050 | ⚠️ WARN |
| extreme_outliers_iqr_latitud | Accuracy | `latitud` | LOW | 0.305 | 0.050 | ⚠️ WARN |
| extreme_outliers_iqr_longitud | Accuracy | `longitud` | LOW | 0.332 | 0.050 | ⚠️ WARN |