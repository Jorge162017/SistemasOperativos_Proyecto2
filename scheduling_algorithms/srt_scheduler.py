#Simulador Shortest Remaining Time (SRT)
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
        self.remaining_time = burst_time
        self.first_run = True
        self.finished = False

def srt_scheduler(process_list):
   
    #En cada ciclo selecciona el proceso con menor tiempo restante.
    #Puede interrumpir un proceso si llega otro con menor tiempo restante.
    
    process_list = sorted(process_list, key=lambda p: p.arrival_time)

    time = 0
    completed = 0
    n = len(process_list)
    scheduled_order = []

    while completed < n:
        # Procesos disponibles con tiempo restante > 0
        available = [p for p in process_list if p.arrival_time <= time and p.remaining_time > 0]

        if available:
            # Elegir proceso con menor tiempo restante
            current = min(available, key=lambda p: p.remaining_time)

            # Registrar inicio si es la primera ejecución
            if current.first_run:
                current.start_time = time
                current.first_run = False

            # Ejecutar 1 ciclo
            current.remaining_time -= 1
            time += 1

            # Si terminó
            if current.remaining_time == 0:
                current.finish_time = time
                current.finished = True
                scheduled_order.append(current)
                completed += 1
        else:
            # Si no hay procesos, avanzar el tiempo
            time += 1

    return scheduled_order
