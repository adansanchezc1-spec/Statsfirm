# Módulo 01: Configuración Técnica e Identidad de la Página de Facebook
**Código de Referencia**: `SFC-MKT-FBP-002`  
**Entidad**: Statsfirm Co.  
**Fase PDCO**: PLAN $\rightarrow$ DEVELOPMENT  

---

## 1. Datos Generales y Configuración Básica en Meta

### 1.1. Nombres y Enlaces Canónicos
- **Nombre Oficial de la Página**: `Statsfirm Co. | Ingeniería de Software, Datos & BPMN`
  - *Alternativa Corta*: `Statsfirm Co.`
- **Nombre de Usuario (@Username / Vanity URL)**: `@statsfirm.co`
  - *URL Directa*: `https://www.facebook.com/statsfirm.co`
- **Categoría Principal**: **Empresa de software** (Software Company)
- **Categorías Secundarias**:
  1. **Consultoría en tecnología de la información** (Information Technology Company)
  2. **Servicio de automatización de procesos empresariales** (Business Automation Service)
  3. **Servicio de ciencia de datos** (Data Analytics Service)

---

## 2. Especificación Gráfica: Avatar y Portada

### 2.1. Foto de Perfil (Avatar / Monograma Corporativo)
- **Activo Gráfico**: `assets/logo_icon.jpg` o `docs/02-brand-identity/logo_monogram_app_icon_1788728712598.jpg`.
- **Dimensiones de Subida**: **800 $\times$ 800 px** (Visualización mínima en escritorio: 176 $\times$ 176 px / móvil: 196 $\times$ 196 px).
- **Formato**: PNG sin compresión con fondo institucional `Dark Slate (#0F172A)`.
- **Zona Segura Circular**: Dejar un margen perimetral del 15% para evitar que el recorte circular de Facebook mutile los vértices del isotipo vectorial.

### 2.2. Portada de la Página (Cover Photo) y Regla de Zona Segura Responsive

Facebook utiliza diferentes relaciones de aspecto en escritorio y teléfonos móviles. Para asegurar que el texto y los logotipos no se corten en ningún dispositivo, se diseña un lienzo maestro de **1200 $\times$ 675 px (relación 16:9)** con la siguiente distribución:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LIENZO MAESTRO DE PORTADA FACEBOOK (1200 x 675 px)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ ░░░░░░░░░░░░░░░░ Franja cortada en ESCRITORIO (Top: 90px) ░░░░░░░░░░░░░░░░░░ │
├───────────┬─────────────────────────────────────────────────────┬───────────┤
│ Cortado en│  ZONA SEGURA UNIVERSAL (1000 x 480 px)               │ Cortado en│
│ MÓVIL     │  • Logotipo Principal Horizontal                    │ MÓVIL     │
│ (Left:    │  • Titular: "Transformación Digital con Rigor       │ (Right:   │
│  100px)   │    Matemático, Datos y BPMN"                        │  100px)   │
│           │  • Badge: DAMA-BOK | IEEE | ISO 25010 | Camunda     │           │
│           │  • Acento: Nodos Electric Cyan (#22D3EE)            │  100px)   │
├───────────┴─────────────────────────────────────────────────────┴───────────┤
│ ░░░░░░░░░░░░░░ Franja cortada en ESCRITORIO (Bottom: 105px) ░░░░░░░░░░░░░░░░ │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Contenido Visual de la Portada:
1. **Fondo**: Azul petróleo oscuro (`#0F172A`) con trama sutil de malla blueprint tridimensional (*grid* de ingeniería).
2. **Titular en Portada**:
   - Fuente: `Space Grotesk Bold` en `Pure White (#FFFFFF)`.
   - Texto: *"INGENIERÍA DE SOFTWARE, DATOS & PROCESOS"*.
3. **Subtítulo**:
   - Fuente: `Inter Medium` en `Electric Cyan (#22D3EE)`.
   - Texto: *"Arquitectura Lakehouse • Control Estadístico SPC • Automatización BPMN 2.0"*.
4. **Call To Action Visual**: Flecha sutil en `Code Green (#00FF66)` que apunta hacia el botón interactivo de la página (*"Contáctanos para un Diagnóstico"*).

---

## 3. Información de la Empresa y Sección "Información" (About)

### 3.1. Biografía Corta (Bio / Descripción de 255 Caracteres)
> *"Firma de ingeniería de software, arquitectura de datos (Lakehouse/BI), Control Estadístico de Procesos (SPC) y automatización BPMN 2.0. Transformamos empresas con rigor matemático y estándares internacionales (DAMA-BOK / ISO 25010)."*

### 3.2. Descripción Larga / Historia Corporativa (Sección "Detalles")
```markdown
Statsfirm Co. es una firma de ingeniería tecnológica y analítica avanzada especializada en diseñar, construir y operar soluciones digitales de alto impacto para organizaciones que exigen rigor técnico, trazabilidad del dato y retorno financiero medible.

Nuestra práctica integra cinco divisiones multidisciplinarias:
1. Curaduría de Datos & Arquitectura Lakehouse (DAMA-BOK, Delta Lake, dbt, SQL Dimensional).
2. Inteligencia de Negocios (BI) & Control Estadístico de Procesos (SPC Shewhart, Dashboards en Tiempo Real).
3. Inteligencia Artificial & Data Science (Series de Tiempo, Modelos Predictivos, Machine Learning).
4. Ingeniería de Software & Cloud (Arquitectura Hexagonal, APIs REST, Microservicios, Apps Offline-First).
5. Ingeniería de Procesos BPMN 2.0 & FinOps (Optimización con Camunda, Eliminación de Desperdicios y Tiempos Muertos).

A través de nuestra división especializada, Agro Stat & Tech Co. (AgroStats), llevamos bioestadística avanzada y transformación analítica al sector agropecuario y agroindustrial sin dependencia de hardware cautivo.

📍 Operación Remota Global con base en Colombia (Zona Horaria UTC-5).
🌐 Sitio Web Oficial: https://statsfirm.co
✉️ Contacto Corporativo: contacto@statsfirm.co
```

---

## 4. Canales de Contacto y Botón de Acción Principal (CTA)

| Parámetro | Configuración Oficial |
|---|---|
| **Botón de Acción Principal (CTA)** | **Enviar mensaje de WhatsApp** (o *"Contactarnos"* apuntando a la Landing Page) |
| **Número de WhatsApp Business** | Número verificado de la empresa con saludo automático configurado |
| **Sitio Web** | `https://statsfirm.co` (con parámetros UTM para atribución: `?utm_source=facebook&utm_medium=profile&utm_campaign=fanpage`) |
| **Correo Electrónico** | `contacto@statsfirm.co` / `info@statsfirm.co` |
| **Ubicación / Dirección** | Modalidad: *Empresa de Servicios Digitales / Sin ubicación física abierta al público* (Área de servicio: Colombia, México, Chile, Perú, España, EE.UU.) |
| **Horario de Atención** | Lunes a Viernes: `08:00 AM - 06:00 PM` (UTC-5) |
| **Rango de Precios** | `$$$ (Servicios Corporativos / Consultoría de Ingeniería)` |
| **Enlace a Políticas de Privacidad** | `https://statsfirm.co/privacidad` (Cumplimiento Ley 1581 / GDPR) |
