"""Biostatistical Engine Domain Service.

Pure mathematical domain service implementing:
- Shewhart Statistical Process Control (SPC) Limits (Center Line, UCL, LCL, Zones A/B/C)
- Nelson Rules 1 through 4 for special cause anomaly detection
- Process Capability Indices (Cp, Cpk)
Normative:
- ISO 7870 (Control Charts)
- Montgomery, D. C. - Introduction to Statistical Quality Control
"""

import math
from typing import List, Optional, Tuple

from agrostat_app.domain.entities import HarvestBatch, SPCControlLimits
from agrostat_app.domain.exceptions import InsufficientDataForSPCException
from agrostat_app.domain.value_objects import NelsonViolation


class BioStatisticalEngine:
    """Domain service for rigorous biostatistical calculations on harvest datasets."""

    MIN_SAMPLES_REQUIRED = 10

    def compute_spc_limits(
        self,
        batches: List[HarvestBatch],
        metric_attr: str = "rendimiento_kg_ha",
        usl: Optional[float] = None,
        lsl: Optional[float] = None,
    ) -> SPCControlLimits:
        """Calculates Shewhart 3-sigma control limits and checks for process anomalies.

        Args:
            batches: Chronologically sorted list of harvest batches.
            metric_attr: Attribute name to extract ('rendimiento_kg_ha', 'grados_brix', etc.)
            usl: Upper Specification Limit (customer/export tolerance)
            lsl: Lower Specification Limit (customer/export tolerance)

        Raises:
            InsufficientDataForSPCException: When batch count < MIN_SAMPLES_REQUIRED.
        """
        if len(batches) < self.MIN_SAMPLES_REQUIRED:
            raise InsufficientDataForSPCException(
                f"Se requieren mínimo {self.MIN_SAMPLES_REQUIRED} muestras para calcular límites SPC válidos. "
                f"Recibidas: {len(batches)}"
            )

        values = [float(getattr(b, metric_attr)) for b in batches]
        n = len(values)
        mean_val = sum(values) / n

        # Varianza y desviación estándar muestral
        variance = sum((x - mean_val) ** 2 for x in values) / (n - 1)
        sigma = math.sqrt(variance) if variance > 0 else 0.0001

        # Límites Shewhart de 3 Sigmas
        ucl = mean_val + (3.0 * sigma)
        lcl = max(0.0, mean_val - (3.0 * sigma))

        one_sigma_upper = mean_val + (1.0 * sigma)
        one_sigma_lower = max(0.0, mean_val - (1.0 * sigma))
        two_sigma_upper = mean_val + (2.0 * sigma)
        two_sigma_lower = max(0.0, mean_val - (2.0 * sigma))

        # Evaluación de Reglas de Nelson
        violations = self._evaluate_nelson_rules(values, mean_val, sigma, ucl, lcl)

        # Cálculo de Capacidad del Proceso (Cp y Cpk)
        # Si no se proveen límites de especificación externa, se asumen los límites técnicos 3 sigma
        eff_usl = usl if usl is not None else ucl
        eff_lsl = lsl if lsl is not None else lcl

        cp_index = (eff_usl - eff_lsl) / (6.0 * sigma) if sigma > 0 else 1.0
        cpu = (eff_usl - mean_val) / (3.0 * sigma) if sigma > 0 else 1.0
        cpl = (mean_val - eff_lsl) / (3.0 * sigma) if sigma > 0 else 1.0
        cpk_index = min(cpu, cpl)

        is_in_control = len(violations) == 0

        return SPCControlLimits(
            metric_name=metric_attr,
            sample_count=n,
            mean_center_line=mean_val,
            standard_deviation=sigma,
            ucl=ucl,
            lcl=lcl,
            one_sigma_upper=one_sigma_upper,
            one_sigma_lower=one_sigma_lower,
            two_sigma_upper=two_sigma_upper,
            two_sigma_lower=two_sigma_lower,
            cp_index=cp_index,
            cpk_index=cpk_index,
            is_in_statistical_control=is_in_control,
            violations=violations,
        )

    def _evaluate_nelson_rules(
        self, values: List[float], mean: float, sigma: float, ucl: float, lcl: float
    ) -> List[NelsonViolation]:
        """Evaluates Nelson Rules 1 through 4 for special cause anomaly detection."""
        violations: List[NelsonViolation] = []

        # Regla 1: Un punto fuera de los límites de control (UCL / LCL) > 3 sigma
        for i, val in enumerate(values):
            if val > ucl or val < lcl:
                violations.append(
                    NelsonViolation(
                        rule_number=1,
                        rule_name="Punto fuera de 3-Sigma",
                        sample_index=i,
                        observed_value=val,
                        expected_limit=ucl if val > ucl else lcl,
                        description=f"Muestra #{i+1} ({val}) fuera de límites de control [{round(lcl, 2)}, {round(ucl, 2)}]",
                    )
                )

        # Regla 2: 9 puntos consecutivos del mismo lado de la línea central
        side_count = 0
        current_side = None
        for i, val in enumerate(values):
            side = 1 if val >= mean else -1
            if side == current_side:
                side_count += 1
            else:
                current_side = side
                side_count = 1

            if side_count == 9:
                violations.append(
                    NelsonViolation(
                        rule_number=2,
                        rule_name="Desplazamiento del Proceso (9 puntos consecutivos)",
                        sample_index=i,
                        observed_value=val,
                        expected_limit=mean,
                        description=f"9 muestras consecutivas en el {'mismo lado superior' if side == 1 else 'lado inferior'} de la media",
                    )
                )

        # Regla 3: 6 puntos consecutivos en aumento continuo o disminución continua (Tendencia)
        if len(values) >= 6:
            for i in range(5, len(values)):
                window = values[i - 5 : i + 1]
                increasing = all(window[k] < window[k + 1] for k in range(5))
                decreasing = all(window[k] > window[k + 1] for k in range(5))
                if increasing or decreasing:
                    violations.append(
                        NelsonViolation(
                            rule_number=3,
                            rule_name="Tendencia Continua (6 puntos en racha)",
                            sample_index=i,
                            observed_value=values[i],
                            expected_limit=mean,
                            description=f"Tendencia {'ascendente' if increasing else 'descendente'} detectada en muestras #{i-4} a #{i+1}",
                        )
                    )

        # Regla 4: 14 puntos consecutivos alternando hacia arriba y hacia abajo (Oscilación sistemática)
        if len(values) >= 14:
            for i in range(13, len(values)):
                window = values[i - 13 : i + 1]
                diffs = [window[k + 1] - window[k] for k in range(13)]
                alternating = all((diffs[k] * diffs[k + 1]) < 0 for k in range(12))
                if alternating:
                    violations.append(
                        NelsonViolation(
                            rule_number=4,
                            rule_name="Oscilación Sistemática (14 puntos alternantes)",
                            sample_index=i,
                            observed_value=values[i],
                            expected_limit=mean,
                            description=f"Oscilación artificial/sistemática en muestras #{i-12} a #{i+1}",
                        )
                    )

        return violations

    def compute_shewhart_limits(
        self,
        metric_values: List[float],
        metric_name: str,
        lower_spec_limit: Optional[float] = None,
        upper_spec_limit: Optional[float] = None,
    ) -> SPCControlLimits:
        """Calculates Shewhart 3-sigma control limits directly from a list of float values."""
        if len(metric_values) < self.MIN_SAMPLES_REQUIRED:
            raise InsufficientDataForSPCException(
                f"Se requieren mínimo {self.MIN_SAMPLES_REQUIRED} muestras para calcular límites SPC. "
                f"Recibidas: {len(metric_values)}"
            )

        n = len(metric_values)
        mean_val = sum(metric_values) / n
        variance = sum((x - mean_val) ** 2 for x in metric_values) / (n - 1)
        sigma = math.sqrt(variance) if variance > 0 else 0.0001

        ucl = mean_val + (3.0 * sigma)
        lcl = max(0.0, mean_val - (3.0 * sigma))

        one_sigma_upper = mean_val + (1.0 * sigma)
        one_sigma_lower = max(0.0, mean_val - (1.0 * sigma))
        two_sigma_upper = mean_val + (2.0 * sigma)
        two_sigma_lower = max(0.0, mean_val - (2.0 * sigma))

        violations = self._evaluate_nelson_rules(metric_values, mean_val, sigma, ucl, lcl)

        eff_usl = upper_spec_limit if upper_spec_limit is not None else ucl
        eff_lsl = lower_spec_limit if lower_spec_limit is not None else lcl

        cp_index = (eff_usl - eff_lsl) / (6.0 * sigma) if sigma > 0 else 1.0
        cpu = (eff_usl - mean_val) / (3.0 * sigma) if sigma > 0 else 1.0
        cpl = (mean_val - eff_lsl) / (3.0 * sigma) if sigma > 0 else 1.0
        cpk_index = min(cpu, cpl)

        is_in_control = len(violations) == 0

        return SPCControlLimits(
            metric_name=metric_name,
            sample_count=n,
            mean_center_line=mean_val,
            standard_deviation=sigma,
            ucl=ucl,
            lcl=lcl,
            one_sigma_upper=one_sigma_upper,
            one_sigma_lower=one_sigma_lower,
            two_sigma_upper=two_sigma_upper,
            two_sigma_lower=two_sigma_lower,
            cp_index=cp_index,
            cpk_index=cpk_index,
            is_in_statistical_control=is_in_control,
            violations=violations,
        )
