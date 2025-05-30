class MutexSimulador:
    def __init__(self, procesos, recursos, acciones):
        self.procesos = {p.pid: p for p in procesos}
        self.recursos = recursos
        self.acciones = acciones
        self.ciclo = 0
        self.finalizados = set()
        self.acciones_pendientes = list(acciones)  # Cola mutable
        self.waiting_since = {}  # Registro del ciclo en que empezó a esperar

    def ejecutar(self):
        tiempo_total = max(a.ciclo for a in self.acciones) + 20  # Margen mayor

        while self.ciclo <= tiempo_total:
            # Verificar acciones nuevas o pendientes
            nuevas_acciones = [a for a in self.acciones_pendientes if a.ciclo == self.ciclo]
            self.acciones_pendientes = [a for a in self.acciones_pendientes if a not in nuevas_acciones]

            for accion in nuevas_acciones:
                proceso = self.procesos[accion.pid]
                recurso = self.recursos[accion.recurso]

                if accion.tipo in ["READ", "WRITE"]:
                    if recurso.contador > 0:
                        recurso.contador -= 1
                        proceso.estado = "ACCESSED"
                        proceso.historial.append((self.ciclo, "ACCESSED"))
                        self.waiting_since.pop(proceso.pid, None)  # Limpia si estaba esperando
                    else:
                        proceso.estado = "WAITING"
                        proceso.historial.append((self.ciclo, "WAITING"))
                        self.waiting_since[proceso.pid] = self.ciclo
                        recurso.cola_espera.append((proceso, self.ciclo))  # Guarda ciclo de espera

            # Liberación y reintento de recursos
            for recurso in self.recursos.values():
                nueva_cola = []
                for proceso, ciclo_espera in recurso.cola_espera:
                    if self.ciclo - ciclo_espera >= 1 and recurso.contador > 0:
                        recurso.contador -= 1
                        proceso.estado = "ACCESSED"
                        proceso.historial.append((self.ciclo, "ACCESSED"))
                        self.waiting_since.pop(proceso.pid, None)
                    else:
                        nueva_cola.append((proceso, ciclo_espera))
                recurso.cola_espera = nueva_cola

            self.ciclo += 1

        # Marcar como DONE al final
        for p in self.procesos.values():
            if p.estado == "ACCESSED":
                p.estado = "DONE"
                p.historial.append((self.ciclo, "DONE"))

        return list(self.procesos.values())
