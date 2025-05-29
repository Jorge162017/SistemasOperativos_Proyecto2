# sync_entities.py
# Definición de clases y funciones para la simulación de mecanismos de sincronización
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

from io import TextIOWrapper
from typing import Union

class Recurso:
    def __init__(self, nombre, contador):
        self.nombre = nombre
        self.contador = int(contador)
        self.cola_espera = []

class Accion:
    def __init__(self, pid, tipo, recurso, ciclo):
        self.pid = pid
        self.tipo = tipo.upper()
        self.recurso = recurso
        self.ciclo = int(ciclo)

class ProcesoSincronizado:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.estado = "NEW"
        self.remaining = int(bt)
        self.historial = []

def _abrir_stream(archivo: Union[str, TextIOWrapper]) -> TextIOWrapper:
    if isinstance(archivo, str):
        return open(archivo, "r")
    if hasattr(archivo, "read") and hasattr(archivo, "name"):  # UploadedFile
        return TextIOWrapper(archivo, encoding="utf-8")
    raise ValueError("Tipo de archivo no soportado")

def leer_procesos(path_or_file: Union[str, TextIOWrapper]):
    procesos = []
    with _abrir_stream(path_or_file) as f:
        for linea in f:
            if linea.strip():
                pid, bt, at, pr = linea.strip().split(",")
                procesos.append(ProcesoSincronizado(pid.strip(), bt.strip(), at.strip(), pr.strip()))
    return procesos

def leer_recursos(path_or_file: Union[str, TextIOWrapper]):
    recursos = {}
    with _abrir_stream(path_or_file) as f:
        for linea in f:
            if linea.strip():
                nombre, contador = linea.strip().split(",")
                recursos[nombre.strip()] = Recurso(nombre.strip(), contador.strip())
    return recursos

def leer_acciones(path_or_file: Union[str, TextIOWrapper]):
    acciones = []
    with _abrir_stream(path_or_file) as f:
        for linea in f:
            if linea.strip():
                pid, tipo, recurso, ciclo = linea.strip().split(",")
                acciones.append(Accion(pid.strip(), tipo.strip(), recurso.strip(), ciclo.strip()))
    return sorted(acciones, key=lambda a: a.ciclo)
