# Statsfirm Co. — Plataforma Web Comercial & Corporativa Oficial

**Código Documental**: SFC-WEB-COM-001  
**Versión**: 2.0.0  
**Arquitectura**: Node.js + Express + REST BFF + Frontend Comercial Reactivo Vanilla JS  
**Normativa Aplicable**: Documento 05 (Catálogo de Servicios y Portafolio Tecnológico), Documento 02 (Manual de Marca y Sistema de Diseño), Documento 08 (BPMN-01 Captación de Clientes) y estándar ISO/IEC 25010.

---

## 1. Propósito de la Plataforma Web

Esta aplicación web constituye el **sitio web comercial y corporativo oficial** con el que clientes potenciales y tomadores de decisiones conocen los servicios de **Statsfirm Co.**, exploran su arquitectura de referencia, calculan alcances y presupuestos de proyecto de forma interactiva, y formalizan solicitudes de consultoría bajo el protocolo oficial de captación **BPMN-01**.

---

## 2. Puesta en Marcha

### Prerrequisitos
- Node.js versión 18+ o superior (`node -v`).
- Puerto `3000` disponible en el entorno local.

### Instalación y Ejecución
1. Navegar al directorio de la aplicación:
   ```bash
   cd app
   ```
2. Instalar las dependencias:
   ```bash
   npm install
   ```
3. Iniciar el servidor web:
   ```bash
   npm start
   ```
4. Abrir en el navegador:
   ```
   http://localhost:3000
   ```

---

## 3. Estructura del Proyecto

```
app/
├── server.js                     # Servidor HTTP Express, enrutador BFF y middleware de telemetría
├── package.json                  # Dependencias del proyecto (express, cors)
├── data/
│   ├── servicesCatalog.js        # Catálogo canónico de las 5 líneas de servicio, SaaS y engagement models
│   └── leadsStore.js             # Almacén de leads comerciales y algoritmo de scoring BPMN-01
├── routes/
│   ├── services.js               # Endpoints REST GET /api/services y GET /api/services/:id
│   ├── contact.js                # Endpoints REST POST /api/contact, POST /api/quote y GET /api/leads
│   └── bpmn.js                   # Catálogo y resolvedor auxiliar de esquemas Camunda BPMN
├── public/
│   ├── index.html                # Landing page comercial corporativa de alta fidelidad
│   ├── css/
│   │   └── style.css             # Sistema de diseño oficial Dark Slate, Code Green y Electric Cyan
│   ├── js/
│   │   └── main.js               # Controlador de interacción, cotizador paramétrico y envío AJAX
│   └── assets/
│       ├── logo_primary.jpg      # Imagotipo institucional oficial Statsfirm Co.
│       ├── logo_stacked.jpg      # Logotipo centrado vertical con isotipo de nodo Lakehouse
│       ├── logo_icon.jpg         # Monograma/App Icon corporativo
│       └── logo_innova.jpg       # Emblema oficial de Innova Lab
```

---

## 4. Secciones de la Plataforma Web

1. **Header & Navbar**: Barra de navegación fija con logotipo oficial, enlaces ancla a secciones y botón de acción principal (*Call To Action*) "Agendar Consultoría".
2. **Hero de Alto Impacto**: Propuesta de valor corporativa con distintivo de calidad (99.9% Uptime SLA, Lakehouse 3 Capas, &lt; 2h SLA Comercial) y visor dinámico de la pila arquitectónica.
3. **Diferencial Competitivo (Value Highlights)**: Compromisos de valor de Statsfirm Co. (Inmutabilidad de datos, Squad as a Service, Gobierno DAMA-BOK y Orquestación BPMN 2.0).
4. **Catálogo Oficial de Servicios (Documento 05)**:
   - *Línea 01*: **Data Intelligence & Engineering** (Lakehouse 3 Capas, Kafka Streaming, Delta Lake, Spark, dbt, Data Mesh).
   - *Línea 02*: **Business Intelligence & Decision Analytics** (Capa 3 Semántica Gold, Dashboards Dark Mode Power BI/Looker, KPI Trees).
   - *Línea 03*: **AI Engineering & Applied Data Science** (Forecasting estocástico, optimización combinatoria, agentes de IA industriales, MLOps).
   - *Línea 04*: **Software & Cloud Engineering** (Microservicios Go/Node/Python, APIs GraphQL/REST, Kubernetes AWS/Azure/GCP, CI/CD).
   - *Línea 05*: **Process Engineering & BPM** (Modelado formal BPMN 2.0 en Camunda 7/8, Process Mining, TOGAF ADM).
5. **Arquitectura Canónica de Tres Capas**: Infografía técnica interactiva que detalla los contratos y propósitos de las capas **Bronze** (Raw Inmutable), **Silver** (Curaduría y dbt) y **Gold** (Semántica y Data Marts).
6. **Metodología Propietaria STF**: Cronograma secuencial de 4 fases (Diagnóstico, Fundaciones MVP, Escalamiento y MLOps/Gobierno Continuo).
7. **Innova Lab SaaS Products**: Exposición de los productos de software empaquetado (*Statsfirm DataWeave*, *Statsfirm ProcessMatrix*, *Statsfirm MetricsEngine*).
8. **Cotizador Interactivo de Proyecto**: Calculadora dinámica en tiempo real que permite al cliente seleccionar servicios, volumen de datos mensual (TB) y urgencia, generando rangos de inversión CAPEX en USD, cronograma estimado en semanas y squad sugerido. Incluye botón directo para sincronizar los parámetros calculados al formulario comercial.
9. **Formulario Oficial de Captación Comercial (BPMN-01)**:
   - Formulario web compatible con `form_01_lead_comercial.form` de Camunda.
   - Campos: Empresa, Contacto, Correo Corporativo, Teléfono, Sector, Servicios de Interés, Volumen TB, Presupuesto USD, Urgencia y Descripción del Reto.
   - Generación automática de Ticket Comercial (`LEAD-2026-XXXX`), cálculo de Score y ventana garantizada de SLA.
10. **Canales Directos & Garantías**: Acceso a correo corporativo (`contacto@statsfirm.com`), WhatsApp Business, oficinas y compromiso de SLA de 2 horas.
11. **Footer Corporativo**: Información institucional, accesos rápidos a líneas de servicio y cláusula de cumplimiento regulatorio ISO/IEC 25010 y DAMA-BOK.

---

## 5. Endpoints REST de la Plataforma

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/services` | Retorna el catálogo completo de líneas de servicio, productos SaaS y modelos de squad |
| `GET` | `/api/services/:id` | Retorna los detalles y capacidades de una línea de servicio específica |
| `POST` | `/api/quote` | Recibe parámetros de proyecto (servicios, volumen TB, urgencia) y calcula inversión y plazos |
| `POST` | `/api/contact` | Procesa la recepción del lead bajo BPMN-01, calcula scoring y emite ticket formal |
| `GET` | `/api/leads` | Auditoría de leads registrados y estado de calificación ARB |

---

## 6. Aseguramiento de Calidad y Pruebas

Para ejecutar la batería automatizada de pruebas sobre los endpoints del servidor:
```bash
python ../scratch/test_commercial_endpoints.py
```

Resultados verificados:
- `GET /`: Código 200 (HTML renderizado y cargado correctamente).
- `GET /api/services`: Código 200 (5 líneas de servicio cargadas).
- `POST /api/quote`: Código 200 (Cálculo paramétrico de CAPEX y semanas).
- `POST /api/contact`: Código 201 (Ticket generado y calificado exitosamente).
