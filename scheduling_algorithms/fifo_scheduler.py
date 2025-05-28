#Simulador FIFO - First In First Out
#Autor: Jorge Lopez
#Carné: 221038
#Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, burst_time, arrival_time, priority=0):
        self.pid = pid                  # Identificador del proceso
        self.burst_time = burst_time    # Tiempo que tarda en ejecutarse
        self.arrival_time = arrival_time# Tiempo de llegada al sistema
        self.priority = priority        # Prioridad (no usada en FIFO)
        self.start_time = None          # Tiempo en que empieza a ejecutarse
        self.finish_time = None         # Tiempo en que termina de ejecutarse

def fifo_scheduler(process_list):
    # Ordenar procesos por tiempo de llegada (arrival_time)
    process_list = sorted(process_list, key=lambda proc: proc.arrival_time)
    
    current_time = 0
    for proc in process_list:
        # Si el CPU está libre, esperar a que el proceso llegue
        if current_time < proc.arrival_time:
            current_time = proc.arrival_time
        proc.start_time = current_time    # Marcar inicio de ejecución
        current_time += proc.burst_time   # Avanzar el tiempo según burst
        proc.finish_time = current_time   # Marcar fin de ejecución
    
    return process_list