# Simulador Round Robin (RR)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, bt, at, priority=0):
        self.pid = pid
        self.bt = bt
        self.at = at
        self.priority = priority
        self.start_time = None
        self.end_time = None
        self.remaining = bt
        self.first_run = True
        self.finished = False

def round_robin_scheduler(process_list, quantum):
    # Algoritmo Round Robin con quantum fijo.
    # Reparte tiempo de CPU equitativamente entre los procesos.

    process_list = sorted(process_list, key=lambda p: p.at)

    time = 0
    queue = []
    completed = 0
    n = len(process_list)
    scheduled_order = []
    index = 0

    while completed < n:
        # Agregar a la cola procesos que hayan llegado hasta ahora
        while index < n and process_list[index].at <= time:
            queue.append(process_list[index])
            index += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)

        if current.first_run:
            current.start_time = time
            current.first_run = False

        exec_time = min(quantum, current.remaining)
        time += exec_time
        current.remaining -= exec_time

        while index < n and process_list[index].at <= time:
            queue.append(process_list[index])
            index += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            current.end_time = time
            current.finished = True
            scheduled_order.append(current)
            completed += 1

    return scheduled_order, None  # Devuelve también timeline=None por consistencia con otros schedulers
