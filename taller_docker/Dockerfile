# Dockerfile — FinTech Nova API (contenido completo)
# ════════════════════════════════════════════════════════════
# Dockerfile para la API FinTech Nova
# Autor: Equipo FinTech Nova
# ════════════════════════════════════════════════════════════
# ── INSTRUCCIÓN 1: Imagen base ──────────────────────────────
FROM python:3.11-slim
# ── INSTRUCCIÓN 2: Metadatos (opcional pero recomendado) ─────
LABEL maintainer="equipo@fintechnova.com"
LABEL version="1.0.0"
LABEL description="API de evaluación crediticia FinTech Nova"
# ── INSTRUCCIÓN 3: Variables de entorno ──────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# ── INSTRUCCIÓN 4: Directorio de trabajo ─────────────────────
WORKDIR /app
# ── INSTRUCCIÓN 5: Usuario no-root (seguridad) ───────────────
RUN addgroup --system appgroup && \
 adduser --system --ingroup appgroup appuser
# ── INSTRUCCIÓN 6: Instalar dependencias del sistema ─────────
RUN apt-get update && apt-get install -y \
 curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
# ── INSTRUCCIÓN 7: Copiar e instalar dependencias Python ──────
# Copiamos SOLO requirements.txt primero (optimización de caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# ── INSTRUCCIÓN 8: Copiar el código de la aplicación ─────────
COPY . .
# ── INSTRUCCIÓN 9: Permisos del usuario ──────────────────────
RUN chown -R appuser:appgroup /app
USER appuser
# ── INSTRUCCIÓN 10: Puerto que expone la API ─────────────────
EXPOSE 8000
# ── INSTRUCCIÓN 11: Health check ─────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
 CMD curl -f http://localhost:8000/health || exit 1
# ── INSTRUCCIÓN 12: Comando de inicio ───────────────────────
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]