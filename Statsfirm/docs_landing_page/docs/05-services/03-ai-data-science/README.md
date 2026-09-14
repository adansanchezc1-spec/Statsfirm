# Servicio 03: Modelos Predictivos y Machine Learning (AI Engineering & Applied Data Science)

**Código de Servicio**: STF-SRV-03  
**Línea de Portafolio**: 03 / Inteligencia Artificial & Analítica Avanzada  
**Normativa Aplicable**: SWEBOK Cap. 2, DAMA-BOK (Ciencia de Datos y Minería), ISO/IEC 25010 (Exactitud y Robustez de Modelos).  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico*), Sección `#servicios` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones?
Desarrolla e implementa algoritmos matemáticos y modelos de aprendizaje automático (*Machine Learning*) que aprenden de los datos históricos de la empresa para anticipar la demanda comercial, detectar clientes en riesgo de abandono (*churn*), optimizar inventarios y automatizar decisiones complejas en producción.

### Metáfora Operativa
Es como tener a un equipo élite de bioestadísticos y científicos de datos trabajando 24/7 para predecir cuándo se agotará un producto en bodega antes de que suceda, qué cliente clave está evaluando irse con la competencia y cuál es el precio óptimo para maximizar el margen.

### Dolor de Negocio Resuelto
- **Dinero Atrapado en Inventario Muerto**: Evita compras excesivas de productos que se quedan estancados en bodega y previene quiebres de stock en momentos de alta demanda.
- **Pérdida Silenciosa de Clientes**: Alerta oportunamente las señales tempranas de desgaste en la relación comercial antes de la rescisión de contratos.
- **Optimización de Precios y Rutas**: Sustituye estimaciones empíricas por modelos de optimización combinatoria y regresiones robustas.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Pronóstico de Demanda Multivariado** | Modelos estocásticos de series temporales (Prophet, ARIMA, LightGBM, XGBoost) con factores de estacionalidad. | API de predicción conectada al ERP/WMS de la empresa. |
| **Prevención Temprana de Churn** | Clasificación probabilística del riesgo de deserción de clientes basada en patrones de compra y tickets. | Tablero de riesgo comercial y alertas automáticas de retención. |
| **Optimización de Rutas & Logística** | Solución algorítmica de ruteo vehicular (VRP) y asignación óptima de carga en bodegas. | Motor de asignación de fletes y reducción de costos logísticos. |
| **MLOps & Monitoreo de Data Drift** | Tuberías CI/CD para reentrenamiento automático y detección de pérdida de precisión algorítmica. | Registro de modelos en MLflow con métricas de desempeño en vivo. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Lenguajes       │ Python 3.11+ (PEP 8), SQL ANSI, Rust      │
│ Frameworks ML   │ Scikit-learn, XGBoost, LightGBM, PyTorch  │
│ MLOps & Tracking│ MLflow, Weights & Biases, DVC             │
│ Feature Store   │ Feast, Hopsworks                          │
│ Despliegue API  │ FastAPI, Docker, Triton Inference Server  │
│ Monitoreo       │ Evidently AI, Prometheus, Grafana         │
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Precisión de Pronóstico (MAPE)**: Error absoluto medio porcentual < 8% en pronósticos a 30 y 60 días.
- **Latencia de Inferencia**: < 50ms para predicciones en línea vía API REST.
- **Garantía Anti-Drift**: Reentrenamiento y validación automática semanal de modelos.
