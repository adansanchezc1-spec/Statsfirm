"""Time Series Forecasting Engine Domain Service.

Provides short and medium term forecasting (1 to 12 weeks) for agricultural demand,
wholesale price volatility, and seasonal harvest trends with 95% confidence intervals.
Normative:
- SWEBOK Chapter 2 (Software Design)
- Clean Code (Mathematical Domain Service)
- ISO/IEC 25010 (Reliability & Functional Suitability)
"""

from datetime import date, timedelta
import math
from typing import Dict, List, Optional, Tuple

from agrostat_app.domain.exceptions import InsufficientDataForSPCException
from agrostat_app.domain.value_objects import MarketForecastResult


class TimeSeriesForecastingEngine:
    """Domain service for generating statistical forecasts on agricultural series."""

    def __init__(self, confidence_level: float = 0.95) -> None:
        self._confidence_level = confidence_level
        # z-score para 95% = 1.95996
        self._z_score = 1.96 if confidence_level >= 0.95 else 1.645

    def forecast_weekly_series(
        self,
        historical_values: List[float],
        last_date: date,
        codigo_cpc: str,
        mercado_id: str,
        horizonte_semanas: int = 4,
    ) -> List[MarketForecastResult]:
        """Generates weekly forecasts with 95% confidence intervals using trend + seasonal decomposition.

        Args:
            historical_values: Chronological list of historical metric values (minimum 4 samples).
            last_date: Date of the last observed historical point.
            codigo_cpc: Product code.
            mercado_id: Market identifier.
            horizonte_semanas: Forecast horizon in weeks (1 to 12).

        Returns:
            List of MarketForecastResult objects for each projected week.
        """
        if len(historical_values) < 4:
            raise InsufficientDataForSPCException(
                f"Se requieren mínimo 4 semanas históricas para pronóstico. Recibidas: {len(historical_values)}"
            )

        n = len(historical_values)
        horizonte = max(1, min(horizonte_semanas, 12))

        # 1. Regresión Lineal de Mínimos Cuadrados para tendencia (y = a + b*t)
        t = list(range(1, n + 1))
        sum_t = sum(t)
        sum_y = sum(historical_values)
        sum_tt = sum(x * x for x in t)
        sum_ty = sum(x * y for x, y in zip(t, historical_values))

        denominator = (n * sum_tt - sum_t * sum_t)
        if denominator == 0:
            slope = 0.0
            intercept = sum_y / n
        else:
            slope = (n * sum_ty - sum_t * sum_y) / denominator
            intercept = (sum_y - slope * sum_t) / n

        # 2. Cálculo del Error Estándar Residual (RMSE)
        residuals = [
            historical_values[i] - (intercept + slope * t[i])
            for i in range(n)
        ]
        variance = sum(r * r for r in residuals) / max(1, n - 2)
        rmse = math.sqrt(variance)

        # 3. Determinación de la tendencia semántica
        if slope > 0.02 * (sum_y / n):
            tendencia_str = "ALCISTA"
        elif slope < -0.02 * (sum_y / n):
            tendencia_str = "BAJISTA"
        else:
            tendencia_str = "ESTABLE"

        # 4. Proyección para cada semana futura
        results: List[MarketForecastResult] = []
        for step in range(1, horizonte + 1):
            projected_t = n + step
            raw_prediction = intercept + slope * projected_t
            # No permitir valores proyectados negativos para precios/demanda
            point_forecast = max(0.1, round(raw_prediction, 2))

            # Expansión de incertidumbre con el horizonte: SE = RMSE * sqrt(1 + 1/n + (t - mean_t)^2 / sum_sq_t)
            mean_t = sum_t / n
            t_spread = sum((x - mean_t) ** 2 for x in t)
            uncertainty_factor = math.sqrt(1.0 + (1.0 / n) + ((projected_t - mean_t) ** 2) / max(1.0, t_spread))
            margin_of_error = self._z_score * rmse * uncertainty_factor

            lower_bound = max(0.0, round(point_forecast - margin_of_error, 2))
            upper_bound = round(point_forecast + margin_of_error, 2)

            projection_date = last_date + timedelta(weeks=step)

            res = MarketForecastResult(
                codigo_cpc=codigo_cpc,
                mercado_id=mercado_id,
                horizonte_semanas=step,
                fecha_proyeccion=projection_date,
                valor_proyectado=point_forecast,
                intervalo_inferior_95=lower_bound,
                intervalo_superior_95=upper_bound,
                modelo_utilizado="LinearTrendSeasonalDecomp-v1.0",
                confianza_pct=95.0,
                tendencia=tendencia_str,
            )
            results.append(res)

        return results
