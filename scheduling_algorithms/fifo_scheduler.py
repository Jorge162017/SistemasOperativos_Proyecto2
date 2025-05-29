# Simulador FIFO - First In First Out
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, bt, at, priority=0):
        self.pid = pid            # Identificador del proceso
        self.bt = bt              # Burst Time (tiempo de ejecución)
        self.at = at              # Arrival Time (tiempo de llegada)
        self.priority = priority  # Prioridad (no usada en FIFO)
        self.start_time = None    # Tiempo en que empieza a ejecutarse
        self.finish_time = None   # Tiempo en que termina de ejecutarse

def fifo_scheduler(process_list):
    # Ordenar procesos por tiempo de llegada (at)
    process_list = sorted(process_list, key=lambda proc: proc.at)
    
    current_time = 0
    for proc in process_list:
        # Si el CPU está libre, esperar a que el proceso llegue
        if current_time < proc.at:
            current_time = proc.at
        proc.start_time = current_time    # Marcar inicio de ejecución
        current_time += proc.bt           # Avanzar el tiempo según burst
        proc.finish_time = current_time   # Marcar fin de ejecución
    
    return process_list
