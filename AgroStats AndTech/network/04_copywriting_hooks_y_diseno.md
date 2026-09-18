# Módulo 04: Copywriting, Hooks de Alto Impacto y Guía Visual
**Código de Referencia**: `AST-MKT-SMP-005` (Basado en `AST-DSGN-SPEC-011`)  
**Entidad**: Agro Stat & Tech Co. (Spin-off de Statsfirm Co.)  
**Fase PDCO**: PLAN $\rightarrow$ DEVELOPMENT  

---

## 1. Psicología del Comprador Agropecuario y Agroindustrial

El productor, el director de calidad y el gerente agroindustrial comparten tres rasgos psicológicos fundamentales:
1. **Escepticismo radical hacia la teoría abstracta**: Han visto fracasar múltiples iniciativas tecnológicas que prometían revolucionar el campo con "sensores mágicos" o "inteligencia artificial" que no soportó el barro ni la falta de internet.
2. **Foco absoluto en la certidumbre y el flujo de caja**: Valoran lo que reduce el riesgo climático, evita mermas en empaque y ahorra jornales o fertilizantes.
3. **Respeto por quien conoce el terreno**: Conectan de inmediato cuando el mensaje demuestra conocimiento real del cultivo (épocas de floración, grados Brix, calibres, jornales, cuadrillas, plagas).

---

## 2. Catálogo Maestro de Ganchos (Hooks) de Alta Retención

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CATEGORÍAS DE GANCHOS (HOOKS) DE RETENCIÓN               │
├─────────────────────┬──────────────────────────┬────────────────────────────┤
│ 1. PÉRDIDA FINANCIERA│ 2. PARADOJA BIOESTADÍSTICA│ 3. CONTRASTE BRUTAL        │
│ "Estás perdiendo    │ "Tu lote se ve verde en   │ "Cultivar por intuición    │
│ $350 USD por Ha..." │ el satélite, pero está a │ vs. Cultivar bajo SPC:     │
│                     │ 72 horas del colapso..." │ 24% más de margen neto."   │
└─────────────────────┴──────────────────────────┴────────────────────────────┘
```

### 2.1. Categoría 1: Pérdida Financiera y Fugas de Dinero Ocultas
- **Hook 1A**: *"Estás perdiendo $350 USD por hectárea en fertilizante nitrogenado que tu cultivo jamás absorbe. Esta carta de control te muestra el porqué."*
- **Hook 1B**: *"El 18% de tu fruta de exportación termina vendiéndose a precio de remate en la plaza local. No es problema de clima; es un problema de variabilidad de calibre en empaque."*
- **Hook 1C**: *"¿Sabes cuánto te cuesta un operario que tarda 4 minutos anotando una planilla que nadie va a digitalizar? Multiplícalo por 25 cuadrillas."*

### 2.2. Categoría 2: Paradojas Agrícolas y Mitos Tecnológicos
- **Hook 2A**: *"El satélite te muestra el lote completamente verde (NDVI 0.82), pero la planta está a 48 horas de un estrés hídrico severo. Te explicamos por qué el NDVI sin bioestadística de suelo te engaña."*
- **Hook 2B**: *"El mito más caro del campo: 'Para digitalizar mi finca necesito llenar cada lote de sensores importados'."*
- **Hook 2C**: *"Tu promedio de producción dice que estás ganando dinero. La varianza entre tus tablones dice que estás subsidiando 3 hectáreas en pérdida."*

### 2.3. Categoría 3: Autoridad Científica y Control Estadístico (SPC)
- **Hook 3A**: *"Cómo un índice $C_{pk}$ de 1.42 blindó la línea de empaque de una agroexportadora contra cualquier rechazo en el puerto de Rotterdam."*
- **Hook 3B**: *"Las 4 Reglas de Nelson explicadas para que cualquier agrónomo detecte una plaga 10 días antes de que sea visible a simple vista."*
- **Hook 3C**: *"Si tus registros de campo no pasan un Data Contract, cualquier modelo de Machine Learning te dará predicciones que te costarán la cosecha."*

### 2.4. Categoría 4: Realismo Operativo (El Campo sin Internet)
- **Hook 4A**: *"Una app agrícola que necesita conexión 4G en medio de la cordillera no es tecnología; es un pisapapeles digital."*
- **Hook 4B**: *"5,000 registros de cuadrilla capturados en el fondo del lote, con cero internet y sincronización perfecta al llegar a la oficina. Así funciona SQLite + CRDTs."*

---

## 3. Fórmulas Estructuradas de Copywriting AgroTech

### 3.1. Fórmula PASA (Problema - Agitación - Solución - Acción)

```markdown
[PROBLEMA]: En el empaque de mango, 1 de cada 5 cajas es rechazada por no cumplir el peso estándar.
[AGITACIÓN]: Eso representa $12,000 USD al mes en penalizaciones de clientes internacionales y fruta reempacada a contrarreloj.
[SOLUCIÓN]: Con una Carta de Control Shewhart X-barra y el monitoreo de límites +/- 3 sigma, estabilizamos la variabilidad de la balanza en solo 14 días.
[ACCIÓN]: Comenta "SPC" y te enviamos la plantilla descargable en Excel y Python lista para calibrar tus básculas.
```

### 3.2. Fórmula BAB (Before - After - Bridge)

```markdown
[BEFORE - ANTES]: Antes de aplicar ingeniería de datos, Don Fernando decidía la fecha de cosecha mirando los días del calendario lunar y el promedio del año pasado. Pérdida promedio por sobremaduración: 14%.
[AFTER - DESPUÉS]: Hoy utiliza el modelo de acumulación térmica (GDD) y las series temporales de abastecimiento SIPSA en su celular. Pérdida: menos del 1.8%.
[BRIDGE - EL PUENTE]: El puente fue la metodología Agro-STF y la integración de datos abiertos del IDEAM con sus registros históricos de campo.
```

---

## 4. Guía Visual y Arquitectura Estética de las Publicaciones

Basada en la especificación formal `AST-DSGN-SPEC-011` (*"Bosque Profundo & Precisión Bio-Digital"*):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               ARQUITECTURA DE COMPOSICIÓN (REGLA 35 / 65)                  │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 35% SUPERIOR / LATERAL:              │ 65% PRINCIPAL / CONTENIDO:           │
│ Fondo de bosque denso o plantación   │ Superficie técnica sólida en         │
│ real con overlay verde oscuro        │ Earth Graphite (#18181B) o           │
│ (#064E3B al 75%) + Gaussian Blur     │ Laboratory White (#FFFFFF)           │
│ + Logotipo de plántula bio-digital   │ Tipografía Space Grotesk + Fórmulas  │
│ (Trazo blanco y Bio Neon Green)      │ y Cartas Shewhart en JetBrains Mono  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 4.1. Sistema Cromático Obligatorio

| Color | HEX | Uso en el Post |
|---|---|---|
| **Deep Forest Green** | `#064E3B` | Fondo institucional primario, banners y cabeceras. |
| **Bio Neon Green** | `#10B981` | Botones de acción, llamadas de atención, nodos activos, $C_{pk} \ge 1.33$. |
| **Earth Graphite** | `#18181B` | Tarjetas técnicas oscuras, cajas de código y gráficos nocturnos. |
| **Harvest Amber** | `#F59E0B` | Alertas tempranas, límites a $\pm 2\sigma$, advertencias climáticas. |
| **Alert Red** | `#DC2626` | Violaciones de reglas de Nelson, límites fuera de control ($\pm 3\sigma$). |
| **Pure White** | `#FFFFFF` | Textos titulares principales sobre fondo oscuro y fondos de reportes claros. |

