#!/bin/bash

# ════════════════════════════════════════════════════════════
# Script: resource_monitor.sh
# Propósito: Monitorear recursos del sistema
# ════════════════════════════════════════════════════════════

# Umbrales
MEMORY_THRESHOLD=80
DISK_THRESHOLD=85

echo "========================================="
echo " MONITOR DE RECURSOS DEL SISTEMA"
echo "========================================="

# ── Memoria RAM ─────────────────────────

MEMORY_USED=$(free | grep Mem | awk '{print int($3/$2 * 100)}')

echo "Uso de memoria RAM: ${MEMORY_USED}%"

if [ "$MEMORY_USED" -gt "$MEMORY_THRESHOLD" ]; then
    echo "WARNING: Uso de memoria superior al ${MEMORY_THRESHOLD}%"
fi

# ── Disco ───────────────────────────────

DISK_USED=$(df -h . | tail -1 | awk '{print $5}' | tr -d '%')

echo "Uso del disco: ${DISK_USED}%"

if [ "$DISK_USED" -gt "$DISK_THRESHOLD" ]; then
    echo "WARNING: Uso del disco superior al ${DISK_THRESHOLD}%"
fi

# ── CPU ─────────────────────────────────

CPU_USED=$(top -bn1 | grep "Cpu(s)" | awk '{print int($2+$4)}')

echo "Uso de CPU: ${CPU_USED}%"

echo "========================================="
echo " Resumen"
echo "========================================="
echo "CPU     : ${CPU_USED}%"
echo "Memoria : ${MEMORY_USED}%"
echo "Disco   : ${DISK_USED}%"
echo "========================================="