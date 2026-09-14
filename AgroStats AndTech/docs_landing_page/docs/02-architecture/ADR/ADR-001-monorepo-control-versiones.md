# ADR-001: Estrategia de Control de Versiones Monorepo Modular Federado

**Fecha**: 2026-09-14  
**Estado**: Aceptado  
**Fase PDCO**: PLAN → DESIGN  
**Skill**: `02-architecture`  
**Autores**: Equipo de Arquitectura de Software & Ciencia de Datos (Statsfirm Co. & Agro Stat & Tech Co.)  

---

## 1. Contexto y Problema

Statsfirm Co. opera como empresa matriz de ingeniería de datos, inteligencia artificial, software bancario y optimización de procesos (BPMN 2.0). Agro Stat & Tech Co. (AgroStats) es una subsidiaria tecnológica especializada en el sector agroempresarial y agroindustrial (aplicaciones móviles Offline-First, bioestadística, linaje EUDR y Farm FinOps).

Aunque ambas empresas atienden segmentos comerciales diferentes y ofertan carteras de productos distintas, comparten:
- Fundamentos metodológicos y de calidad del software (SWEBOK, DAMA-BOK, ISO/IEC 25010, Clean Code, SOLID).
- Sistema de diseño y directrices de marca.
- Especificaciones de arquitectura de datos (Lakehouse Medallion).
- Documentación base de gobierno corporativo (Documentos 01 al 10).

Se requería definir la arquitectura de control de versiones con Git que evitara la desincronización metodológica sin acoplar los despliegues ni los ciclos de entrega de ambas firmas.

---

## 2. Decisión

Se decide implementar un **Monorepo Modular Federado** alojado en un único repositorio Git corporativo con las siguientes directrices técnicas:

1. **Aislamiento por Carpetas de Nivel Superior**:
   - `Statsfirm/`: Aplicación Express BFF, landing page, agentes y documentación de los 5 servicios corporativos.
   - `AgroStats AndTech/`: Aplicación móvil, portal agronómico, agentes bioestadísticos y documentación de los 4 servicios agropecuarios.
2. **Desacoplamiento de Despliegues en CI/CD**:
   - Uso obligatorio de **Path Filtering** en GitHub Actions (`statsfirm-ci.yml` y `agrostats-ci.yml`).
   - Un cambio en AgroStats no activa pruebas ni despliegues en Statsfirm, y viceversa.
3. **Estrategia de Ramas**:
   - `main`: Producción estable.
   - `develop`: Integración continua.
   - Ramas de características prefijadas: `feat/statsfirm/...` y `feat/agrostats/...`.
4. **Versionado Semántico Independiente (SemVer con Namespace)**:
   - Tags Git con prefijo de producto: `statsfirm@vX.Y.Z` y `agrostats@vX.Y.Z`.
5. **Gobernanza de Commits (Conventional Commits)**:
   - Formato: `<tipo>(<scope>): <descripción>`, donde `<scope>` es `statsfirm`, `agrostats`, `holding` o `governance`.

---

## 3. Alternativas Descartadas

| Alternativa | Razón del Descarte |
|---|---|
| **Multi-Repo (Polyrepo)** | Fragmenta la gobernanza; duplicaría los esfuerzos de mantenimiento de CI/CD y desincronizaría las directrices metodológicas y contratos de datos comunes. |
| **Git Submodules** | Introduce complejidad innecesaria en sincronización de punteros Git (*detached HEAD*, fricción para desarrolladores). Antipatrón de complejidad accidental. |

---

## 4. Consecuencias y Trade-offs

### Positivas
- **Única Fuente de Verdad**: Todo el conocimiento, contratos de datos y especificaciones de procesos residen en un solo ecosistema trazable.
- **Despliegues 100% Independientes**: Cada producto entrega valor a su propio ritmo sin dependencias cruzadas en tiempo de ejecución.
- **Auditoría Centralizada**: Simplifica la trazabilidad ISO/IEC 25010 y el cumplimiento DAMA-BOK.

### Negativas / Mitigaciones
- **Tamaño del Repositorio**: El repositorio contiene ambos ecosistemas.  
  *Mitigación*: Se excluyen binarios pesados no versionables mediante `.gitignore` y se usa shallow clone (`fetch-depth: 1`) en CI/CD.
