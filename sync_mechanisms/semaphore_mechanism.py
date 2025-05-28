# semaphore_mechanism.py
# Simulador del mecanismo de Semáforos
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class SemaforoSimulador:
    def __init__(self, procesos, recursos, acciones):
        # Diccionario de procesos por PID para acceso rápido
        self.procesos = {p.pid: p for p in procesos}
        # Diccionario de recursos por nombre
        self.recursos = recursos
        # Lista de acciones a ejecutar (cada acción con ciclo, pid, tipo, recurso)
        self.acciones = acciones
        # Ciclo actual de la simulación
        self.ciclo = 0

    def ejecutar(self):
        # Tiempo máximo para ejecutar (ciclo máximo entre acciones + margen)
        tiempo_total = max(a.ciclo for a in self.acciones) + 10

        while self.ciclo <= tiempo_total:
            # Obtener todas las acciones que ocurren en el ciclo actual
            acciones_en_ciclo = [a for a in self.acciones if a.ciclo == self.ciclo]

            for accion in acciones_en_ciclo:
                proceso = self.procesos[accion.pid]
                recurso = self.recursos[accion.recurso]

                # Procesar acciones WAIT, WRITE o READ
                if accion.tipo in ["WAIT", "WRITE", "READ"]:
                    if recurso.contador > 0:
                        # Recurso disponible: proceso accede y ocupa el recurso
                        recurso.contador -= 1
                        proceso.estado = "ACCESSED"
                        proceso.historial.append((self.ciclo, "ACCESSED"))
                    else:
                        # Recurso no disponible: proceso espera
                        proceso.estado = "WAITING"
                        proceso.historial.append((self.ciclo, "WAITING"))
                        recurso.cola_espera.append(proceso)

                # Procesar acción SIGNAL (liberar recurso)
                elif accion.tipo == "SIGNAL":
                    recurso.contador += 1
                    # Si hay procesos en espera, asignar recurso al primero
                    if recurso.cola_espera:
                        siguiente = recurso.cola_espera.pop(0)
                        siguiente.estado = "ACCESSED"
                        siguiente.historial.append((self.ciclo, "ACCESSED"))
                        recurso.contador -= 1

            self.ciclo += 1

        # Al finalizar, marcar procesos que accedieron como terminados
        for p in self.procesos.values():
            if p.estado == "ACCESSED":
                p.estado = "DONE"
                p.historial.append((self.ciclo, "DONE"))

        return list(self.procesos.values())
