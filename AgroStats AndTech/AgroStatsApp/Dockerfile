# ==============================================================================
# AgroData Intelligence Platform Enterprise v1.0 — Production Dockerfile
# Multi-stage secure build / Non-root user / Python 3.11+
# ==============================================================================

# Build Stage
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Stage
FROM python:3.11-slim-bookworm AS final

WORKDIR /app

# Non-root user for security
RUN groupadd -r agrouser && useradd -r -g agrouser -u 1001 agrouser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/agrouser/.local
ENV PATH=/home/agrouser/.local/bin:$PATH
ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# Copy application source
COPY --chown=agrouser:agrouser src/ ./src/
COPY --chown=agrouser:agrouser data/ ./data/
COPY --chown=agrouser:agrouser sql/ ./sql/
COPY --chown=agrouser:agrouser web/ ./web/

USER agrouser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "src.agrostats.adapters.driving.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
