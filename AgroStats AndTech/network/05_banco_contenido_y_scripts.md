# Módulo 05: Banco de Contenidos, Guiones y Plantillas Listas para Producción
**Código de Referencia**: `AST-MKT-SMP-006`  
**Entidad**: Agro Stat & Tech Co. (Spin-off de Statsfirm Co.)  
**Fase PDCO**: PLAN $\rightarrow$ DEVELOPMENT  

---

## 1. Banco de Publicaciones Listas para Producción

A continuación se presentan los guiones, estructuras diapositiva por diapositiva y copys listos para publicar en los diferentes canales de la marca.

---

### Pieza 01: Carrusel Educativo LinkedIn / Instagram (Formato PDF 1080x1350)
- **Pilar**: Pilar 1 (Bioestadística & SPC)
- **Audiencia**: Directores de Calidad, Jefes de Poscosecha, Gerentes de Agroexportación.
- **Objetivo**: Posicionamiento de Autoridad y Descarga de Plantilla ($C_{pk}$ Agro).

#### Estructura Diapositiva por Diapositiva:

```
[Slide 1 - Portada / Hook]
Fondo: 35% Bosque profundo con overlay verde #064E3B + Isotipo en Bio Neon.
Titular (Space Grotesk Bold): "¿Por qué tu empaque de exportación pierde miles de dólares si 'el promedio' da bien?"
Subtítulo (Inter): La trampa del promedio simple y cómo el índice Cpk salva tus contenedores.
Coordenadas al pie: 4°20'44"N 74°21'43"W | Agro Stat & Tech Co.

[Slide 2 - El Problema Oculto]
Fondo: Earth Graphite (#18181B)
Titular: El 90% de las fincas evalúan sus cajas con el promedio.
Gráfica: Comparación de dos distribuciones con el mismo promedio (200g), pero una tiene el doble de varianza.
Texto: "Si tu cliente en Europa exige entre 190g y 210g, un promedio de 200g no garantiza nada si tu varianza arroja frutos de 180g y 220g. Esos extremos son fruta rechazada o regalada."

[Slide 3 - La Solución Matemática: Índice Cpk]
Fondo: Earth Graphite (#18181B)
Titular: Presentamos el Índice de Capacidad del Proceso (Cpk)
Fórmula (JetBrains Mono en #10B981): 
Cpk = min[ (USL - X̄) / (3σ) , (X̄ - LSL) / (3σ) ]
Texto explicativo:
- Cpk < 1.00 🔴 Proceso incapaz (Pérdidas masivas).
- 1.00 ≤ Cpk < 1.33 🟡 Aceptable con riesgo de merma.
- Cpk ≥ 1.33 🟢 Proceso bajo Control Estadístico de Clase Mundial.

[Slide 4 - Caso de Campo Real]
Fondo: Clean Surface Light (#F8FAFC) con texto en Deep Slate (#0F172A)
Titular: Finca de Aguacate Hass en Antioquia
- Estado Inicial: Cpk = 0.78 (16.4% de cajas fuera de especificación en destino).
- Intervención Agro-STF: Calibración por cuadrilla y carta de control Shewhart en tiempo real.
- Estado Final (Semana 3): Cpk = 1.41 (Merma reducida al 1.2%).
- Ahorro mensual generado: $8,400 USD.

[Slide 5 - Cero Inversión en Hardware]
Fondo: Deep Forest Green (#064E3B)
Titular: "No necesitas comprar básculas nuevas ni sensores importados."
Texto: "Solo necesitas tomar los datos que tus operarios ya registran en las planillas de pesaje y pasarlos por nuestro motor bioestadístico."

[Slide 6 - Llamada a la Acción (CTA)]
Fondo: Earth Graphite (#18181B)
Titular: ¿Quieres auditar el Cpk de tu línea de empaque hoy mismo?
Texto: Comenta la palabra "CPK" en este post o escríbenos por mensaje directo y te enviaremos nuestra **Plantilla Bioestadística Agro-STF (Excel + Python)** sin costo.
Logo institucional completo al centro.
```

#### Copy Acompañante para LinkedIn:
```markdown
El promedio es la métrica más engañosa de la agricultura moderna.

Puedes tener un lote de café con un promedio perfecto de humedad del 11.5%, pero si tienes sacos con 9% y otros con 14%, la mitad de tu lote se va a sobretostar y la otra mitad desarrollará hongos en el contenedor.

En la industria automotriz y aeroespacial nadie evalúa la calidad con promedios simples; utilizan el **Índice de Capacidad del Proceso (Cpk)** y el **Control Estadístico de Procesos (SPC)** de Shewhart.

En **Agro Stat & Tech Co.** adaptamos este rigor matemático a la realidad del campo y la agroindustria:
✅ Detecta variabilidad antes de despachar el camión.
✅ Reduce mermas y castigos de precio en destino.
✅ Cero compra de hardware o sensores cautivos: usamos tus datos actuales.

Desliza el carrusel 👆 para ver cómo calcular el Cpk de tu empaque y comenta **CPK** para enviarte la plantilla técnica gratuita.

#AgTech #Bioestadística #ControlDeCalidad #Agroindustria #AgroStats #DataScienceAgro
```

---

### Pieza 02: Guion de Video Reel / TikTok Agro (Formato 1080x1920 - 45 Segundos)
- **Pilar**: Pilar 2 / 3 (Mitos Tech & Diferenciación)
- **Protagonista**: Ingeniero / Científico de Datos con chaleco de campo sobre fondo de plantación real.

