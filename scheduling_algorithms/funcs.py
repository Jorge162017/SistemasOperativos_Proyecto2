# funcs.py - Funciones utilitarias para el simulador de planificación
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

from typing import Union
from io import TextIOWrapper

class Proceso:
    def __init__(self, pid: str, bt: int, at: int, priority: int):
        self.pid = pid  # ID del proceso
        self.bt = int(bt)  # Burst Time
        self.at = int(at)  # Arrival Time
        self.priority = int(priority)  # Prioridad

        self.remaining = int(bt)  # Tiempo restante (para RR y SRT)
        self.start_time = None  # Tiempo de inicio de ejecución
        self.end_time = None  # Tiempo de fin de ejecución
        self.first_run = True  # Marca si ya se ejecutó al menos una vez
        self.finished = False  # Estado finalizado

def leer_procesos(path_or_file: Union[str, TextIOWrapper]) -> list[Proceso]:
    procesos = []

    if isinstance(path_or_file, str):
        f = open(path_or_file, "r")
        close_after = True
    else:
        f = TextIOWrapper(path_or_file) if not isinstance(path_or_file, TextIOWrapper) else path_or_file
        close_after = False

    with f:
        for linea in f:
            if linea.strip():
                try:
                    pid, bt, at, pr = linea.strip().split(",")
                    procesos.append(Proceso(pid.strip(), bt.strip(), at.strip(), pr.strip()))
                except ValueError:
                    print(f"Error: línea mal formateada: {linea.strip()}")

    if close_after:
        f.close()

    return procesos

def calcular_metricas(procesos: list[Proceso]) -> tuple[float, float]:
    total_wt = 0
    total_tat = 0
    n = 0

    for p in procesos:
        if p.start_time is None or p.end_time is None:
            continue  # Omitir procesos incompletos

        wt = p.start_time - p.at
        tat = p.end_time - p.at
        total_wt += wt
        total_tat += tat
        n += 1

    avg_wt = total_wt / n if n > 0 else 0
    avg_tat = total_tat / n if n > 0 else 0
    return avg_wt, avg_tat

def generar_tabla_resultados(procesos: list[Proceso]) -> list[dict]:
    tabla = []
    for p in procesos:
        if p.start_time is None or p.end_time is None:
            continue  # Omitir procesos incompletos

        wt = p.start_time - p.at
        tat = p.end_time - p.at

        tabla.append({
            "Proceso": p.pid,
            "Inicio": p.start_time,
            "Fin": p.end_time,
            "Llegada": p.at,
            "Ráfaga": p.bt,
            "Espera": wt,
            "Turnaround": tat,
        })
    return tabla

__all__ = ["Proceso", "leer_procesos", "calcular_metricas", "generar_tabla_resultados"]
