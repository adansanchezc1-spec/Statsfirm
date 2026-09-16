# Documentación de Interfaces y APIs de la Plataforma
**Plataforma**: Agrostat Data Intelligence Platform  
**Fase PDCO**: **DEVELOPMENT**  
**Active Skill**: `03-development`  
**Estándares**: SWEBOK Cap. 3, OpenAPI / CLI Style Guides  

---

## 1. Comandos de la Interfaz de Línea de Comandos (CLI)

El ejecutable principal es invocable mediante el módulo `agrostat_app.adapters.driving.cli`:

```bash
python -m agrostat_app.adapters.driving.cli <comando> [opciones]
```

### 1.1. Ingesta Nacional de Mercados y Clima (`ingest-market`)
Ejecuta la extracción de DANE SIPSA (Precios y Abastecimiento) y de IDEAM (Meteorología), aplica la curaduría DAMA-BOK, desvía registros anómalos a la DLQ, persiste la capa Silver en Parquet y actualiza las tablas de hechos de DuckDB Gold.

```bash
python -m agrostat_app.adapters.driving.cli ingest-market --date 2026-09-14 --limit 100
```
- `--date`: Fecha en formato ISO `YYYY-MM-DD` (por defecto: fecha actual).
- `--limit`: Cantidad máxima de registros a extraer por fuente (por defecto: 100).

### 1.2. Pronóstico Bioestadístico de Mercado (`forecast-market`)
Calcula proyecciones semanales de precios mayoristas y demanda agrícola con bandas de confianza del 95% y análisis de tendencia.

```bash
python -m agrostat_app.adapters.driving.cli forecast-market --cpc 01211 --mercado CORABASTOS --weeks 4
```
- `--cpc`: Código CPC del producto (ej. `01211` para Papa Pastusa, `01222` para Tomate Chonto).
- `--mercado`: Identificador de la central mayorista (ej. `CORABASTOS`, `CAVASA`, `CMA_MEDELLIN`).
- `--weeks`: Horizonte predictivo en semanas (1 a 12, por defecto: 4).

### 1.3. Control Estadístico de Procesos Shewhart (`spc-market`)
Audita la estabilidad estocástica de los precios de mercado calculando la línea central ($\bar{X}$), límites de control ($UCL/LCL = \bar{X} \pm 3\sigma$) y evalúa las Reglas de Nelson (1 a 4).

```bash
python -m agrostat_app.adapters.driving.cli spc-market --cpc 01211 --mercado CORABASTOS
```

### 1.4. Consulta Analítica Directa a DuckDB (`query-dw`)
Ejecuta cualquier consulta analítica en sintaxis ANSI SQL directamente sobre el archivo local de DuckDB (`data/gold/agro_dw.duckdb`).

```bash
python -m agrostat_app.adapters.driving.cli query-dw --sql "SELECT producto_cpc_codigo, ROUND(AVG(precio_medio_kg), 2) as precio_prom FROM fact_precios_sipsa GROUP BY producto_cpc_codigo"
```

### 1.5. Balance de Oferta y Demanda (`balance-market`)
Consulta la vista analítica materializada `vw_balance_mercado_diario` para monitorear volúmenes de ingreso frente a precios promedio.

```bash
python -m agrostat_app.adapters.driving.cli balance-market --mercado CORABASTOS --cpc 01211
```

---

## 2. Contratos de Datos y Schemas JSON

### 2.1. Payload de Auditoría en Dead Letter Queue (DLQ)
Formato de cada registro escrito en `data/dlq/quarantine_records.jsonl`:

```json
{
  "quarantined_at": "2026-09-14T22:15:52.123456",
  "payload": {
    "record_index": 12,
    "dataset": "SIPSA_P",
    "raw_payload": {
      "id_cotizacion": "sipsa_20260914_CORABASTOS_01211_12",
      "fecha": "2026-09-14",
      "mercado_id": "CORABASTOS",
      "codigo_cpc": "01211",
      "precio_min_kg": 4500.0,
      "precio_prom_kg": 3200.0,
      "precio_max_kg": 3000.0
    },
    "errors": [
      "Consistencia: Violación de jerarquía de precios (4500.0 <= 3200.0 <= 3000.0 es falso)"
    ]
  }
}
```

### 2.2. Esquema de Salida de Pronóstico (`MarketForecastResult`)
```json
{
  "codigo_cpc": "01211",
  "mercado_id": "CORABASTOS",
  "horizonte_semanas": 1,
  "fecha_proyeccion": "2026-09-21",
  "valor_proyectado": 3167.57,
  "intervalo_95": {
    "inferior": 3007.97,
    "superior": 3327.17
  },
  "modelo_utilizado": "LinearTrendSeasonalDecomp-v1.0",
  "confianza_pct": 95.0,
  "tendencia": "ESTABLE",
  "generated_at": "2026-09-14T22:16:04.123456"
}
```
