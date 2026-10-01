# Servicio 01: App Móvil de Gestión Operativa (Offline-First)

**Código de Servicio**: AGRO-SRV-01  
**Línea de Portafolio**: 01 / Operaciones & Campo  
**Normativa Aplicable**: SWEBOK Cap. 2 & 3, ISO/IEC 25010 (Portabilidad y Fiabilidad), Principios Offline-First & Local-First Software.  
**Trazabilidad**: Documento 05 (*Catálogo de Servicios y Portafolio Tecnológico Agroindustrial*), Documento 10 (*App del Productor y Consola Agro*), Sección `#que-ofrecemos` de la Landing Page.

---

## 1. Visión General y Propósito del Negocio

### ¿Qué es para tomadores de decisiones agroempresariales?
Es la solución de software móvil diseñada específicamente para el entorno rural y predial disperso, que digitaliza en tiempo real la captura de labores de campo, asignación de jornales, control de cuadrillas y recepción de cosechas en centros de acopio, funcionando con **autonomía absoluta sin depender de señal celular o internet**.

### Metáfora Operativa
Es como entregar a cada mayordomo, supervisor de cuadrilla y pesador de báscula una bitácora digital blindada e inteligente que nunca se borra ni se pierde: registra las pesadas y jornales en el lote más remoto de la cordillera y, en cuanto la camioneta o el operador se acerca a la oficina con WiFi o señal, todos los datos viajan solos y se consolidan en el sistema central en segundos.

### Dolor de Negocio Resuelto
- **Pérdida y Suciedad de Planillas en Papel**: Elimina las libretas de campo arrugadas, mojadas o manchadas que tardaban días en llegar a la administración central.
- **Descontrol de Mano de Obra y Rendimientos**: Provee auditoría exacta de jornales trabajados, kilos recolectados por trabajador y costos devengados por lote.
- **Demoras en Recepción y Despachos**: Agiliza el pesaje y registro de calidad en centros de acopio sin cuellos de botella.

---

## 2. Capacidades y Entregables

| Capacidad | Detalle de Implementación | Entregable Concreto |
|---|---|---|
| **Arquitectura 100% Offline-First** | Base de datos local transaccional (SQLite / WatermelonDB / PouchDB) con cola de mutaciones inmutable. | Aplicación móvil Android / iOS para dispositivos robustos. |
| **Sincronización Bidireccional Segura** | Protocolo de sincronización incremental por bloques con resolución determinística de conflictos (CRDTs). | Mecanismo automático de push/pull al detectar conectividad. |
| **Control de Cuadrillas & Jornales** | Registro biométrico/código QR de colaboradores, asignación de tareas agronómicas y rendimientos unitarios. | Módulo de pre-liquidación de mano de obra y rendimientos. |
| **Trazabilidad de Lote y Predio** | Georreferenciación estricta de cada labor y recolección para trazabilidad de exportación. | Registros geolocalizados listos para auditorías de calidad. |

---

## 3. Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────┬───────────────────────────────────────────┤
│ Frontend Móvil  │ Flutter / React Native, TypeScript        │
│ Base Local      │ SQLite, WatermelonDB, SQLCipher           │
│ Sincronización  │ Background Fetch, Protocolo CRDT / REST   │
│ Backend BFF     │ Node.js / Python FastAPI, Webhooks        │
│ Seguridad       │ Encriptación local AES-256, mTLS          │
│ Hardware        │ Smartphones Android estándar & rugerizados│
└─────────────────┴───────────────────────────────────────────┘
```

---

## 4. Métricas de Impacto y SLAs

- **Autonomía Operativa**: 100% operativo sin internet por días continuos; cero pérdida de registros transaccionales.
- **Tiempo de Sincronización**: < 15 segundos al restablecer enlace de datos para lotes de 1,000 transacciones.
- **Reducción de Tiempo en Pre-Nómina**: De 4 días a 15 minutos en el cálculo y liquidación de cuadrillas.
