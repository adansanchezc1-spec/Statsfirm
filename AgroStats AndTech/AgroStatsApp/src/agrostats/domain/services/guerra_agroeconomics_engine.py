"""
Motor Agroempresarial de Rentabilidad y Economía de Bioinsumos
Metodología: Guillermo Guerra E. (IICA) - Manual de Administración de Empresas Agropecuarias
"""
from typing import Dict, Any
from src.agrostats.domain.entities import CultivoRentabilidad
from src.agrostats.domain.value_objects import PorcentajeAdopcion
from src.agrostats.domain.exceptions import InvalidAgroeconomicParametersException

class GuillermoGuerraEngine:
    """
    Evalúa la sustitución técnica de insumos químicos por bioinsumos,
    el Margen Bruto por Hectárea (MB/ha) y el Punto de Equilibrio (BEP).
    """

    @staticmethod
    def calcular_rentabilidad(cultivo: CultivoRentabilidad, adopcion: PorcentajeAdopcion) -> Dict[str, Any]:
        if cultivo.rendimiento_kg_ha <= 0 or cultivo.precio_base_cop_kg <= 0:
            raise InvalidAgroeconomicParametersException("El rendimiento y precio base deben ser positivos.")

        factor = adopcion.factor

        # 1. Costos Variables Convencionales vs Bioinsumos
        costo_quimico_base = cultivo.costos_variables_quimicos_ha
        ahorro_quimico = costo_quimico_base * (cultivo.tasa_ahorro_max_bio_pct * factor)
        cv_convencional = cultivo.costos_variables_totales_convencional
        cv_bioinsumos = (costo_quimico_base - ahorro_quimico) + cultivo.costos_variables_otros_ha

        # 2. Costos Totales (Fijos + Variables)
        ct_convencional = cultivo.costos_fijos_ha + cv_convencional
        ct_bioinsumos = cultivo.costos_fijos_ha + cv_bioinsumos

        # 3. Precios Efectivos con Prima Verde por Cero LMR
        prima_export_kg = cultivo.precio_base_cop_kg * (cultivo.prima_verde_max_pct * factor)
        precio_efectivo = cultivo.precio_base_cop_kg + prima_export_kg

        # 4. Ingresos y Margen Bruto (Guillermo Guerra: Ingreso Bruto - Costos Variables)
        ingreso_convencional = cultivo.rendimiento_kg_ha * cultivo.precio_base_cop_kg
        ingreso_bioinsumos = cultivo.rendimiento_kg_ha * precio_efectivo

        mb_convencional = ingreso_convencional - cv_convencional
        mb_bioinsumos = ingreso_bioinsumos - cv_bioinsumos
        ganancia_neta_adicional = mb_bioinsumos - mb_convencional

        # 5. Punto de Equilibrio (Break-Even Point) Físico y Monetario
        bep_precio_convencional = ct_convencional / cultivo.rendimiento_kg_ha
        bep_precio_bioinsumos = ct_bioinsumos / cultivo.rendimiento_kg_ha
        bep_kilos_convencional = ct_convencional / cultivo.precio_base_cop_kg
        bep_kilos_bioinsumos = ct_bioinsumos / precio_efectivo

        # 6. Retorno sobre la Inversión en Capital Operativo (ROI %)
        roi_convencional = ((mb_convencional - cultivo.costos_fijos_ha) / ct_convencional) * 100.0
        roi_bioinsumos = ((mb_bioinsumos - cultivo.costos_fijos_ha) / ct_bioinsumos) * 100.0

        return {
            "codigo_cpc": cultivo.codigo_cpc,
            "nombre_producto": cultivo.nombre_producto,
            "tasa_adopcion_bio_pct": adopcion.porcentaje,
            "ahorro_insumos_quimicos_ha": round(ahorro_quimico, 2),
            "ahorro_insumos_pct": round((ahorro_quimico / costo_quimico_base) * 100.0, 1) if costo_quimico_base > 0 else 0.0,
            "precio_efectivo_cop_kg": round(precio_efectivo, 2),
            "prima_verde_cop_kg": round(prima_export_kg, 2),
            "margen_bruto_convencional_ha": round(mb_convencional, 2),
            "margen_bruto_bioinsumos_ha": round(mb_bioinsumos, 2),
            "ganancia_neta_adicional_ha": round(ganancia_neta_adicional, 2),
            "bep_precio_convencional_cop_kg": round(bep_precio_convencional, 2),
            "bep_precio_bioinsumos_cop_kg": round(bep_precio_bioinsumos, 2),
            "bep_kilos_convencional_ha": round(bep_kilos_convencional, 1),
            "bep_kilos_bioinsumos_ha": round(bep_kilos_bioinsumos, 1),
            "roi_operativo_convencional_pct": round(roi_convencional, 1),
            "roi_operativo_bioinsumos_pct": round(roi_bioinsumos, 1),
            "autor_metodologia": "Guillermo Guerra (IICA) - Manual de Administracion de Empresas Agropecuarias"
        }
