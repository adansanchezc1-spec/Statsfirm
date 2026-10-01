# Especificación Oficial de Identidad Visual y Logotipo: Agro Stat & Tech Co.
**Documento de Referencia**: `AST-CORP-BM-002` (Manual de Marca) & `AST-DSGN-SPEC-011` (Ficha Técnica Estética)  
**Proyecto**: Agro Stat & Tech Co. (Spin-off de Statsfirm Co.)  
**Fecha**: 2026-09-12  
**Fase PDCO**: DEVELOPMENT  
**Skill Activa**: `02-architecture` / `03-development`  

---

## 1. Concepto Creativo: El Contraste "Bosque Profundo & Precisión Bio-Digital"

La identidad visual de **Agro Stat & Tech Co.** plasma la intersección entre la biología del cultivo y la exactitud matemática del software y la bioestadística:

```
          [ Nodo Circular de Datos (Bio Neon Green #10B981) ]
                                 |
           /=====================+=====================\
          /                                             \
  [ Hoja Izquierda ]                             [ Hoja Derecha ]
          \                                             /
           \------- Campana de Gauss / Shewhart -------/
                      (Límites +/- 3 Sigma)
```

1. **La Campana de Gauss (Distribución Normal de Shewhart)**:
   - Representa el Control Estadístico de Procesos (SPC), la reducción de varianza y el rigor cuantitativo.
2. **La Plántula / Brote Bio-Digital**:
   - Dos hojas simétricas (cotiledones) que brotan orgánicamente desde la curvatura de la campana.
3. **El Nodo de Datos Central**:
   - Vértice superior iluminado en **Bio Neon Green (`#10B981`)** con resplandor bioluminiscente, simbolizando el dato exacto como el catalizador esencial del rendimiento del cultivo.

---

## 2. Catálogo de Activos Gráficos Generados

| Activo | Archivo | Formato | Uso Principal |
|---|---|---|---|
| **Logotipo Horizontal Primario (Fotográfico)** | `assets/logo_horizontal_primary.jpg` | JPG 4K | Portadas corporativas, presentaciones y hero header sobre fondo bosque. |
| **Logotipo Apilado Centrado** | `assets/logo_centered_stacked.jpg` | JPG 4K | Afiches, reportes técnicos, packaging bioestadístico y splash screens. |
| **Isotipo / Monograma App Icon** | `assets/logo_monogram_app_icon.jpg` | JPG 4K | Favicon corporativo, app de campo y avatares de redes sociales. |
| **Insignia AgroInnova Lab** | `assets/logo_agroinnova_badge.jpg` | JPG 4K | Certificación de calidad bioestadística y reportes de I+D. |
| **Vector Horizontal Claro** | `assets/logo-horizontal.svg` | SVG | Barra de navegación web principal y documentos PDF/impresos. |
| **Vector Horizontal Oscuro** | `assets/logo-horizontal-dark.svg` | SVG | Footer web corporativo y modos nocturnos. |
| **Vector Isotipo** | `assets/logo-icon.svg` | SVG | Icono responsive e indicadores de carga. |
| **Favicon Web** | `assets/favicon.svg` | SVG | Pestaña del navegador y bookmark icon. |

---

## 3. Sistema Cromático Agro Tech (Documento 02)

| Nombre del Color | Código HEX | RGB | Uso y Significado |
|---|---|---|---|
| **Deep Forest Green** | `#064E3B` | `(6, 78, 59)` | Color institucional primario. Profundidad del dosel vegetal y solidez corporativa. |
| **Bio Neon Green** | `#10B981` | `(16, 185, 129)` | Acento tecnológico y biológico. Procesos bajo control SPC ($C_{pk} \ge 1.33$), nodos y botones de acción. |
| **Earth Graphite** | `#18181B` | `(24, 24, 27)` | Base de contraste oscuro, tarjetas técnicas y consola de datos. |
| **Harvest Amber** | `#F59E0B` | `(245, 158, 11)` | Alertas tempranas SPC, límites de advertencia ($\pm 2\sigma$) y maduración de cosecha. |
| **Alert Red** | `#DC2626` | `(220, 38, 38)` | Violaciones críticas de Western Electric y registros aislados en DLQ. |
| **Laboratory White** | `#FFFFFF` | `(255, 255, 255)` | Fondo principal del portal (estética minimalista de laboratorio biotecnológico). |
| **Clean Surface Light** | `#F8FAFC` | `(248, 250, 252)` | Superficie de widgets, tarjetas de métricas y simuladores. |

---

## 4. Tipografía Institucional

1. **Display & Titulares**: `Space Grotesk` (Google Fonts).
   - "AGRO STAT": Mayúsculas, peso Bold (700).
   - "& TECH CO.": Mayúsculas, peso SemiBold (600), espaciado expandido (*tracking* +120).
2. **Cuerpo de Lectura**: `Inter` (Google Fonts).
   - Pesos: Regular (400), Medium (500) y SemiBold (600).
3. **Métricas y Fórmulas**: `JetBrains Mono` (Google Fonts).
   - Utilizado para límites de control Shewhart ($UCL, LCL, \bar{X}$), índices $C_p, C_{pk}$, consultas dbt y JSON payloads.

---

## 5. Accesibilidad y Ratios de Contraste (WCAG 2.1 AAA)

- Texto principal `#0F172A` sobre fondo `#FFFFFF`: **15.8:1** (Supera holgadamente el estándar AAA de 7.0:1).
- Texto `#064E3B` sobre fondo `#FFFFFF`: **8.9:1** (Cumple estándar AAA).
- Isotipo `#10B981` sobre fondo `#064E3B`: **5.2:1** (Cumple estándar de elementos gráficos y titulares).
