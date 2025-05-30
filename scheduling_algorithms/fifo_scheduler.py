# Simulador FIFO - First In First Out
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

def fifo_scheduler(process_list):
    # Ordenar procesos por tiempo de llegada (at)
    process_list = sorted(process_list, key=lambda proc: proc.at)
    
    current_time = 0
    for proc in process_list:
        if current_time < proc.at:
            current_time = proc.at
        proc.start_time = current_time
        current_time += proc.bt
        proc.end_time = current_time  # 👈 CAMBIO importante: usar end_time en lugar de finish_time

    return process_list
