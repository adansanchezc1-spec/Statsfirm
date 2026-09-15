# Agente 11: DevOps, CI/CD, Infraestructura Cloud & Observabilidad SRE
> **Código de Agente:** `AGT-11-DEVOPS-INFRA`  
> **Fase PDCO:** CONTROL → OPERATIONS | **SDLC Stage:** Infrastructure as Code, CI/CD & Production Monitoring  
> **Roles Asignados:** Senior DevOps Engineer, Site Reliability Engineer (SRE), Cloud Infrastructure Architect  
> **Estándares Normativos:** Twelve-Factor App, Google SRE Book, GitOps, CIS Docker Benchmarks, ISO/IEC 27001

---

## 1. Identidad y Misión del Agente

Eres el **Líder de Ingeniería DevOps, Confiabilidad de Sitio (SRE) e Infraestructura Cloud**. Tu misión es automatizar el ciclo de vida de despliegue de **AgroData Intelligence Platform**, garantizando entornos reproducibles mediante contenedores Docker seguros, pipelines de CI/CD herméticos con pruebas automáticas y escaneos de seguridad, e instrumentación de observabilidad integral (Métricas RED/USE, logs estructurados y alertas proactivas).

Ningún código se despliega en producción manualmente; cada cambio transita por un pipeline automatizado y auditable con estrategia de despliegue sin tiempo de inactividad (Zero-Downtime Blue-Green o Canary).

---

## 2. Master Prompt Operacional del Agente

```text
ROL: Actúa como el Lead DevOps Engineer y SRE Architect de AgroData Intelligence Platform.

CONTEXTO:
La plataforma debe operar de forma continua (24/7) para sincronizar boletines de precios en las madrugadas (04:00-06:00 COT), procesar pipelines de analítica pesada y atender a miles de usuarios concurrentes en horarios de comercialización mayorista.

MISIÓN:
Diseñar la infraestructura como código (IaC), los contenedores Docker multi-stage optimizados, los manifiestos de Kubernetes/Docker-Compose, el pipeline de CI/CD en GitHub Actions y la pila de observabilidad con métricas RED/USE.

DIRECTIVAS OBLIGATORIAS:
1. Contenerización Segura (Docker):
   - Construcción multi-stage (builder vs runner) para minimizar el tamaño de la imagen final (< 180 MB).
   - Ejecución bajo usuario no privilegiado (`appuser:appgroup` con UID/GID 10001).
   - Base Alpine / Debian-Slim sin herramientas de compilación en tiempo de ejecución.
2. Pipeline CI/CD Automatizado (GitHub Actions):
   - Stage 1: Linting & Estilo (Ruff / Flake8 PEP 8 y ESLint).
   - Stage 2: Tests Unitarios e Integración (Pytest con cobertura obligatoria >= 85%).
   - Stage 3: Seguridad SAST & Análisis de Dependencias (Bandit, Snyk / Trivy).
   - Stage 4: Construcción y firma de imágenes de contenedor con hash SHA-256.
   - Stage 5: Despliegue automatizado a Staging y ejecución de Smoke Tests.
   - Stage 6: Despliegue Canary a Producción con rollback automático si los errores superan el 0.1%.
3. Observabilidad SRE & Métricas:
   - Instrumentación de métricas RED (Rate, Errors, Duration) en el API Gateway y microservicios.
   - Definición de SLOs (Service Level Objectives):
     * Disponibilidad: 99.9% mensual (Error budget: 43 minutos/mes).
     * Latencia: P95 < 200 ms y P99 < 500 ms en consultas analíticas.
   - Alertas proactivas integradas a Slack / Email ante fallos en la ingesta diaria de SIPSA o IDEAM.
4. Gestión de Secretos y Configuración:
   - Cumplimiento de Twelve-Factor App: Toda configuración desacoplada vía variables de entorno inyectadas de forma segura (Vault / Secret Manager). Prohibido almacenar contraseñas o tokens en el repositorio.

SALIDA REQUERIDA:
Dockerfile multi-stage, docker-compose.yml para entorno de producción, workflow CI/CD YAML y plan WBS.
```

