# Módulo 03: Estrategia de Contenidos y Formatos para Facebook
**Código de Referencia**: `SFC-MKT-FBP-004`  
**Entidad**: Statsfirm Co.  
**Fase PDCO**: PLAN $\rightarrow$ DEVELOPMENT  

---

## 1. Adaptación del Contenido Técnico al Algoritmo de Facebook

El algoritmo de Facebook prioriza publicaciones que generen **conversación significativa (comentarios de más de 4 palabras), tiempo de retención en video y compartidos en grupos**. Para una firma B2B de ingeniería de software y datos como **Statsfirm Co.**, el contenido debe estructurarse en 4 formatos nativos de alto rendimiento:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 FORMATOS NATIVOS DE ALTO RENDIMIENTO EN FACEBOOK             │
├─────────────────────┬──────────────────────────┬────────────────────────────┤
│ 1. ÁLBUMES TÉCNICOS │ 2. FACEBOOK REELS        │ 3. EVENTOS EN VIVO         │
│ Desgloses visuales  │ Explicaciones en 45 seg  │ Masterclasses técnicas     │
│ de arquitectura en  │ de conceptos complejos   │ con recordatorios push     │
│ 4 a 6 diapositivas  │ (BPMN, Cartas Shewhart)  │ y registro de asistentes   │
└─────────────────────┴──────────────────────────┴────────────────────────────┘
```

---

## 2. Los 4 Formatos Clave de Publicación

### 2.1. Formato A: Álbumes de Infografías Técnicas (Multi-Image Posts)
- **Estructura**: Publicación con 4 a 6 imágenes en formato cuadrado (1080 $\times$ 1080 px) o vertical (1080 $\times$ 1350 px).
- **Caso de Uso**: Explicar un flujo de ingeniería paso a paso (ej. *"Cómo fluye el dato desde la ingesta cruda Bronze hasta el dashboard Gold sin ensuciar la base de datos"*).
- **Ventaja Algorítmica**: Cada clic en una imagen para ampliarla cuenta como una interacción positiva en el algoritmo de Facebook, multiplicando el alcance orgánico.

### 2.2. Formato B: Facebook Reels & Video Nativo (Relación 9:16 vertical)
- **Duración**: 30 a 60 segundos.
- **Contenido**:
  - Screencasts de código en Python o SQL con resaltado de sintaxis sobre fondo oscuro.
  - Simulaciones animadas de procesos BPMN en Camunda mostrando la eliminación de cuellos de botella.
  - El "Mito vs. Realidad" de los proyectos de datos en empresas reales.
- **Audio y Subtítulos**: Obligatorio subtitular al 100% el video (el 85% de los usuarios en Facebook navegan con el audio apagado).

### 2.3. Formato C: Publicaciones de Enlace con Tarjetas OpenGraph Ricas
- **Objetivo**: Conducir tráfico calificado hacia la landing page corporativa (`https://statsfirm.co`) o a los artículos del blog técnico.
- **Requisitos de OpenGraph (Meta Tags en el HTML)**:
  ```html
  <meta property="og:title" content="Arquitectura de Datos y Rigor Estadístico | Statsfirm Co." />
  <meta property="og:description" content="Diseñamos Data Warehouses, Lakehouses y flujos BPMN 2.0 con estándares DAMA-BOK e ISO 25010." />
  <meta property="og:image" content="https://statsfirm.co/assets/og-facebook-cover.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  ```

### 2.4. Formato D: Eventos de Facebook para Masterclasses y Webinars
- **Frecuencia**: 1 evento mensual organizado por **Innova Lab**.
- **Temas Clave**:
  - *"Taller Práctico: Implementando Data Contracts con Pydantic y dbt desde Cero"*.
  - *"Control Estadístico de Procesos (SPC) aplicado a la Agroindustria y Operaciones de Planta"*.
- **Ventaja**: Los usuarios registrados reciben notificaciones automáticas y recordatorios por correo y en la app de Facebook antes de comenzar el en vivo.

---

## 3. Parrilla Editorial Semanal para Facebook

```
┌───────────┬──────────────────────┬──────────────────────────────────────────────────────────┐
│ DÍA       │ TIPO DE FORMATO      │ ENFOQUE Y TEMA                                           │
├───────────┼──────────────────────┼──────────────────────────────────────────────────────────┤
│ Martes    │ Álbum Técnico        │ Arquitectura de Software / Curaduría de Datos (DAMA-BOK) │
│ Jueves    │ Reel / Video Corto   │ Píldora de Código, BPMN o Demo de la App Offline         │
│ Sábado    │ Post con Enlace / CTA│ Caso de Éxito con ROI / Descarga de Plantilla o Whitepaper│
│ Domingos  │ Story Interactiva    │ Pregunta de diagnóstico técnico / Encuesta de madurez    │
└───────────┴──────────────────────┴──────────────────────────────────────────────────────────┘
```

---

## 4. Estrategia de Grupos y Comunidad Técnica

1. **Creación del Grupo Oficial**: *"Comunidad Statsfirm: Ingeniería de Datos, BPMN y Arquitectura de Software"*.
   - Propósito: Espacio de debate técnico moderado donde se comparten scripts, plantillas de dbt, diagramas BPMN y ofertas de trabajo/colaboración.
2. **Participación Estratégica en Grupos Existentes**:
   - Grupos de *Python Colombia / Latam*, *Data Science en Español*, *Ingenieros Industriales & BPMN*, *AgTech Hispanoamérica*.
   - Aporte de valor genuino: Responder dudas complejas citando estándares y compartiendo diagramas técnicos con la firma de Statsfirm Co., sin spam comercial directo.
