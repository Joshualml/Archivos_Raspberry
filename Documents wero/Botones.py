# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 15:02:46 2024

@author: mater
"""

import tkinter as tk  # Importa la librería tkinter para la interfaz gráfica
from tkinter import ttk  # Importa el submódulo ttk de tkinter para estilos de widgets avanzados
import serial  # Importa la librería pySerial para comunicación serial
import time  # Importa la librería time para gestionar el tiempo (delays)
import spidev  # Importa la librería spidev para comunicación SPI con dispositivos como el MCP3204
import matplotlib.pyplot as plt  # Importa matplotlib para gráficos
import matplotlib.animation as animation  # Importa el módulo de animación de matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite insertar gráficos de matplotlib en un widget de tkinter
import threading  # Importa la librería threading para crear hilos
import numpy as np  # Importa numpy para trabajar con arreglos numéricos
from calculo_presion import calculo_presion  # Importa la función de cálculo de presión desde un módulo personalizado

def activacion_sistema(root, id_usuario):
    # Elimina todos los widgets de la ventana para reiniciar la interfaz
    for widget in root.winfo_children():
        widget.destroy()

    # Configura el puerto serial para la comunicación con el Arduino en el puerto COM3
    arduino = serial.Serial('/dev/serial0', 9600, timeout=1)
    time.sleep(2)  # Espera 2 segundos para asegurarse de que la conexión serial esté establecida

    # Configura la interfaz SPI para comunicarte con el MCP3204 (convertidor analógico a digital)
    spi = spidev.SpiDev()  # Crea un objeto para comunicación SPI
    spi.open(1, 0)  # Abre la conexión SPI en el bus 1, dispositivo 0
    spi.max_speed_hz = 1350000  # Establece la velocidad de comunicación SPI

    # Inicializa las listas para almacenar los datos de los sensores
    Sensor1 = []
    Sensor2 = []
    
    # Variable para controlar la animación
    id_usuario1 = id_usuario  # Almacena el id del usuario para usarlo en otras funciones
    
    ani = None  # Variable global que almacenará la animación de la gráfica
    timelaps = 600  # Define el tiempo límite en el eje X para las gráficas

    
    def activar_bomba():
        """Envía el comando para activar la bomba"""
        if arduino.isOpen():
            print("Activando bomba...")
            arduino.write(b'1')  # Envía el comando '1' para activar la bomba en el Arduino
            time.sleep(0.1)
            # Iniciar la verificación del estado en un hilo separado
            threading.Thread(target=verificar_estado).start()
    
    def verificar_estado():
        """Verifica el estado de la bomba hasta que se apague"""
        while True:
            arduino.write(b's')  # Solicita el estado de la bomba
            estado = arduino.readline().decode('utf-8').strip()
    
            if estado == "0":
                print("Bomba desactivada.")
                break
            else:
                print("Bomba en proceso...")
    
            time.sleep(0.1)  # Espera 1 segundo antes de verificar de nuevo
    
    def funcion_extra():
        """Envía el comando para desactivar la bomba"""
        if arduino.isOpen():
            print("Desactivando bomba de emergencia...")
            arduino.write(b'2')  # Envía el comando '2' para desactivar la bomba
            time.sleep(0.1)
            # Iniciar la verificación del estado en un hilo separado
            threading.Thread(target=verificar_estado).start()
    
    def cerrar():
        """Cierra la conexión serial y la interfaz"""
        arduino.close()
        root.destroy()
        print("Conexión serial cerrada y aplicación terminada.")

    # Configura la ventana principal de la interfaz
    #root.attributes("-fullscreen", True)  # Configura la ventana para que ocupe toda la pantalla
    root.configure(bg="black")  # Establece el color de fondo de la ventana como negro

    # Crea un frame para los botones (1/3 de la pantalla)
    frame_botones = tk.Frame(root, width=root.winfo_screenwidth() // 3, bg="black")
    frame_botones.pack(side=tk.LEFT, fill=tk.BOTH)  # Empaqueta el frame en el lado izquierdo

    # Configura el tamaño de fuente y estilo de los botones
    button_font = ("Arial", 32, "bold")  # Establece la fuente y tamaño para los botones

    # Botón para activar la bomba
    boton_activar = tk.Button(frame_botones, text="Activar Bomba", font=button_font, command=activar_bomba, bg="green", fg="white")
    boton_activar.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón con relleno

    # Botón para la función extra
    boton_funcion_extra = tk.Button(frame_botones, text="Desactivador de emergencia", font=button_font, command=funcion_extra, bg="blue", fg="white")
    boton_funcion_extra.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón con relleno

    # Botón para cerrar la aplicación
    boton_salir = tk.Button(frame_botones, text="Salir", font=button_font, command=cerrar, bg="red", fg="white")
    boton_salir.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón con relleno

    # Crear una figura de Matplotlib y dos subplots para las gráficas (2/3 de la pantalla)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Crea una figura con dos subgráficas

    # Inicializa las listas de datos para los canales
    xdata, ydata_ch1, ydata_ch2 = [], [], []  # Listas para los datos del eje X y de los dos canales
    ln1, = ax1.plot([], [], 'r-', animated=True, label="CH1")  # Crea la línea para el canal 1
    ln2, = ax2.plot([], [], 'b-', animated=True, label="CH2")  # Crea la línea para el canal 2

    # Configura los límites de los gráficos
    for ax in (ax1, ax2):
        ax.set_xlim(0, timelaps)  # Establece el límite del eje X
        ax.set_ylim(0, 1027)  # Establece el límite del eje Y

    ax1.set_title("Señal del Canal 1")  # Título para el canal 1
    ax2.set_title("Señal del Canal 2")  # Título para el canal 2

    # Función para leer los datos del ADC
    def analogRead(pin):
        adc = spi.xfer2([1, (8 + pin) << 4, 0])  # Realiza la transferencia SPI para leer el ADC
        lec = ((adc[1] & 3) << 8) + adc[2]  # Calcula el valor leído
        return lec  # Devuelve el valor de la lectura

    # Función para inicializar la gráfica
    def init():
        ln1.set_data([], [])  # Inicializa la línea 1
        ln2.set_data([], [])  # Inicializa la línea 2
        return ln1, ln2  # Devuelve las líneas inicializadas

    def update(frame, id_usuario1):
        # Lee los datos de los dos canales
        lectura_ch1 = analogRead(0)
        lectura_ch2 = analogRead(1)

        # Almacena los datos en las listas correspondientes
        if len(Sensor1) < timelaps:
            Sensor1.append(lectura_ch1)  # Añade los datos de lectura al canal 1
            Sensor2.append(lectura_ch2)  # Añade los datos de lectura al canal 2
        else:
            # Si
