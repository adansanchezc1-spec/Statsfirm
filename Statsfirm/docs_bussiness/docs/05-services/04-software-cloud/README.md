# Servicio 04: Portales y Nube de Alta Disponibilidad (Software & Cloud Engineering)

**Código de Servicio**: STF-SRV-04  
**Línea de Portafolio**: 04 / Software & Nube  
**Normativa Aplicable**: SWEBOK Cap. 1, 2 & 3, ISO/IEC 25010 (Mantenibilidad, Portabilidad, Seguridad), Principios SOLID y Clean Architecture.  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico*), Sección `#servicios` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones?
Diseña, construye y moderniza aplicaciones web empresariales, portales de autoservicio para clientes y microservicios en la nube con arquitectura de grado bancario, garantizando alta velocidad de respuesta, cero caídas operativas en fechas pico y facturación de infraestructura controlada y predecible (FinOps).

### Metáfora Operativa
Es como construir un rascacielos corporativo con cimientos sismorresistentes y puertas de alta seguridad: sin importar si ingresan diez personas o decenas de miles de clientes en una misma hora pico, la estructura se mantiene sólida, silenciosa y sin vibraciones.

### Dolor de Negocio Resuelto
- **Caídas en Momentos Críticos**: Evita la pérdida de ventas e imagen de marca causada por sistemas que colapsan durante cierres comerciales o quincenas.
- **Plataformas Lentas y Poco Amigables**: Desarrolla interfaces rápidas y reactivas que incrementan la adopción de usuarios y la conversión de clientes.
- **Costos Desbordados en la Nube**: Audita y redimensiona recursos en AWS, Azure o Google Cloud para pagar únicamente por la capacidad real utilizada.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Arquitectura Hexagonal (Ports & Adapters)** | Aislamiento estricto de lógica de dominio respecto a frameworks y bases de datos. | Código limpio, testeable y modular con cobertura > 85%. |
| **Microservicios Resilientes & APIs REST/GraphQL** | Servicios independientes contenerizados con tolerancia a fallos y circuit breakers. | APIs documentadas bajo OpenAPI 3.0 / Swagger. |
| **Infraestructura como Código (IaC)** | Automatización de aprovisionamiento de servidores, redes y bases de datos con Terraform. | Repositorio de Terraform / Helm charts para despliegue automatizado. |
| **Ciberseguridad y Cero Confianza** | Autenticación robusta OAuth 2.0 / OpenID Connect, cifrado en tránsito (TLS 1.3) y en reposo (AES-256). | Certificación de cumplimiento OWASP Top 10 y auditoría de seguridad. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Backend         │ Node.js (TypeScript), Go, Python (FastAPI)│
│ Frontend        │ React, Next.js, Vanilla JS / Modern CSS   │
│ Contenedores    │ Docker, Kubernetes (EKS / GKE / AKS)      │
│ Nube & FinOps   │ AWS, Azure, Google Cloud Platform, Terraform│
│ CI/CD Pipelines │ GitHub Actions, GitLab CI, ArgoCD         │
│ Observabilidad  │ Prometheus, Grafana, OpenTelemetry, Sentry│
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Disponibilidad Contractual (SLA)**: 99.9% Uptime mensual.
- **Tiempo de Respuesta (Latencia P95)**: < 120ms en endpoints de servicios core.
- **Tiempo Medio de Recuperación (MTTR)**: < 15 minutos ante contingencias operativas mediante auto-healing en Kubernetes.
