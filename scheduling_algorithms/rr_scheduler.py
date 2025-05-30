# Simulador Round Robin (RR)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Process:
    def __init__(self, pid, bt, at, priority=0):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.start_time = None
        self.end_time = None
        self.remaining = int(bt)
        self.first_run = True
        self.finished = False

def round_robin_scheduler(process_list, quantum):
    process_list = sorted(process_list, key=lambda p: p.at)
    time = 0
    queue = []
    completed = 0
    n = len(process_list)
    timeline = []
    index = 0

    while completed < n:
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
        timeline.append((current.pid, time, time + exec_time))

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
            completed += 1

    return process_list, timeline