### 4.2. Jerarquía Tipográfica
- **Titulares de Portada (Hook)**: `Space Grotesk Bold`, tamaño grande (48 a 72 pt), mayúsculas o altas/bajas con contraste alto.
- **Cuerpo de Explicación**: `Inter Regular / Medium`, máximo 3 líneas por diapositiva en carruseles para asegurar legibilidad en smartphones de 5 pulgadas.
- **Gráficas, Coordenadas y Fórmulas**: `JetBrains Mono` con acento en Bio Neon Green.
  - *Detalle estético institucional*: Incluir coordenadas geográficas sutiles al pie de las piezas para autenticidad de campo: `4°20'44"N 74°21'43"W | ELEV: 1,720m | RH: 74%`.

---

## 5. Checklist de Control de Calidad Previo a Publicar (8 Filtros)

- [ ] **Filtro 1: Ratio de Contraste WCAG**: ¿Cumple con un ratio mínimo de 7:1 (ideal 11.5:1)?
- [ ] **Filtro 2: Isotipo Institucional**: ¿Está presente el isotipo de la plántula gaussiana sin distorsión de escala?
- [ ] **Filtro 3: Regla 35/65**: ¿Se respeta el balance entre el fondo orgánico de bosque y el área técnica de datos?
- [ ] **Filtro 4: Legibilidad en Móvil**: ¿Se lee con claridad en la pantalla de un celular sin necesidad de hacer zoom?
- [ ] **Filtro 5: Cero Humo Tecnológico**: ¿Cada término técnico (ej. $C_{pk}$, Shewhart) tiene su aplicación práctica explicada?
- [ ] **Filtro 6: Acento Bio Neon**: ¿Se utilizó `#10B981` únicamente para resaltar elementos clave y no como fondo masivo?
- [ ] **Filtro 7: Coherencia de Datos**: ¿Las cifras y fórmulas matemáticas presentadas son 100% verídicas y auditadas?
- [ ] **Filtro 8: Call to Action (CTA)**: ¿Hay una instrucción clara de qué debe hacer el lector (descargar, comentar, compartir)?
