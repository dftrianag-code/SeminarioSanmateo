# Imagen base
FROM python:3.11-slim

# Metadatos
LABEL maintainer="fintech-nova@empresa.com"
LABEL version="1.0.0"
LABEL description="API de evaluación crediticia FinTech Nova"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Crear usuario no-root
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Instalar curl para HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Asignar propietario
RUN chown -R appuser:appgroup /app

# Usuario no root
USER appuser

# Puerto de la aplicación
EXPOSE 8000

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

# Ejecutar FastAPI
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]