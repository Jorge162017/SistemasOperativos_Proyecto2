# sync_entities.py
# Definición de clases y funciones para la simulación de mecanismos de sincronización
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

class Recurso:
    def __init__(self, nombre, contador):
        # Nombre del recurso
        self.nombre = nombre
        # Contador que indica cuántas unidades del recurso están disponibles
        self.contador = int(contador)
        # Cola de procesos esperando por este recurso
        self.cola_espera = []

class Accion:
    def __init__(self, pid, tipo, recurso, ciclo):
        # ID del proceso que realiza la acción
        self.pid = pid
        # Tipo de acción (READ, WRITE, WAIT, SIGNAL)
        self.tipo = tipo.upper()
        # Nombre del recurso involucrado
        self.recurso = recurso
        # Ciclo en el que ocurre la acción
        self.ciclo = int(ciclo)

class ProcesoSincronizado:
    def __init__(self, pid, bt, at, priority):
        # ID del proceso
        self.pid = pid
        # Burst Time (tiempo total de ejecución)
        self.bt = int(bt)
        # Arrival Time (tiempo de llegada)
        self.at = int(at)
        # Prioridad (menor número = mayor prioridad)
        self.priority = int(priority)
        # Estado actual: NEW, READY, WAITING, ACCESSED, DONE
        self.estado = "NEW"
        # Tiempo restante para ejecución (usado en algunos algoritmos)
        self.remaining = int(bt)
        # Historial de estados (lista de tuplas con ciclo y estado)
        self.historial = []

def leer_procesos(path):
    # Lee archivo y devuelve lista de procesos sincronizados
    procesos = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, bt, at, pr = linea.strip().split(",")
                procesos.append(ProcesoSincronizado(pid.strip(), bt.strip(), at.strip(), pr.strip()))
    return procesos

def leer_recursos(path):
    # Lee archivo y devuelve diccionario de recursos
    recursos = {}
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                nombre, contador = linea.strip().split(",")
                recursos[nombre.strip()] = Recurso(nombre.strip(), contador.strip())
    return recursos

def leer_acciones(path):
    # Lee archivo y devuelve lista de acciones ordenadas por ciclo
    acciones = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, tipo, recurso, ciclo = linea.strip().split(",")
                acciones.append(Accion(pid.strip(), tipo.strip(), recurso.strip(), ciclo.strip()))
    return sorted(acciones, key=lambda a: a.ciclo)
