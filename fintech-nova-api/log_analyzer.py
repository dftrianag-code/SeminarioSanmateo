#!/usr/bin/env python3

"""
log_analyzer.py — Detecta intentos de SQL Injection en logs de FinTech Nova
Sesión 13 - Laboratorio 3
"""

import re # Módulo de expresiones regulares (pattern matching)
import sys # Acceso a argumentos de línea de comandos
import json # Para exportar resultados en formato estructurado
from datetime import datetime
from collections import defaultdict

# ── PATRONES DE DETECCIÓN ───────────────────────────────────
# Cada patrón es una tupla: (regex_pattern, descripción)
# re.IGNORECASE hace la búsqueda sin importar mayúsculas/minúsculas

SQL_PATTERNS = [
    (r"'\s*OR\s*'?1'?\s*=\s*'?1", "Bypass de login (OR 1=1)"),
    (r"'\s*--", "Comentario SQL para ignorar password"),
    (r"UNION\s+SELECT", "Exfiltración UNION SELECT"),
    (r"DROP\s+TABLE", "Destrucción de tabla DROP TABLE"),
    (r"INSERT\s+INTO.*SELECT", "Inyección de datos"),
    (r"EXEC", "Ejecución de comandos EXEC")
]

# ── FUNCIÓN PRINCIPAL DE ANÁLISIS ───────────────────────────

def analyze_log(log_path: str) -> dict:
    """
    Analiza un archivo de logs y retorna estadísticas e incidentes detectados.
    Retorna un dict con: total_lines, clean, incidents, by_ip, by_type
    """

    incidents = []
    by_ip = defaultdict(int) # Cuántos ataques por cada IP
    by_type = defaultdict(int) # Cuántos ataques de cada tipo
    total_lines = 0

    try:
        # 'with open()' garantiza que el archivo se cierre aunque haya errores
        with open(log_path, 'r', encoding='utf-8') as f:

            for line_num, line in enumerate(f, start=1):
                total_lines += 1
                line = line.strip() # Elimina espacios y saltos de línea

                if not line: # Ignora líneas vacías
                    continue

                # Verificar cada patrón de SQL Injection
                for pattern, desc in SQL_PATTERNS:

                    if re.search(pattern, line, re.IGNORECASE):

                        # Extraer IP de la línea del log
                        ip_match = re.search(r'IP:\s*(\S+)', line)
                        ip = ip_match.group(1) if ip_match else 'desconocida'

                        incidents.append({
                            'line' : line_num,
                            'type' : desc,
                            'ip' : ip,
                            'content': line[:100], # Max 100 chars
                        })

                        by_ip[ip] += 1
                        by_type[desc] += 1

                        break # Una detección por línea es suficiente

    except FileNotFoundError:
        print(f'ERROR: Archivo no encontrado: {log_path}')
        sys.exit(1)

    except PermissionError:
        print(f'ERROR: Sin permisos para leer: {log_path}')
        sys.exit(1)

    return {
        'total_lines': total_lines,
        'clean' : total_lines - len(incidents),
        'incidents' : incidents,
        'by_ip' : dict(by_ip),
        'by_type' : dict(by_type),
     }

# ── FUNCIÓN PARA MOSTRAR EL REPORTE ─────────────────────────

def print_report(results: dict, log_path: str):
    """Imprime un reporte legible con los resultados del análisis."""

    sep = '=' * 60

    print(f'\n{sep}')
    print(f' REPORTE DE SEGURIDAD — FinTech Nova')
    print(f' Archivo : {log_path}')
    print(f' Fecha : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'{sep}')

    print(f' Total líneas : {results["total_lines"]}')
    print(f' Líneas limpias : {results["clean"]}')
    print(f' Incidentes : {len(results["incidents"])}')

    print(f'{sep}\n')

    if results['incidents']:
        print(' INCIDENTES DETECTADOS:')

        for i, inc in enumerate(results['incidents'], 1):

            print(f' [{i}] Línea {inc["line"]} | {inc["type"]}')
            print(f' IP: {inc["ip"]}')
            print(f' {inc["content"][:80]}...')
            print()

        print(' IPs más activas:')

        for ip, count in sorted(
            results['by_ip'].items(),
            key=lambda x: -
            x[1]):

            print(f' {ip}: {count} ataque(s)')

        print("\nTipos de ataque detectados:")

        for attack_type, count in sorted(
                results["by_type"].items(),
                key=lambda x: x[1],
                reverse=True):

            print(f"  {attack_type}: {count}")

    else:

        print(' Sin incidentes. Logs limpios.')
        print(f'\n{sep}\n')

# ── PUNTO DE ENTRADA ────────────────────────────────────────
#             
if __name__ == '__main__':
    # Permite especificar otro archivo por línea de comandos
    log_file = sys.argv[1] if len(sys.argv) > 1 else "server.log"

    print(f"[INFO] Analizando archivo: {log_file}")

    results = analyze_log(log_file)

    print_report(results, log_file)
