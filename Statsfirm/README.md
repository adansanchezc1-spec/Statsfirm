# Statsfirm Co. — Plataforma Corporativa & Ecosistema de Ingeniería

```
  ███████╗████████╗ █████╗ ████████╗███████╗███████╗██╗██████╗ ███╗   ███╗     ██████╗ ██████╗ 
  ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝██╔════╝██║██╔══██╗████╗ ████║    ██╔════╝██╔═══██╗
  ███████╗   ██║   ███████║   ██║   ███████╗█████╗  ██║██████╔╝██╔████╔██║    ██║     ██║   ██║
  ╚════██║   ██║   ██╔══██║   ██║   ╚════██║██╔══╝  ██║██╔══██╗██║╚██╔╝██║    ██║     ██║   ██║
  ███████║   ██║   ██║  ██║   ██║   ███████║██║     ██║██║  ██║██║ ╚═╝ ██║    ╚██████╗╚██████╔╝
  ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ 
```

**Statsfirm Co.** es una firma de ingeniería tecnológica, arquitectura de software, ingeniería de datos (Lakehouse/BI), Control Estadístico de Procesos (SPC) y modelado BPMN 2.0. Diseñamos soluciones empresariales de alto rendimiento regidas por los estándares internacionales **SWEBOK, DAMA-BOK, IEEE 830, ISO/IEC 25010 y Clean Code**.

---

## 🏛️ Estructura del Repositorio

```
Statsfirm/
├── docs_bussiness/              # Repositorio documental, arquitectura empresarial y diseño BPMN
│   ├── Statsfirm/               # Documentos normativos y manuales de marca (DOCX)
│   ├── docs/                    # Especificaciones en Markdown (02-architecture, 05-services, 08-bpmn)
│   ├── bpmn/                    # Modelos de procesos BPMN 2.0 y formularios Camunda
│   ├── agents/                  # Sistema multi-agente de automatización y orquestación
│   └── metadata.json            # Trazabilidad PDCO del proyecto
│
├── landing_page/                # Aplicación web corporativa y portal de servicios
│   ├── public/                  # Assets, hojas de estilo (CSS) y lógica de frontend (JS)
│   ├── routes/                  # Endpoints de API REST, telemetría y enrutamiento
│   ├── server.js                # Servidor Express.js / Node.js
│   ├── Dockerfile               # Contenedor de producción
│   └── docker-compose.yml       # Orquestación de servicios
│
├── network/                     # Plan estratégico de redes sociales, Meta Business & Facebook
│   ├── 01_configuracion_identidad_pagina.md
│   ├── 02_secciones_servicios_y_catalogo.md
│   ├── 03_estrategia_contenido_formatos_fb.md
│   ├── 04_automatizacion_messenger_lead_bot.md
│   ├── 05_checklist_lanzamiento_y_meta_ads.md
│   ├── README.md
│   └── metadata.json
│
├── .gitignore                   # Exclusiones de dependencias, entornos y temporales
└── README.md                    # Documento principal del repositorio
```

---

## 💼 Portafolio de Servicios

1. **Curaduría de Datos & Arquitectura Lakehouse**: Capas Medallion (Bronze, Silver, Gold), Data Contracts (DAMA-BOK), Delta Lake, DuckDB y dbt.
2. **Business Intelligence & Control Estadístico (SPC)**: Dashboards ejecutivos en tiempo real con monitoreo de límites Shewhart ($\bar{X} \pm 3\sigma$) e índices $C_{pk}$.
3. **Machine Learning & Analítica Predictiva**: Series de tiempo, pronóstico de demanda y modelos estocásticos.
4. **Ingeniería de Software & Cloud**: Arquitectura Hexagonal, microservicios, APIs REST y aplicaciones móviles *Offline-First* con SQLite y CRDTs.
5. **Ingeniería de Procesos BPMN 2.0 & FinOps**: Mapeo, simulación y eliminación de tiempos muertos con Camunda 7/8.

---

## 🚀 Despliegue Local de la Landing Page

### Prerrequisitos
- **Node.js**: v18.0.0 o superior
- **npm**: v9.0.0 o superior

### Ejecución
```bash
# Navegar al directorio de la aplicación
cd landing_page

# Instalar dependencias
npm install

# Iniciar servidor en modo desarrollo
npm start
# O ejecutar el script interactivo
iniciar.bat
```

La aplicación estará disponible en `http://localhost:3000`.

---

## 🔒 Estándares de Calidad y Gobierno

- **Clean Code & SOLID**: Código modular, desacoplado y comprobable.
- **Pruebas Unitarias & Cobertura**: Cobertura objetivo $\ge 80\%$.
- **Control de Versiones**: Convenciones de *Conventional Commits* (`feat:`, `fix:`, `docs:`, `refactor:`).

---

## 📬 Contacto Corporativo

- **Organización**: Statsfirm Co.
- **Email Oficial**: `statsfirmco@gmail.com`
- **GitHub**: [`@statsfirmco-bussiness-account`](https://github.com/statsfirmco-bussiness-account)
- **Licencia**: Propiedad exclusiva de Statsfirm Co. Todos los derechos reservados.
