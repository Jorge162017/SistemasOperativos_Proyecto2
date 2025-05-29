# Simulador Shortest Remaining Time (SRT)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

def srt_scheduler(process_list):
    # En cada ciclo selecciona el proceso con menor tiempo restante.
    # Puede interrumpir un proceso si llega otro con menor tiempo restante.

    process_list = sorted(process_list, key=lambda p: p.at)

    time = 0
    completed = 0
    n = len(process_list)
    scheduled_order = []

    while completed < n:
        # Procesos disponibles con tiempo restante > 0
        available = [p for p in process_list if p.at <= time and p.remaining > 0]

        if available:
            # Elegir proceso con menor tiempo restante
            current = min(available, key=lambda p: p.remaining)

            # Registrar inicio si es la primera ejecución
            if current.first_run:
                current.start_time = time
                current.first_run = False

            # Ejecutar 1 ciclo
            current.remaining -= 1
            time += 1

            # Si terminó
            if current.remaining == 0:
                current.end_time = time
                current.finished = True
                scheduled_order.append(current)
                completed += 1
        else:
            # Si no hay procesos, avanzar el tiempo
            time += 1

    return scheduled_order, None
