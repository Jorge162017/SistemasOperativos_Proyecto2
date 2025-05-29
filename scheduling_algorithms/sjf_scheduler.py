# Simulador Shortest Job First (SJF)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

def sjf_scheduler(process_list):
    # Ejecuta siempre el proceso disponible con el menor tiempo de ráfaga (burst time).
    
    # Ordenar inicialmente por tiempo de llegada
    process_list = sorted(process_list, key=lambda p: p.at)

    time = 0
    completed = 0
    n = len(process_list)
    scheduled_order = []

    while completed < n:
        # Procesos que ya llegaron y no han terminado
        available = [p for p in process_list if p.at <= time and not p.finished]

        if available:
            # Elegir proceso con menor burst time
            current = min(available, key=lambda p: p.bt)
            current.start_time = time
            time += current.bt
            current.end_time = time
            current.finished = True
            scheduled_order.append(current)
            completed += 1
        else:
            # Si no hay procesos, avanzar tiempo
            time += 1

    return scheduled_order, None
