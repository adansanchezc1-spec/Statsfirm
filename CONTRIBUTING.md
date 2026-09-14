# Guía de Contribución y Control de Versiones — Statsfirm Ecosystem

**Holding Tecnológico**: Statsfirm Co. & Agro Stat & Tech Co.  
**Arquitectura de Repositorio**: Monorepo Modular Federado  
**Estándar de Control de Versiones**: SWEBOK Cap. 7 & Conventional Commits 1.0.0  

---

## 1. Modelo de Ramas (Branching Model)

El repositorio opera bajo un modelo **GitFlow Simplificado / Trunk-Based con Prefijos**:

```
main (Producción estable)
  ▲
  │ (Pull Request aprobada)
develop (Integración continua)
  ▲
  ├─ feat/statsfirm/<descripcion-corta>    ← Para desarrollo en Statsfirm Co.
  ├─ feat/agrostats/<descripcion-corta>    ← Para desarrollo en Agro Stat & Tech Co.
  ├─ fix/statsfirm/<issue-id>
  ├─ fix/agrostats/<issue-id>
  └─ chore/governance/<mejora>             ← Para cambios metodológicos o DAMA-BOK
```

### Reglas de Creación de Ramas
1. Toda nueva funcionalidad parte de la rama `develop`.
2. El nombre de la rama **debe** incluir el scope del producto:
   - Correcto: `feat/statsfirm/cotizador-cop`, `feat/agrostats/sincronizacion-sqlite`
   - Incorrecto: `feature-nueva`, `cambios-juan`

---

## 2. Convención de Commits (Conventional Commits)

Cada commit debe seguir la estructura:
```
<tipo>(<scope>): <descripción imperativa en minúsculas>

[cuerpo opcional detallando el por qué]

[pie de commit opcional con referencias a issues]
```

### Tipos Permitidos
- `feat`: Nueva funcionalidad para el usuario/cliente.
- `fix`: Corrección de un error o bug.
- `docs`: Modificaciones exclusivas de documentación técnica.
- `refactor`: Refactorización de código sin cambio de comportamiento.
- `test`: Añadir o corregir pruebas unitarias/integración.
- `chore`: Tareas de mantenimiento, actualización de dependencias o gobernanza.

### Scopes Obligatorios
- `statsfirm`: Afecta a la plataforma web, BFF o servicios de Statsfirm Co.
- `agrostats`: Afecta a la aplicación móvil o servicios de Agro Stat & Tech Co.
- `holding`: Afecta a la raíz o a directrices comunes de ambas empresas.
- `bpmn`: Cambios en modelos Camunda o esquemas de formularios.
- `lakehouse`: Cambios en tuberías de datos o contratos dbt/Delta Lake.

### Ejemplos Válidos
```bash
git commit -m "feat(statsfirm): agregar visualización de 5 soluciones empresariales en bento grid"
git commit -m "fix(statsfirm): corregir resolucion multirruta de formularios camunda en bpmn.js"
git commit -m "feat(agrostats): implementar persistencia local offline-first con SQLite"
git commit -m "docs(agrostats): agregar especificacion de servicio 03 curaduria lakehouse"
git commit -m "chore(holding): configurar pipeline de CI con path filtering para agrostats"
```

---

## 3. Versionado Semántico y Tags de Release

Dado que Statsfirm y AgroStats tienen ciclos de entrega independientes, los tags Git se crean con el prefijo del producto:

```bash
# Release para Statsfirm Co.
git tag -a statsfirm@v2.2.0 -m "Release v2.2.0: Portafolio de 5 servicios y docs_landing_page estructurado"

# Release para Agro Stat & Tech Co.
git tag -a agrostats@v2.1.0 -m "Release v2.1.0: Modularización de 4 servicios agroempresariales"

# Enviar tags al remoto
git push origin --tags
```

---

## 4. Flujo de Trabajo para Pull Requests (PR)

1. Crear rama desde `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feat/statsfirm/mi-funcionalidad
   ```
2. Realizar cambios y verificar localmente:
   ```bash
   # Si trabajas en Statsfirm:
   cd Statsfirm/app && npm test
   # Si trabajas en AgroStats:
   cd "AgroStats AndTech/docs_landing_page/agents" && python test_runner.py
   ```
3. Realizar commits siguiendo la convención:
   ```bash
   git add .
   git commit -m "feat(statsfirm): ..."
   ```
4. Abrir Pull Request hacia `develop`.
5. El pipeline de GitHub Actions ejecutará automáticamente **únicamente** los tests del producto modificado gracias al filtro por rutas.
