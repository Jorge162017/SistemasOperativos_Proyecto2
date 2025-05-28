# Simulador del mecanismo Mutex
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class MutexSimulador:
    def __init__(self, procesos, recursos, acciones):
        # Diccionario de procesos por PID para acceso rápido
        self.procesos = {p.pid: p for p in procesos}
        # Diccionario de recursos por nombre
        self.recursos = recursos
        # Lista de acciones a ejecutar (cada acción con ciclo, pid, tipo, recurso)
        self.acciones = acciones
        # Ciclo actual de la simulación
        self.ciclo = 0
        # Conjunto de procesos finalizados (puede usarse para métricas o control)
        self.finalizados = set()

    def ejecutar(self):
        # Tiempo máximo para ejecutar (ciclo máximo entre acciones + margen)
        tiempo_total = max(a.ciclo for a in self.acciones) + 10

        while self.ciclo <= tiempo_total:
            # Obtener todas las acciones que ocurren en el ciclo actual
            acciones_en_ciclo = [a for a in self.acciones if a.ciclo == self.ciclo]

            for accion in acciones_en_ciclo:
                proceso = self.procesos[accion.pid]
                recurso = self.recursos[accion.recurso]

                # Solo procesar acciones de lectura o escritura
                if accion.tipo in ["READ", "WRITE"]:
                    if recurso.contador > 0:
                        # Recurso disponible: proceso accede y ocupa el recurso
                        recurso.contador -= 1
                        proceso.estado = "ACCESSED"
                        proceso.historial.append((self.ciclo, "ACCESSED"))
                    else:
                        # Recurso no disponible: proceso debe esperar
                        proceso.estado = "WAITING"
                        proceso.historial.append((self.ciclo, "WAITING"))
                        recurso.cola_espera.append(proceso)

            # Al finalizar el ciclo, liberar recursos y asignar al siguiente en cola
            for recurso in self.recursos.values():
                if recurso.cola_espera:
                    siguiente = recurso.cola_espera.pop(0)
                    recurso.contador -= 1
                    siguiente.estado = "ACCESSED"
                    siguiente.historial.append((self.ciclo, "ACCESSED"))

            self.ciclo += 1

        # Marcar los procesos que accedieron como terminados al finalizar la simulación
        for p in self.procesos.values():
            if p.estado == "ACCESSED":
                p.estado = "DONE"
                p.historial.append((self.ciclo, "DONE"))

        return list(self.procesos.values())
