#Simulador Shortest Job First (SJF)
#Autor: Jorge Lopez
#Carné: 221038
#Universidad del Valle de Guatemala


class Process:
    def __init__(self, pid, burst_time, arrival_time, priority=0):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.start_time = None
        self.finish_time = None
        self.finished = False

def sjf_scheduler(process_list):

    #Ejecuta siempre el proceso disponible con el menor tiempo de ráfaga (burst time).
    
    # Ordenar inicialmente por tiempo de llegada
    process_list = sorted(process_list, key=lambda p: p.arrival_time)

    time = 0
    completed = 0
    n = len(process_list)
    scheduled_order = []

    while completed < n:
        # Procesos que ya llegaron y no han terminado
        available = [p for p in process_list if p.arrival_time <= time and not p.finished]

        if available:
            # Elegir proceso con menor burst time
            current = min(available, key=lambda p: p.burst_time)
            current.start_time = time
            time += current.burst_time
            current.finish_time = time
            current.finished = True
            scheduled_order.append(current)
            completed += 1
        else:
            # Si no hay procesos, avanzar tiempo
            time += 1

    return scheduled_order
