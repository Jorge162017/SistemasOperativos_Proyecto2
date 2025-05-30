# app.py
# Punto de entrada e interfaz completa para simulador con Streamlit (Versión estilizada con animación)
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

import streamlit as st
import random
import time
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scheduling_algorithms.funcs import leer_procesos, calcular_metricas, generar_tabla_resultados
from scheduling_algorithms.fifo_scheduler import fifo_scheduler
from scheduling_algorithms.sjf_scheduler import sjf_scheduler
from scheduling_algorithms.srt_scheduler import srt_scheduler
from scheduling_algorithms.rr_scheduler import round_robin_scheduler
from scheduling_algorithms.priority_scheduler import priority_scheduler

from sync_mechanisms.sync_entities import (
    leer_procesos as leer_procesos_sync,
    leer_recursos,
    leer_acciones,
)
from sync_mechanisms.mutex_mechanism import MutexSimulador
from sync_mechanisms.semaphore_mechanism import SemaforoSimulador

def dibujar_gantt(procesos, nombre, colores):
    fig, ax = plt.subplots(figsize=(10, max(len(procesos) * 0.6, 3)))
    y_pos = range(len(procesos))
    i = 0
    for p in procesos:
        if p.start_time is None or p.end_time is None:
            continue

        if p.pid not in colores:
            colores[p.pid] = (random.random(), random.random(), random.random())
        color = colores[p.pid]

        ax.broken_barh([(p.start_time, p.end_time - p.start_time)], (i - 0.4, 0.8), facecolors=color)
        ax.text(p.start_time + (p.end_time - p.start_time) / 2, i, p.pid,
                ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        i += 1

    ax.set_yticks(range(i))
    ax.set_yticklabels([p.pid for p in procesos if p.start_time is not None and p.end_time is not None])
    ax.set_xlabel('Tiempo')
    ax.set_title(f'Diagrama de Gantt - {nombre}')
    ax.grid(True)
    st.pyplot(fig)

def simular_tiempo_real(procesos):
    st.subheader("🟢 Simulación en tiempo real")
    fig, ax = plt.subplots(figsize=(10, max(len(procesos) * 0.6, 3)))
    ax.set_xlim(0, sum(p.bt for p in procesos) + 5)
    ax.set_ylim(-1, len(procesos))
    ax.set_xlabel('Tiempo')
    ax.set_title('Animación en tiempo real')
    ax.grid(True)
    colores = {}
    placeholders = [ax.text(-1, i, p.pid, va='center', fontsize=10, fontweight='bold') for i, p in enumerate(procesos)]
    plot = st.pyplot(fig)

    i = 0
    for p in procesos:
        if p.start_time is None or p.end_time is None:
            continue
        duracion = p.end_time - p.start_time
        if p.pid not in colores:
            colores[p.pid] = (random.random(), random.random(), random.random())
        color = colores[p.pid]

        barra = mpatches.Rectangle((p.start_time, i - 0.4), 0, 0.8, color=color)
        ax.add_patch(barra)
        plot.pyplot(fig)

        for j in range(1, duracion + 1):
            barra.set_width(j)
            plot.pyplot(fig)
            time.sleep(0.1)

        i += 1
    st.success("✅ Simulación completa")

def dibujar_sync(resultado, tipo):
    fig, ax = plt.subplots(figsize=(12, max(len(resultado) * 0.6, 3)))
    escala = 1
    for i, p in enumerate(resultado):
        for ciclo, estado in p.historial:
            color = '#27ae60' if estado == "ACCESSED" else '#c0392b'
            ax.broken_barh([(ciclo, escala)], (i - 0.4, 0.8), facecolors=color)
        ax.text(-1, i, p.pid, va='center', fontsize=10, fontweight='bold')

    ax.set_yticks([])
    ax.set_xlabel('Ciclos')
    ax.set_title(f'Sincronización ({tipo})')
    ax.grid(True)
    st.pyplot(fig)


def main():
    st.set_page_config(page_title="OrganizeMe Simulator - Jorge Lopez", layout="wide")
    st.title("🧩 OrganizeMe Simulator - Jorge Lopez")
    st.markdown("---")

    if "procesos" not in st.session_state:
        st.session_state.procesos = []
    if "recursos" not in st.session_state:
        st.session_state.recursos = {}
    if "acciones" not in st.session_state:
        st.session_state.acciones = []
    if "colors" not in st.session_state:
        st.session_state.colors = {}

    modo = st.radio("📍 Seleccione modo de simulación", ("Calendarización", "Sincronización"), horizontal=True)

    if modo == "Calendarización":
        st.subheader("📂 Cargar archivo de procesos")
        archivo = st.file_uploader("Archivo de texto con procesos", type=["txt"])

        if archivo is not None:
            try:
                st.session_state.procesos = leer_procesos(archivo)
                st.success(f"✅ Procesos cargados: {len(st.session_state.procesos)}")
            except Exception as e:
                st.error(f"❌ Error al leer procesos: {e}")

        st.markdown("---")
        st.subheader("⚙️ Configuración de algoritmo")
        algoritmos = {
            "FIFO": fifo_scheduler,
            "SJF": sjf_scheduler,
            "SRT": srt_scheduler,
            "Round Robin": round_robin_scheduler,
            "Priority": priority_scheduler,
        }

        seleccion = st.multiselect("Seleccionar algoritmos de planificación", list(algoritmos.keys()), default=["FIFO"])

        quantum = 3
        if "Round Robin" in seleccion:
            quantum = st.slider("Quantum para Round Robin", min_value=1, max_value=10, value=3)

        if st.button("▶️ Simular"):
            if not st.session_state.procesos:
                st.warning("⚠️ Primero carga un archivo de procesos.")
            else:
                st.session_state.colors = {}
                tabs = st.tabs(seleccion)

                for idx, nombre in enumerate(seleccion):
                    func = algoritmos[nombre]
                    if nombre == "Round Robin":
                        resultado = func(deepcopy(st.session_state.procesos), quantum)
                    else:
                        resultado = func(deepcopy(st.session_state.procesos))

                    procesos_res = resultado if not isinstance(resultado, tuple) else resultado[0]

                    with tabs[idx]:
                        simular_tiempo_real(procesos_res)
                        avg_wt, avg_tat = calcular_metricas(procesos_res)
                        st.subheader(f"📊 Resultados {nombre}")
                        st.metric("⏱️ Tiempo de espera promedio", f"{avg_wt:.2f}")
                        st.metric("⏳ Turnaround time promedio", f"{avg_tat:.2f}")
                        dibujar_gantt(procesos_res, nombre, st.session_state.colors)

                        # Nueva tabla por proceso
                        tabla_resultados = generar_tabla_resultados(procesos_res)
                        if tabla_resultados is not None:
                            st.subheader("📋 Tabla de resultados por proceso")
                            st.dataframe(tabla_resultados, use_container_width=True)

    else:
        st.subheader("🔐 Cargar archivos de sincronización")
        procesos_file = st.file_uploader("Procesos", type=["txt"], key="proc")
        recursos_file = st.file_uploader("Recursos", type=["txt"], key="rec")
        acciones_file = st.file_uploader("Acciones", type=["txt"], key="acc")

        tipo_sync = st.radio("Tipo de sincronización", ("Mutex", "Semáforo"), horizontal=True)

        if procesos_file and recursos_file and acciones_file:
            try:
                st.session_state.procesos = leer_procesos_sync(procesos_file)
                st.session_state.recursos = leer_recursos(recursos_file)
                st.session_state.acciones = leer_acciones(acciones_file)
                st.success("✅ Archivos de sincronización cargados correctamente.")
            except Exception as e:
                st.error(f"❌ Error al leer archivos: {e}")

            if st.button("▶️ Simular sincronización"):
                if not (st.session_state.procesos and st.session_state.recursos and st.session_state.acciones):
                    st.warning("⚠️ Faltan archivos para simular sincronización.")
                else:
                    simulador = MutexSimulador(st.session_state.procesos, st.session_state.recursos, st.session_state.acciones) \
                        if tipo_sync == "Mutex" else \
                        SemaforoSimulador(st.session_state.procesos, st.session_state.recursos, st.session_state.acciones)

                    resultado = simulador.ejecutar()
                    st.subheader("📈 Resultados de la sincronización")

                    for p in resultado:
                        estados = ", ".join([f"Ciclo {c}: {e}" for c, e in p.historial])
                        st.markdown(f"**Proceso {p.pid}**: {estados}")

                    dibujar_sync(resultado, tipo_sync)

if __name__ == "__main__":
    main()
