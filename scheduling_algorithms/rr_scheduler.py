#Simulador Round Robin (RR)
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

def round_robin_scheduler(process_list, quantum):
    
    #Algoritmo Round Robin con quantum fijo.
    #Reparte tiempo de CPU equitativamente entre los procesos.
    
    # Ordenamos procesos por tiempo de llegada
    process_list = sorted(process_list, key=lambda p: p.arrival_time)

    time = 0
    queue = []
    completed = 0
    n = len(process_list)
    scheduled_order = []
    index = 0

    while completed < n:
        # Añadir a la cola los procesos que hayan llegado hasta el tiempo actual
        while index < n and process_list[index].arrival_time <= time:
            queue.append(process_list[index])
            index += 1

        if not queue:
            # Si no hay procesos en la cola, avanzar el tiempo
            time += 1
            continue

        current = queue.pop(0)

        # Registrar tiempo de inicio en la primera ejecución
        if current.first_run:
            current.start_time = time
            current.first_run = False

        # Ejecutar proceso por el tiempo mínimo entre quantum y tiempo restante
        exec_time = min(quantum, current.remaining_time)
        time += exec_time
        current.remaining_time -= exec_time

        # Añadir nuevos procesos que llegaron mientras se ejecutaba el proceso actual
        while index < n and process_list[index].arrival_time <= time:
            queue.append(process_list[index])
            index += 1

        if current.remaining_time > 0:
            # Si el proceso no terminó, vuelve al final de la cola
            queue.append(current)
        else:
            # Proceso finalizado
            current.finish_time = time
            current.finished = True
            scheduled_order.append(current)
            completed += 1

    return scheduled_order
