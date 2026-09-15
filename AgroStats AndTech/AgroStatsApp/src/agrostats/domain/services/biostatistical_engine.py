"""
Motor Bioestadístico de Control de Procesos (SPC)
Normas: ISO 7870 / Cartas Shewhart / 4 Reglas de Nelson
"""
from typing import List, Dict, Any
import numpy as np
from src.agrostats.domain.exceptions import InsufficientDataForSPCException

class BioStatisticalEngine:
    @staticmethod
    def evaluate_nelson_rules(data_points: List[float], min_samples: int = 10) -> Dict[str, Any]:
        if len(data_points) < min_samples:
            raise InsufficientDataForSPCException(len(data_points), min_samples)

        series = np.array(data_points, dtype=float)
        mean = float(np.mean(series))
        sigma = float(np.std(series, ddof=1))
        if sigma == 0:
            sigma = 1e-6

        # Límites de Control Shewhart (±3 sigma)
        ucl = mean + 3.0 * sigma
        lcl = max(0.0, mean - 3.0 * sigma)

        # Regla 1: Un punto fuera de límites ±3 sigma
        rule_1_violated = bool(np.any((series > ucl) | (series < lcl)))

        # Regla 2: 9 puntos consecutivos en el mismo lado de la media
        rule_2_violated = False
        above_count = 0
        below_count = 0
        for val in series:
            if val > mean:
                above_count += 1
                below_count = 0
            elif val < mean:
                below_count += 1
                above_count = 0
            else:
                above_count = 0
                below_count = 0
            if above_count >= 9 or below_count >= 9:
                rule_2_violated = True
                break

        # Regla 3: 6 puntos consecutivos en tendencia creciente o decreciente
        rule_3_violated = False
        if len(series) >= 6:
            diffs = np.diff(series)
            inc_count = 0
            dec_count = 0
            for d in diffs:
                if d > 0:
                    inc_count += 1
                    dec_count = 0
                elif d < 0:
                    dec_count += 1
                    inc_count = 0
                else:
                    inc_count = 0
                    dec_count = 0
                if inc_count >= 5 or dec_count >= 5: # 5 diferencias = 6 puntos
                    rule_3_violated = True
                    break

        # Regla 4: 14 puntos alternando arriba y abajo (oscilación rápida)
        rule_4_violated = False
        if len(series) >= 14:
            diffs = np.diff(series)
            alternations = 0
            for i in range(1, len(diffs)):
                if (diffs[i] > 0 and diffs[i-1] < 0) or (diffs[i] < 0 and diffs[i-1] > 0):
                    alternations += 1
                    if alternations >= 13: # 13 alternancias = 14 puntos
                        rule_4_violated = True
                        break
                else:
                    alternations = 0

        # Determinación de Estado
        if rule_1_violated:
            status = "DANGER"
            title = "SHOCK DE OFERTA O PRECIO DETECTADO"
            desc = "El punto supera los límites ±3σ Shewhart. Alerta logística o especulativa crítica."
        elif rule_2_violated or rule_3_violated or rule_4_violated:
            status = "WARNING"
            title = "Inestabilidad Detectada por Reglas de Nelson"
            desc = "Se detectan tendencias sistemáticas o desplazamientos de media en las cotizaciones."
        else:
            status = "NORMAL"
            title = "Mercado Estable y Confiable"
            desc = "El proceso oscila bajo causas comunes aleatorias. Ventana óptima para emisión de contratos."

        return {
            "mean": round(mean, 2),
            "sigma": round(sigma, 2),
            "ucl": round(ucl, 2),
            "lcl": round(lcl, 2),
            "rule_1_violated": rule_1_violated,
            "rule_2_violated": rule_2_violated,
            "rule_3_violated": rule_3_violated,
            "rule_4_violated": rule_4_violated,
            "status": status,
            "title": title,
            "desc": desc,
            "normative": "ISO 7870 Statistical Process Control"
        }
