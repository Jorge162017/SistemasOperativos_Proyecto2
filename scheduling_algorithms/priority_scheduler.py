#Simulador de Planificación por Prioridad (No Expropiativo)
#Autor: Jorge Lopez
#Carné: 221038
#Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, burst_time, arrival_time, priority):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.start_time = None
        self.finish_time = None
        self.finished = False

def priority_scheduler(process_list):
    
    #Algoritmo de planificación por prioridad no expropiativa.
    #En cada ciclo selecciona el proceso disponible con mayor prioridad (menor valor).
    
    # Ordenamos por tiempo de llegada para control
    process_list = sorted(process_list, key=lambda proc: proc.arrival_time)
    
    time = 0
    completed = 0
    n = len(process_list)
    scheduled_order = []

    while completed < n:
        # Procesos disponibles: llegaron y no han terminado
        available = [p for p in process_list if p.arrival_time <= time and not p.finished]

        if available:
            # Seleccionar proceso con prioridad más alta (menor valor), y si hay empate, el que llegó primero
            current = min(available, key=lambda p: (p.priority, p.arrival_time))
            
            current.start_time = time
            time += current.burst_time
            current.finish_time = time
            current.finished = True

            scheduled_order.append(current)
            completed += 1
        else:
            # Si no hay procesos disponibles, avanzar el tiempo
            time += 1

    return scheduled_order