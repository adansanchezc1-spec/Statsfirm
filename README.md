# Ecosistema Tecnológico — Statsfirm Co. & Agro Stat & Tech Co.

Repositorio centralizado (**Monorepo Modular Federado**) del holding tecnológico compuesto por **Statsfirm Co.** y su subsidiaria especializada **Agro Stat & Tech Co.**

---

## 1. Arquitectura del Ecosistema

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STATSFIRM ECOSYSTEM (MONOREPO)                     │
├──────────────────────────────────────┬──────────────────────────────────────┤
│            STATSFIRM CO.             │       AGRO STAT & TECH CO.           │
│   (Ingeniería Corporativa B2B)       │   (Transformación Agroempresarial)   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • 01. Centralización & Lakehouse     │ • 01. App Móvil Offline-First        │
│ • 02. Tableros Ejecutivos Real-Time  │ • 02. BI & Control Gerencial Agro    │
│ • 03. Modelos Predictivos e IA       │ • 03. Curaduría Lakehouse & EUDR     │
│ • 04. Portales & Nube Resiliente     │ • 04. Procesos BPMN & Farm FinOps    │
│ • 05. Automatización BPMN 2.0        │                                      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ Directorio: Statsfirm/               │ Directorio: AgroStats AndTech/       │
│ • app/ (Backend Express BFF & Web)   │ • Agrostat_app/ (App Móvil)          │
│ • docs_landing_page/                 │ • docs_landing_page/                 │
│   - Statsfirm/ (11 docs .docx)       │   - AgroStats/ (14 docs .docx)       │
│   - docs/05-services/ (5 servicios)  │   - docs/05-services/ (4 servicios)  │
│   - bpmn/ (Camunda 7/8 & 10 forms)   │   - bpmn/ (Procesos analíticos)      │
│   - agents/ (Agentes Python)         │   - agents/ (Bioestadística & SPC)   │
│   - index.html (Portal oficial)      │   - index.html (Portal oficial)      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. Puesta en Marcha Rápida

### Ejecución de Statsfirm Co. (Servidor Web & API BFF)
Ejecutar el script en la raíz del repositorio:
```bash
iniciar.bat
```
O manualmente:
```bash
cd Statsfirm/app
npm install
node server.js
```
Acceder en el navegador: [http://localhost:3000](http://localhost:3000)

### Visualización de Agro Stat & Tech Co.
Abrir directamente en el navegador:
```bash
AgroStats AndTech/docs_landing_page/index.html
```

---

## 3. Control de Versiones con Git

Este repositorio implementa la política de **Monorepo Modular Federado**:
- **Despliegues Autónomos**: Configurados mediante **Path-Filtering** en `.github/workflows/` (`statsfirm-ci.yml` y `agrostats-ci.yml`).
- **Guía de Ramas y Commits**: Consultar [`CONTRIBUTING.md`](file:///c:/Users/ADAN/OneDrive/Documentos/Statsfirm/CONTRIBUTING.md).
- **Registro de Decisión Arquitectónica**: Consultar el documento formal [`ADR-001: Estrategia Monorepo`](file:///c:/Users/ADAN/OneDrive/Documentos/Statsfirm/Statsfirm/docs_landing_page/docs/02-architecture/ADR/ADR-001-monorepo-control-versiones.md).

---

## 4. Normativa y Estándares Aplicados

- **SWEBOK** (Software Engineering Body of Knowledge).
- **DAMA-BOK** (Data Management Body of Knowledge).
- **ISO/IEC 25010** (Calidad de Producto de Software).
- **ISO 19510** (BPMN 2.0 Business Process Model and Notation).
- **Clean Code & Principios SOLID**.
