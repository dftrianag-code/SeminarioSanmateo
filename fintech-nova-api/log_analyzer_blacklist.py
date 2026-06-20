#!/usr/bin/env python3
"""
log_analyzer_blacklist.py
FinTech Nova - Laboratorio 3

Detecta intentos de SQL Injection y mantiene una lista negra
de IPs atacantes con fecha de detección.
"""

import re
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path

BLACKLIST_FILE = "ip_blacklist.txt"

# ── PATRONES DE DETECCIÓN ───────────────────────────────────
# Cada patrón es una tupla: (regex_pattern, descripción)
# re.IGNORECASE hace la búsqueda sin importar mayúsculas/minúsculas

SQL_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1", "Bypass de login (OR 1=1)"),
    (r"'\s*--", "Comentario SQL para ignorar password"),
    (r"UNION\s+SELECT", "Exfiltración UNION SELECT"),
    (r"DROP\s+TABLE", "Destrucción de tabla DROP TABLE"),
    (r"INSERT\s+INTO.*SELECT", "Inyección de datos"),
    (r"EXEC", "Ejecución de comandos EXEC"),
]


# ── CARGAR LISTA NEGRA ─────────────────────────────────────

def load_blacklist():
    blacklist = {}

    if Path(BLACKLIST_FILE).exists():

        with open(BLACKLIST_FILE, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if line:

                    ip, date = line.split(",")

                    blacklist[ip] = date

    return blacklist


# ── GUARDAR LISTA NEGRA ────────────────────────────────────

def save_blacklist(blacklist):

    with open(BLACKLIST_FILE, "w", encoding="utf-8") as f:

        for ip, date in blacklist.items():

            f.write(f"{ip},{date}\n")


# ── CALCULAR DÍAS EN LISTA NEGRA ───────────────────────────

def days_in_blacklist(date_string):

    start_date = datetime.strptime(date_string, "%Y-%m-%d")

    days = (datetime.now() - start_date).days

    return days


# ── ANALIZAR LOG ───────────────────────────────────────────

def analyze_log(log_path):

    incidents = []

    by_ip = defaultdict(int)

    by_type = defaultdict(int)

    total_lines = 0

    blacklist = load_blacklist()

    try:

        with open(log_path, "r", encoding="utf-8") as f:

            for line_num, line in enumerate(f, start=1):

                total_lines += 1

                line = line.strip()

                if not line:
                    continue

                for pattern, desc in SQL_PATTERNS:

                    if re.search(pattern, line, re.IGNORECASE):

                        ip_match = re.search(r"IP:\s*(\S+)", line)

                        ip = ip_match.group(1) if ip_match else "desconocida"

                        priority = "NORMAL"

                        if ip in blacklist:

                            priority = "ALTA"

                        else:

                            blacklist[ip] = datetime.now().strftime("%Y-%m-%d")

                        incidents.append({
                            "line": line_num,
                            "type": desc,
                            "ip": ip,
                            "priority": priority,
                            "content": line[:100]
                        })

                        by_ip[ip] += 1

                        by_type[desc] += 1

                        break

    except FileNotFoundError:

        print(f"[ERROR] No existe el archivo {log_path}")

        sys.exit(1)

    save_blacklist(blacklist)

    return {
        "total_lines": total_lines,
        "clean": total_lines - len(incidents),
        "incidents": incidents,
        "by_ip": dict(by_ip),
        "by_type": dict(by_type),
        "blacklist": blacklist
    }


# ── REPORTE ────────────────────────────────────────────────

def print_report(results, log_path):

    separator = "=" * 60

    print(f"\n{separator}")

    print("REPORTE DE SEGURIDAD - FinTech Nova")

    print(f"Archivo: {log_path}")

    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(separator)

    print(f"Total líneas: {results['total_lines']}")

    print(f"Líneas limpias: {results['clean']}")

    print(f"Incidentes: {len(results['incidents'])}")

    print(separator)

    if results["incidents"]:

        print("\nINCIDENTES DETECTADOS:\n")

        for i, incident in enumerate(results["incidents"], start=1):

            print(f"[{i}] Línea {incident['line']}")

            print(f"Tipo: {incident['type']}")

            print(f"IP: {incident['ip']}")

            print(f"Prioridad: {incident['priority']}")

            print(f"Contenido: {incident['content']}")

            print()

    print("IPs más activas:\n")

    for ip, count in sorted(
            results["by_ip"].items(),
            key=lambda x: x[1],
            reverse=True):

        days = days_in_blacklist(results["blacklist"][ip])

        print(f"{ip} -> {count} ataque(s) | {days} día(s) en lista negra")

    print("\nTipos de ataque:\n")

    for attack, count in sorted(
            results["by_type"].items(),
            key=lambda x: x[1],
            reverse=True):

        print(f"{attack}: {count}")

    print(f"\n{separator}\n")


# ── MAIN ───────────────────────────────────────────────────

if __name__ == "__main__":

    log_file = sys.argv[1] if len(sys.argv) > 1 else "server.log"

    print(f"[INFO] Analizando {log_file}")

    results = analyze_log(log_file)

    print_report(results, log_file)