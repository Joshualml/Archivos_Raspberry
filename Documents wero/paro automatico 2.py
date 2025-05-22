# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:52:23 2025

@author: mater
"""

import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from collections import deque

# Configurar el puerto serial (ajusta el puerto y el baudrate según tu Arduino)
puerto = "COM9"  # Para Windows (ejemplo: COM3), en Linux/Mac: "/dev/ttyUSB0"
baudrate = 115200
ser = serial.Serial(puerto, baudrate)

# Configurar la ventana de datos para la gráfica
ventana_muestras = 100 # Número de muestras a graficar
datos = deque([0] * ventana_muestras, maxlen=ventana_muestras)

# Configurar la figura
plt.ion()
fig, ax = plt.subplots()
linea_senal, = ax.plot(range(ventana_muestras), np.zeros(ventana_muestras), label="Señal Original")
linea_env, = ax.plot(range(ventana_muestras), np.zeros(ventana_muestras), label="Envolvente", linestyle="dashed", color="red")
ax.set_ylim(0, 3)  # Ajusta según el rango de la señal
ax.legend()

# Bucle para recibir datos en tiempo real
try:
    while True:
        # Leer dato del puerto serial
        if ser.in_waiting > 0:
            valor = ser.readline().decode('utf-8').strip()
            try:
                valor_float = float(valor)
                datos.append(valor_float)

                # Calcular la envolvente con Transformada de Hilbert
                senal = np.array(datos)
                senal_analitica = hilbert(senal)
                envolvente = np.abs(senal_analitica)

                # Actualizar las gráficas
                linea_senal.set_ydata(senal)
                linea_env.set_ydata(envolvente)
                
                plt.pause(0.005)
            except ValueError:
                pass  # Ignorar errores de conversión de datos

except KeyboardInterrupt:
    print("Interrumpido por el usuario")
    ser.close()
