#!/bin/bash

# ==========================================================
# PLAN DE BACKUP - FINTECH NOVA
# ==========================================================

# 1. RPO (Recovery Point Objective)
#
# Se define un RPO de 1 hora.
#
# Justificación:
# La API procesa solicitudes de crédito continuamente.
# Un intervalo de una hora implica una pérdida máxima de
# información equivalente a las transacciones realizadas
# durante ese período, manteniendo un equilibrio entre
# disponibilidad y carga sobre el sistema.


# 2. RTO (Recovery Time Objective)
#
# Se establece un RTO de 15 minutos.
#
# La API no debería permanecer fuera de servicio más de
# 15 minutos, ya que esto afectaría la experiencia de los
# clientes y la disponibilidad de los servicios financieros.


# 3. Configuración de Cron
#
# Ejecutar un backup cada hora:
#
# 0 * * * * /workspaces/SeminarioSanmateo/fintech-nova-api/backup_db.sh


# 4. Copia Offsite (Regla 3-2-1)
#
# Se almacenaría una tercera copia en Amazon S3.
#
# Ejemplo:
#
# aws s3 cp backups/ s3://fintech-nova-backups/ --recursive
#
# También podría utilizarse Google Cloud Storage o Azure Blob.


# Reflexión
#
# Un RPO de una hora requiere ejecutar backups con mayor
# frecuencia. Esto incrementa las operaciones de entrada y
# salida (I/O) sobre el disco, aumenta el consumo de recursos
# y requiere una adecuada planificación para evitar afectar
# el rendimiento del servidor.