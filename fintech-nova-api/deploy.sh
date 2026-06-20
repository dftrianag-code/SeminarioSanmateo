#!/bin/bash

echo "Iniciando despliegue..."

# Verificar Docker
docker --version > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "ERROR: Docker no está instalado."
    exit 1
fi

# Verificar requirements.txt
if [ ! -f requirements.txt ]; then
    echo "ERROR: requirements.txt no existe."
    exit 1
fi

# Crear versión
VERSION=$(date +%Y%m%d)

echo "Construyendo imagen..."
docker build -t fintech-nova:$VERSION .

# Detener contenedor anterior
docker stop fintech-api 2>/dev/null
docker rm fintech-api 2>/dev/null

# Levantar contenedor nuevo
docker run -d \
-p 8000:8000 \
--name fintech-api \
fintech-nova:$VERSION

echo "Esperando inicio..."
sleep 10

STATUS=$(curl -s http://localhost:8000/health | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

if [ "$STATUS" = "healthy" ] || [ "$STATUS" = "degraded" ]; then
    echo "¡Despliegue exitoso!"
else
    echo "ERROR: El despliegue falló"
fi