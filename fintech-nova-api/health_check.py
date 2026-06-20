#!/usr/bin/env python3

"""
health_check.py
Lógica de verificación de salud para FinTech Nova
"""

import sqlite3
import shutil
import os
import time
import psutil
from datetime import datetime
from typing import Tuple



# -------------------------------------------------
# Verificar base de datos
# -------------------------------------------------

def check_database(db_path="database.db"):
    """
    Verifica que la base de datos esté accesible y responda consultas.
    Retorna: (estado, mensaje) donde estado es 'ok', 'warning' o 'error'
    """

    if not os.path.exists(db_path):
        return "error", f"Archivo de BD no encontrado: {db_path}"

    try:

        start = time.time()
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute("SELECT 1")
        conn.close()
        elapsed_ms = (time.time() - start) * 1000

        if elapsed_ms > 500:
            return "warning", f"BD lenta: {elapsed_ms:.1f} ms"

        return "ok", f"BD accesible y respondiendo en {elapsed_ms:.1f} ms"

    except sqlite3.OperationalError as e:

        return "error", f"Error de conexión: {e}"


# -------------------------------------------------
# Verificar disco
# -------------------------------------------------

def check_disk(path="/", warn_pct=80, crit_pct=95):
    """
    Verifica el espacio en disco disponible.
    warn_pct: umbral de advertencia (%). crit_pct: umbral crítico (%).
    """

    try:

        usage = shutil.disk_usage(path)
        used_pct = (usage.used / usage.total) * 100
        free_gb = usage.free / (1024 ** 3)

        if used_pct >= crit_pct:

            return "error", f"Disco crítico: {used_pct:.1f}% usado"

        if used_pct >= warn_pct:

            return "warning", f"Disco alto: {used_pct:.1f}% usado"

        return "ok", f"Disco saludable: {used_pct:.1f}% usado ({free_gb:.1f} GB libres)"

    except Exception as e:

        return "error", str(e)


# -------------------------------------------------
# Verificar memoria RAM
# -------------------------------------------------

def check_memory():

    try:

        memory = psutil.virtual_memory()
        used_pct = memory.percent

        if used_pct > 90:

            return "error", f"RAM crítica: {used_pct}% usada"

        elif used_pct >= 75:

            return "warning", f"RAM alta: {used_pct}% usada"

        else:

            return "ok", f"RAM saludable: {used_pct}% usada"

    except Exception as e:

        return "error", str(e)
    

# -------------------------------------------------
# Verificar backups
# -------------------------------------------------

def check_backup(backup_dir="backups", max_age_hours=25):
    """
    Verifica que exista un backup reciente (del Bloque 1).
    Integración directa con backup_db.sh
    """

    if not os.path.isdir(backup_dir):

        return "warning", f"No existe {backup_dir}"

    backups = sorted(

        [f for f in os.listdir(backup_dir)
         if f.endswith(".tar.gz")]

    )

    if not backups:

        return "error", "No existen backups"

    latest = backups[-1]
    latest_path = os.path.join(backup_dir, latest)
    age_hours = (time.time() - os.path.getmtime(latest_path)) / 3600

    if age_hours > max_age_hours:

        return "warning", f"Backup antiguo ({age_hours:.1f} h)"

    return "ok", f"Backup reciente: {latest} ({age_hours:.1f} h)"


# -------------------------------------------------
# Ejecutar todos los checks
# -------------------------------------------------

def run_all_checks():
    """
    Ejecuta todas las verificaciones y retorna el estado consolidado.
    Es llamada por el endpoint /health de FastAPI.
    """

    checks = {}

    db_status, db_msg = check_database()
    disk_status, disk_msg = check_disk()
    backup_status, backup_msg = check_backup()
    memory_status, memory_msg = check_memory()

    checks["database"] = {
        "status": db_status,
        "message": db_msg
    }

    checks["disk"] = {
        "status": disk_status,
        "message": disk_msg
    }

    checks["backup"] = {
        "status": backup_status,
        "message": backup_msg
    }

    checks["memory"] = {
    "status": memory_status,
    "message": memory_msg
}   

    statuses = [checks[x]["status"] for x in checks]

    if "error" in statuses:

        overall = "unhealthy"

    elif "warning" in statuses:

        overall = "degraded"

    else:

        overall = "healthy"

    return {

        "status": overall,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "checks": checks

    }


# -------------------------------------------------
# Prueba independiente
# -------------------------------------------------

if __name__ == "__main__":

    import json
    result = run_all_checks()
    print(json.dumps(result, indent=4, ensure_ascii=False))