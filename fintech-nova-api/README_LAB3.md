# Laboratorio 3 – Automatización, Monitoreo y Contenerización
## FinTech Nova API

Autor: David Triana  
Programa: Ingeniería de Sistemas  
Seminario de Arquitectura Segura  
Versión: 1.0

---

# 1. Descripción

FinTech Nova es una API desarrollada con FastAPI para la evaluación de riesgo crediticio. Durante este laboratorio se implementaron mecanismos de automatización, monitoreo, respaldo, análisis de logs y despliegue mediante Docker.

---

# 2. Estructura del proyecto

```
fintech-nova-api/
│
├── main.py
├── database.db
├── backup_db.sh
├── resource_monitor.sh
├── log_analyzer.py
├── health_check.py
├── deploy.sh
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
├── server.log
├── ip_blacklist.txt
├── backups/
└── data/
```

---

# 3. Prerrequisitos

Antes de ejecutar el proyecto es necesario tener instalado:

- Git
- Python 3.11
- Pip
- Docker
- Docker Compose
- Curl
- Uvicorn
- FastAPI

Verificar instalación:

```bash
git --version
python3 --version
docker --version
docker compose version
```

---

# 4. Configuración inicial

Ingresar al proyecto:

```bash
cd fintech-nova-api
```

Crear entorno virtual:

```bash
python3 -m venv .venv
```

Activar entorno:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# 5. Ejecución local

Iniciar la API:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Consultar estado:

```bash
curl http://localhost:8000/status
```

Consultar health check:

```bash
curl http://localhost:8000/health
```

---

# 6. Sistema de Backups

El script `backup_db.sh` realiza:

- Copia comprimida de la base de datos.
- Asignación de timestamp.
- Limpieza automática de copias antiguas.
- Conservación de backups por 7 días.

Ejecutar manualmente:

```bash
./backup_db.sh
```

Los respaldos se almacenan en:

```
backups/
```

---

# 7. Automatización con Cron

Editar crontab:

```bash
crontab -e
```

Agregar:

```bash
0 2 * * * /workspaces/SeminarioSanmateo/fintech-nova-api/backup_db.sh >> /tmp/backup.log 2>&1
```

Ver tareas configuradas:

```bash
crontab -l
```

Consultar logs:

```bash
cat /tmp/backup.log
```

---

# 8. Monitor de Recursos

Archivo:

```
resource_monitor.sh
```

Permite verificar:

- Uso de memoria RAM.
- Espacio en disco.
- Generación de advertencias cuando se superan los límites establecidos.

Ejecutar:

```bash
./resource_monitor.sh
```

---

# 9. Análisis de Logs

Archivo:

```
log_analyzer.py
```

Detecta:

- OR 1=1
- UNION SELECT
- DROP TABLE
- Comentarios SQL
- EXEC()

Ejecutar:

```bash
python3 log_analyzer.py
```

Genera:

- Número de incidentes.
- IP atacante.
- Tipo de ataque.
- Estadísticas por IP.

---

# 10. Lista Negra de IPs

Archivo:

```
ip_blacklist.txt
```

Funciones:

- Registrar IPs maliciosas.
- Detectar reincidencias.
- Llevar control histórico de ataques.

---

# 11. Health Check del Sistema

Archivo:

```
health_check.py
```

Verifica:

### Base de datos

- Accesibilidad.
- Tiempo de respuesta.

### Disco

- Espacio disponible.

### Backups

- Existencia y antigüedad.

### Memoria RAM

- Estado de utilización.

Estados posibles:

- healthy
- degraded
- unhealthy

Consultar:

```bash
curl http://localhost:8000/health
```

---

# 12. Docker de Producción

Construcción:

```bash
docker build -t fintech-nova:1.0 .
```

Ejecutar:

```bash
docker run -d \
-p 8000:8000 \
--name fintech-api \
fintech-nova:1.0
```

Ver contenedores:

```bash
docker ps
```

Logs:

```bash
docker logs -f fintech-api
```

Detener:

```bash
docker stop fintech-api
```

Eliminar:

```bash
docker rm fintech-api
```

---

# 13. Dockerfile.dev

Utilizado para desarrollo.

Características:

- Python 3.11 completo.
- Hot Reload.
- Soporte para pruebas.
- Dependencias de desarrollo.

Construcción:

```bash
docker build -f Dockerfile.dev -t fintech-dev .
```

Ejecución:

```bash
docker run -it \
-p 8001:8000 \
-v $(pwd):/app \
fintech-dev
```

---

# 14. Script de Despliegue

Archivo:

```
deploy.sh
```

Automatiza:

1. Verificar Docker.
2. Construir imagen.
3. Detener versión anterior.
4. Eliminar contenedor anterior.
5. Iniciar nuevo contenedor.
6. Esperar inicialización.
7. Verificar health check.

Ejecutar:

```bash
./deploy.sh
```

---

# 15. Docker Compose

Archivo:

```
docker-compose.yml
```

Servicios:

### API FinTech Nova

Puerto:

```
8000:8000
```

### Redis

Puerto:

```
6379:6379
```

Iniciar:

```bash
docker compose up -d
```

Ver servicios:

```bash
docker ps
```

Detener:

```bash
docker compose down
```

---

# 16. Solución de Problemas

## Error: crontab command not found

Instalar cron:

```bash
sudo apt update
sudo apt install cron
```

Iniciar servicio:

```bash
sudo service cron start
```

---

## Error: container name already in use

Detener:

```bash
docker stop fintech-api
```

Eliminar:

```bash
docker rm fintech-api
```

---

## Error: puerto ocupado

Verificar:

```bash
docker ps
```

Detener el contenedor que utiliza el puerto:

```bash
docker stop <container_id>
```

---

## Error: health check en estado degraded

Verificar:

- Existencia de la carpeta backups.
- Existencia de database.db.
- Espacio disponible en disco.

Consultar:

```bash
curl http://localhost:8000/health
```

---

# 17. Buenas prácticas implementadas

- Automatización mediante Cron.
- Backups periódicos.
- Limpieza automática de respaldos.
- Monitoreo de recursos.
- Detección de SQL Injection.
- Lista negra de IPs.
- Endpoint /health.
- Usuario no-root en Docker.
- Healthcheck automático.
- Docker Compose.
- Redis preparado para caché.
- Despliegue automatizado.

---

# 18. Conclusiones

Se implementó un entorno completo para FinTech Nova, integrando mecanismos de respaldo, monitoreo, seguridad y contenerización. El sistema permite automatizar tareas críticas, supervisar la salud de la aplicación y facilitar su despliegue y mantenimiento mediante Docker y Docker Compose, siguiendo buenas prácticas de administración y operación de servicios.