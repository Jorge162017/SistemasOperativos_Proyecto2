# main.py
# Punto de entrada alternativo para el simulador
# Autor: Jorge Lopez
# Carné: 221038
# Universidad del Valle de Guatemala

import tkinter as tk
from interface.simulator_gui import SimulatorGUI

def start_app():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Simulador UVG - Jorge Lopez")

    # Inicializar interfaz gráfica
    app = SimulatorGUI(ventana)

    # Ejecutar loop principal
    ventana.mainloop()

if __name__ == "__main__":
    start_app()
