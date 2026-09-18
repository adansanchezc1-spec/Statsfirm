# Módulo 02: Matriz de Canales, Audiencias y Formatos
**Código de Referencia**: `AST-MKT-SMP-003`  
**Entidad**: Agro Stat & Tech Co. (Spin-off de Statsfirm Co.)  
**Fase PDCO**: PLAN $\rightarrow$ DEVELOPMENT  

---

## 1. Arquitectura Multicanal Integrada

La estrategia de distribución de **Agro Stat & Tech Co.** no es un volcado masivo indiferenciado; cada canal cumple una función anatómica específica dentro del embudo de autoridad, nutrición y conversión agroempresarial:

```
                      [ REDES SOCIALES DE AGRO STATS ]
                                     │
    ┌────────────────┬───────────────┼───────────────┬────────────────┐
    ▼                ▼               ▼               ▼                ▼
 [ LinkedIn ]   [ Instagram ]   [ YouTube ]       [ X / Twitter ] [ WhatsApp / TG ]
  B2B / C-Level   Visual / Agro   Masterclasses   Datos / Alertas  Comunidad VIP
  Directores      Productores     Ingeniería      SIPSA / Clima    Boletín Matutino
  (Autoridad)     (Inspiración)   (Educación)     (Inmediatez)     (Fidelización)
```

---

## 2. Matriz Comparativa de Canales

| Canal | Audiencia Primaria | Objetivo Principal | Formatos Clave | Frecuencia Semanal |
|---|---|---|---|---|
| **LinkedIn** | Gerentes de Operaciones, Directores de Calidad, Agroexportadores, Consultores | Liderazgo de pensamiento, Generación de SQLs (reuniones de negocio) | Carruseles PDF (1080x1350), Artículos Técnicos, Infografías de Arquitectura | 3 a 4 posts / semana |
| **Instagram** | Productores modernos, Agrónomos de campo, Estudiantes de ingeniería agrícola | Alcance, Humanización de marca, Viralidad educativa | Reels (1080x1920), Carruseles "Swipe & Learn", Stories interactivas | 4 a 5 posts + Stories diarias |
| **YouTube** | Ingenieros de datos, Agroanalistas, Investigadores, C-Level técnico | Autoridad profunda, Explicación de metodologías (AgroInnova Lab) | Videos largos (10-15 min), Shorts técnicos (60 seg) | 1 video largo quincenal + 2 Shorts/semana |
| **X (Twitter)** | Analistas de mercados, Economistas agrícolas, Prensa especializada | Inmediatez de datos, Tendencias macroeconómicas y climáticas | Hilos de análisis SIPSA/DANE, Gráficos rápidos de anomalías ENSO | 3 a 5 hilos / semana |
| **WhatsApp / Telegram** | Clientes activos, Productores suscritos a alertas, Comunidad AgroData | Retención, Entrega de valor diario y conversión directa | Boletines en audio/texto, Resúmenes de precios de abastos, Alertas de heladas | Lunes a Viernes (6:30 AM) |

---

## 3. Especificaciones Técnicas y Dimensiones por Canal

### 3.1. LinkedIn (`/company/agrostats-andtech`)
- **Avatar Corporativo**: 400 $\times$ 400 px (PNG / WebP), Isotipo centrado con fondo `#064E3B`.
- **Banner de Cabecera**: 1584 $\times$ 396 px (PNG), Vista cenital de bosque con overlay al 75% y titular en `Space Grotesk Bold` (*"Transformación Agroempresarial basada en Bioestadística y Datos Existentes"*).
- **Carruseles de Documentos (PDF)**:
  - Relación de Aspecto: **4:5 Vertical (1080 $\times$ 1350 px)**.
  - Estructura: Diapositiva 1 (Hook con 35% bosque y titular de alto contraste) $\rightarrow$ Diapositivas 2-6 (Desarrollo técnico en superficie oscura/clara con fórmulas o gráficas Shewhart) $\rightarrow$ Diapositiva final (CTA a descarga o agendamiento).
  - Peso máximo del PDF: 15 MB.

### 3.2. Instagram (`@agrostats.tech`)
- **Avatar**: 320 $\times$ 320 px (Monograma / Isotipo de plántula bio-digital en Bio Neon Green `#10B981`).
- **Feed Vertical (Posts & Carruseles)**: 1080 $\times$ 1350 px (relación 4:5).
- **Reels y Stories**: 1080 $\times$ 1920 px (relación 9:16 vertical a 60 fps).
  - Zona Segura (*Safe Zone*): Margen superior de 220 px e inferior de 380 px libres de texto para no tapar con la interfaz de usuario de Instagram.
- **Portadas de Destacadas**: 1080 $\times$ 1920 px con iconografía técnica minimalista (`#10B981` sobre `#064E3B`).

### 3.3. YouTube (`Agro Stat & Tech Co. / AgroInnova Lab`)
- **Banner del Canal**: 2560 $\times$ 1440 px (Zona segura de texto y logos: 1546 $\times$ 423 px central).
- **Miniaturas (Thumbnails)**: 1280 $\times$ 720 px (16:9), con borde perimetral en `Bio Neon Green` (`#10B981`) de 4px, texto en `Space Grotesk Bold` de no más de 4 palabras y gráfica de control o mapa de calor de fondo.
- **Videos Principales**: 1080p o 4K (16:9 a 24 o 30 fps), audio normalizado a -14 LUFS con tratamiento acústico limpio.

### 3.4. X (Twitter) (`@AgroStatsTech`)
- **Banner**: 1500 $\times$ 500 px.
- **Posts con Gráfica**: 1600 $\times$ 900 px (16:9) o 1200 $\times$ 1200 px (1:1).

---

## 4. Hábitos de Consumo y Horarios Óptimos de Publicación en el Sector Agro

El público agropecuario e industrial tiene rutinas drásticamente diferentes a las de las audiencias urbanas de oficina:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CRONOGRAMA DE ACTIVIDAD DEL USUARIO AGRO                    │
├─────────────────────┬──────────────────────────┬────────────────────────────┤
│ 05:30 - 07:00 AM    │ 12:00 - 01:30 PM         │ 06:30 - 08:30 PM           │
│ "Ronda de Campo"    │ "Almuerzo y Descanso"    │ "Cierre de Jornada y Casa" │
│ Alertas meteorológicas, Revisión de notas técnicas, Resúmenes del día,     │
│ boletín de precios de cotizaciones de mercados   análisis en profundidad,   │
│ centrales de abasto  y carruseles LinkedIn      videos largos en YouTube    │
└─────────────────────┴──────────────────────────┴────────────────────────────┘
```

### Reglas de Publicación por Franja:
1. **Franja Matutina (05:45 - 06:45 AM)**:
   - Contenido: Alertas de precios DANE/SIPSA, pronósticos meteorológicos de alta resolución, tips rápidos de arranque de jornada.
   - Canales: WhatsApp/Telegram, Stories de Instagram, X (Twitter).
2. **Franja de Almuerzo (12:00 - 01:15 PM)**:
   - Contenido: Carruseles educativos en LinkedIn e Instagram (lectura pausada de 2 minutos).
   - Canales: LinkedIn, Instagram Feed.
3. **Franja Nocturna (06:30 - 08:00 PM)**:
   - Contenido: Casos de estudio en video, debates técnicos, testimonios y anuncios de webinars.
   - Canales: YouTube, LinkedIn, Instagram Reels.
