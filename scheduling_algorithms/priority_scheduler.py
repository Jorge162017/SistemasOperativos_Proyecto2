# Simulador de Planificación por Prioridad (No Expropiativo)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.start_time = None
        self.finish_time = None
        self.end_time = None  # 👈 necesario para que se muestre en las gráficas
        self.remaining_time = int(bt)
        self.first_run = True
        self.finished = False

def priority_scheduler(process_list):
    process_list = sorted(process_list, key=lambda proc: proc.at)
    
    time = 0
    completed = 0
    n = len(process_list)

    while completed < n:
        available = [p for p in process_list if p.at <= time and not p.finished]

        if available:
            current = min(available, key=lambda p: (p.priority, p.at))
            current.start_time = time
            time += current.bt
            current.finish_time = time
            current.end_time = time  # 👈 necesario para la animación
            current.finished = True
            completed += 1
        else:
            time += 1

    return sorted(process_list, key=lambda p: p.start_time)
