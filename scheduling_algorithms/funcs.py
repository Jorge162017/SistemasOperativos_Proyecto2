# funcs.py - Funciones utilitarias para el simulador de planificación
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Proceso:
    def __init__(self, pid: str, bt: int, at: int, priority: int):
        # Inicializa un proceso con sus atributos básicos y estados
        self.pid = pid  # ID del proceso
        self.bt = int(bt)  # Burst Time
        self.at = int(at)  # Arrival Time
        self.priority = int(priority)  # Prioridad (menor número = mayor prioridad)

        self.remaining = int(bt)  # Tiempo restante (para RR y SRT)
        self.start_time = None  # Tiempo de inicio de ejecución
        self.end_time = None  # Tiempo de fin de ejecución
        self.first_run = True  # Marca primer ciclo (RR, SRT)
        self.finished = False  # Indica si terminó el proceso

def leer_procesos(path: str) -> list[Proceso]:
    # Lee un archivo de texto y devuelve una lista de objetos Proceso
    # Formato por línea: <PID>, <BT>, <AT>, <Priority>
    procesos = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                try:
                    pid, bt, at, pr = linea.strip().split(",")
                    procesos.append(Proceso(pid.strip(), bt.strip(), at.strip(), pr.strip()))
                except ValueError:
                    print(f"Error: línea mal formateada: {linea.strip()}")
    return procesos

def calcular_metricas(procesos: list[Proceso]) -> tuple[float, float]:
    # Calcula métricas promedio para un conjunto de procesos:
    # - Waiting Time (WT) = Start Time - Arrival Time
    # - Turnaround Time (TAT) = End Time - Arrival Time
    total_wt = 0
    total_tat = 0
    n = len(procesos)

    for p in procesos:
        wt = p.start_time - p.at
        tat = p.end_time - p.at
        total_wt += wt
        total_tat += tat

    avg_wt = total_wt / n if n > 0 else 0
    avg_tat = total_tat / n if n > 0 else 0
    return avg_wt, avg_tat

__all__ = ["Proceso", "leer_procesos", "calcular_metricas"]