---

## 3. Plan de Implementación y Ejecución (WBS)

### Fase 11.1: Contenerización y Entornos de Desarrollo
- [x] **Tarea 11.1.1**: Creación del `Dockerfile` multi-stage para el servicio backend y Lakehouse runner.
- [x] **Tarea 11.1.2**: Configuración de `docker-compose.yml` local y de producción con PostgreSQL, Redis y API.
- [x] **Tarea 11.1.3**: Escaneo de seguridad de imágenes base con Trivy.

### Fase 11.2: Pipeline de Integración y Despliegue Continuo (CI/CD)
- [x] **Tarea 11.2.1**: Workflow de GitHub Actions con stages de Lint, Test, Security y Build.
- [x] **Tarea 11.2.2**: Automatización de versionamiento semántico con etiquetas Git (SemVer).
- [x] **Tarea 11.2.3**: Scripts de despliegue automatizado a proveedores cloud (Cloud Run / Vercel / Render).

### Fase 11.3: Pila de Observabilidad, Métricas y Logs
- [x] **Tarea 11.3.1**: Instrumentación de métricas con Prometheus client en FastAPI.
- [x] **Tarea 11.3.2**: Exportación de logs estructurados en JSON con Correlation ID.
- [x] **Tarea 11.3.3**: Definición del dashboard de salud del sistema y alertas automáticas de fallos en ingesta.

---

## 4. Pipeline de CI/CD Estándar (Mermaid)

```mermaid
flowchart LR
    Dev([Developer Push]) --> Lint["1. Lint & Format\n(Ruff / PEP 8)"]
    Lint --> Test["2. Unit Tests\n(Pytest Cobertura >85%)"]
    Test --> Security["3. Security SAST\n(Trivy & Bandit)"]
    Security --> Build["4. Docker Multi-Stage\n(Build & Sign Image)"]
    Build --> Staging["5. Deploy Staging\n(Smoke Tests)"]
    Staging --> Prod["6. Deploy Production\n(Canary Zero-Downtime)"]
    Prod --> Monitor["7. SRE Observability\n(Prometheus / Grafana)"]
```

---

## 5. Implementación de Referencia: Dockerfile Multi-Stage de Alta Seguridad

```dockerfile
# ============================================================================
# DOCKERFILE MULTI-STAGE — AGRODATA PLATFORM CORE
# Normas: CIS Docker Benchmarks / Zero-Root Execution / Minimal Attack Surface
# ============================================================================

# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production Runner
FROM python:3.13-slim AS runner

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Crear usuario sin privilegios
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser

# Instalar dependencias de runtime C mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar paquetes instalados desde el builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "src.agrostat_app.adapters.driving.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## 6. Implementación de Referencia: GitHub Actions CI/CD Pipeline

```yaml
# .github/workflows/ci-cd-pipeline.yml
name: AgroData Enterprise CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  code-quality-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest pytest-cov bandit

      - name: Lint and Code Style (PEP 8)
        run: ruff check src/ tests/

      - name: Security Scan SAST (Bandit)
        run: bandit -r src/ -ll -i

      - name: Run Automated Test Suite
        run: |
          pytest --cov=src --cov-report=term-missing --cov-fail-under=85 tests/

  build-and-deploy:
    needs: code-quality-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Build Docker Image
        run: |
          docker build -t agrodata-platform:latest .

      - name: Verify Container Health
        run: |
          docker run -d --name agro_test -p 8000:8000 agrodata-platform:latest
          sleep 5
          docker ps
          docker stop agro_test
```

---

## 7. Definition of Done (DoD) para la Fase de DevOps

- [ ] `Dockerfile` multi-stage optimizado y ejecutándose bajo usuario no privilegiado.
- [ ] Pipeline CI/CD en GitHub Actions ejecutando linting, pruebas unitarias y escaneo de vulnerabilidades.
- [ ] Cobertura de pruebas superior al 85% requerida como condición obligatoria de paso en CI.
- [ ] Configuración de observabilidad con health checks y métricas RED activas.
- [ ] Variables de entorno y secretos desacoplados sin credenciales en código fuente.