```
[00:00 - 00:05] GANCHO VISUAL (HOOK):
Visual: El presentador sostiene una tablet mostrando un mapa satelital lleno de verde fosforescente, y luego señala una planta marchita en el suelo.
Audio / Voz: "Tu satélite te dice que tu lote está perfecto y verde... pero tus plantas están a 48 horas de morir de sed. Te explico por qué el NDVI te engaña."

[00:05 - 00:18] DESARROLLO DEL CONFLICTO:
Visual: Gráfica animada en pantalla dividida. Izquierda: Imagen satelital con NDVI 0.80. Derecha: Curva de humedad en perfil de suelo cayendo en picada (Cartas Shewhart en JetBrains Mono).
Audio / Voz: "El NDVI solo mide la reflectancia de la clorofila en el dosel superior. Cuando la imagen satelital se pone amarilla, tu cultivo ya sufrió daño celular irreversible y perdiste el 15% del rendimiento."

[00:18 - 00:32] LA SOLUCIÓN AGRO-STF:
Visual: El presentador abre la App Móvil de AgroStats (modo offline) e ingresa tres datos simples de campo (textura, días sin lluvia, registro de tensiómetro manual).
Audio / Voz: "En Agro Stat & Tech Co. no te vendemos sensores caros. Integramos tus registros de campo con los modelos climatológicos abiertos del IDEAM y la NASA. Así predecimos el déficit hídrico antes de que ocurra."

[00:32 - 00:45] CIERRE Y CTA:
Visual: Logo institucional animado sobre fondo bosque + Texto en Bio Neon (#10B981): "Audita tu lote".
Audio / Voz: "Deja de cultivar a ciegas. Ve al link de nuestro perfil y descarga gratis nuestra guía de Control Estadístico de Riego."
```

---

### Pieza 03: Post Técnico de Autoridad (LinkedIn / Newsletter Especializada)
- **Pilar**: Pilar 3 (Data Contracts & Lakehouse Agro)
- **Audiencia**: Ingenieros de Datos, Directores de TI Agro, Gerentes de Transformación Digital.

```markdown
# Data Contracts en el Agro: Por qué el 80% de los proyectos de IA agrícola fracasan en el lodo

El principal enemigo de la analítica en el campo no es la falta de datos; es la **entropía del dato agrícola**.

El agrónomo anota "Lote 4" en un cuaderno; el operario de báscula escribe "Lt. 04 - Sector Norte" en un Excel con celdas combinadas; y el laboratorio de suelos entrega un PDF escaneado con la mitad de las columnas borrosas.

Cuando intentas entrenar un modelo de machine learning con ese vertedero de datos, obtienes predicciones basura (*Garbage In, Garbage Out*).

¿Cómo lo resolvemos en **Agro Stat & Tech Co.** bajo el marco **DAMA-BOK**?

Implementando **Data Contracts** estrictos desde la capa Bronze de ingesta:

1. **Validación de Tipos y Esquemas**: Si el pH no está entre 3.5 y 9.0, o los grados Brix no son numéricos, el registro se aísla automáticamente en una cola de descarte (Dead Letter Queue - DLQ).
2. **Estandarización Espacial DIVIPOLA**: Ningún municipio entra como texto libre; todos se validan contra el catálogo del DANE.
3. **Consistencia Lógica**: Los kilos exportables jamás pueden superar los kilos brutos cosechados.

No necesitas servidores millonarios en la nube para empezar. Con un Lakehouse embebido en DuckDB y validación en Python (Pydantic), blindas la calidad de tu agroempresa desde el día 1.

¿En tu empresa aún limpian datos a mano los viernes por la tarde? Hablemos.

#DataEngineering #DataContracts #AgTech #DAMA #DuckDB #PythonAgro
```

---

### Pieza 04: Formato Diario del Boletín Matutino (WhatsApp / Telegram VIP)
- **Pilar**: Pilar 4 (Precios SIPSA & Clima)
- **Horario**: Lunes a Viernes, 06:15 AM
- **Formato**: Texto estructurado con emojis sobrios + Imagen infográfica rápida.

```markdown
🌱 *BOLETÍN AGRODATA — 18 DE SEPTIEMBRE DE 2026*
*Agro Stat & Tech Co. | División de Inteligencia de Mercados*

📊 *1. PULSO DE PRECIOS MAYORISTAS (DANE - SIPSA)*
• *Aguacate Hass (kg)*:
  - Corabastos (Bogotá): $6,200 (▲ +4.2% vs. ayer)
  - Cavasa (Cali): $5,900 (▼ -1.5%)
  - Mayorista Medellín: $6,400 (▬ Estable)
• *Limón Tahití (Bulto 50kg)*: $145,000 (▲ Fuerte repunte por menor oferta en Tolima).
• *Café Pergamino Seco (Carga 125kg)*: $2,180,000 COP (Tasa FLC estable).

🌦️ *2. MONITOREO CLIMÁTICO & ENSO (IDEAM / NASA POWER)*
• *Región Andina*: Probabilidad de lluvias moderadas en la tarde (15-25 mm). Ventana óptima de aspersión foliar: 06:30 AM a 10:30 AM.
• *Región Caribe*: Déficit de presión de vapor elevado (VPD > 1.8 kPa). Alerta de evapotranspiración acelerada en cítricos.

💡 *3. PÍLDORA BIOESTADÍSTICA DEL DÍA*
"La Regla 1 de Nelson indica que un solo punto fuera de los límites ±3σ es evidencia de una causa especial en el lote (ej. fuga en manguera de goteo o calibración defectuosa de boquilla)."

📲 *¿Necesitas auditar la variabilidad de tus cosechas?* Responde a este mensaje con la palabra *AUDITORÍA* y un especialista de nuestro equipo se pondrá en contacto.
```
