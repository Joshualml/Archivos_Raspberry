import time
import threading
import numpy as np
import serial
import spidev
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Configura el puerto serial para la comunicación con el Arduino en el puerto COM3
arduino = serial.Serial('/dev/serial0', 9600, timeout=1)  # Establece el puerto, velocidad y tiempo de espera
time.sleep(2)  # Espera 2 segundos para que se establezca la conexión serial

# Configurar SPI para MCP3204
spi = spidev.SpiDev()  # Crea un objeto SPI
spi.open(1, 2)  # Abre la conexión SPI en el bus 1, dispositivo 2
spi.max_speed_hz = 1350000  # Configura la velocidad máxima de transferencia SPI a 1.35 MHz

# Listas para almacenar las lecturas de los sensores
Sensor1 = []  # Almacena datos del canal 1
Sensor2 = []  # Almacena datos del canal 2

# Variable para controlar la animación
ani = None  # Almacena la referencia a la animación
timelaps = 600  # Límite en el eje x para las gráficas

def activar_bomba():
    """Envía el comando para activar la bomba y comienza la animación"""
    global ani
    Sensor1.clear()  # Limpia la lista de datos del canal 1
    Sensor2.clear()  # Limpia la lista de datos del canal 2

    if arduino.isOpen():  # Verifica si la conexión serial está abierta
        print("Activando bomba...")
        arduino.write(b'1')  # Envía el comando '1' para activar la bomba
        time.sleep(0.1)  # Espera un momento

        # Inicia la animación de gráficas
        ani = animation.FuncAnimation(fig, update, frames=range(timelaps), init_func=init, blit=True, interval=50)
        canvas.draw()  # Dibuja la animación en el canvas de Tkinter

        # Inicia la verificación del estado en un hilo separado
        threading.Thread(target=verificar_estado).start()

def verificar_estado():
    """Verifica el estado de la bomba hasta que se apague"""
    while True:
        arduino.write(b's')  # Envía el comando 's' para solicitar el estado
        estado = arduino.readline().decode('utf-8').strip()  # Lee y decodifica la respuesta
        if estado == "0":  # Si el estado es "0", la bomba está desactivada
            print("Bomba desactivada.")
            break  # Sale del bucle si la bomba está apagada
        else:
            print("Bomba en proceso...")
        time.sleep(0.1)  # Espera un momento antes de verificar nuevamente

def funcion_extra():
    """Envía el comando para la función extra"""
    if arduino.isOpen():  # Verifica si la conexión serial está abierta
        print("Desactivando Bomba")
        arduino.write(b'2')  # Envía el comando '2' para ejecutar la función extra
        time.sleep(0.1)  # Espera un momento

def cerrar():
    """Cierra la conexión serial y la interfaz"""
    arduino.close()  # Cierra la conexión serial
    root.destroy()  # Cierra la ventana de Tkinter
    print("Conexión serial cerrada y aplicación terminada.")

# Configurar la interfaz gráfica principal
root = tk.Tk()  # Crea una instancia de Tkinter
root.attributes("-fullscreen", True)  # Establece la ventana en pantalla completa
root.configure(bg="black")  # Configura el fondo de la ventana en negro

# Crear un frame para los botones (1/3 de la pantalla)
frame_botones = tk.Frame(root, width=root.winfo_screenwidth() // 3, bg="black")  # Crea un marco para los botones
frame_botones.pack(side=tk.LEFT, fill=tk.BOTH)  # Coloca el marco a la izquierda de la pantalla

# Configurar el tamaño de fuente y estilo de los botones
button_font = ("Arial", 32, "bold")  # Define el estilo de fuente para los botones

# Botón para activar la bomba
boton_activar = tk.Button(frame_botones, text="Activar Bomba", font=button_font, command=activar_bomba, bg="green", fg="white")
boton_activar.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón en el marco

# Botón para la función extra
boton_funcion_extra = tk.Button(frame_botones, text="Desactivador de emergencia", font=button_font, command=funcion_extra, bg="blue", fg="white")
boton_funcion_extra.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón en el marco

# Botón para cerrar la aplicación
boton_salir = tk.Button(frame_botones, text="Salir", font=button_font, command=cerrar, bg="red", fg="white")
boton_salir.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Empaqueta el botón en el marco

# Crear una figura de Matplotlib y dos subplots para las gráficas (2/3 de la pantalla)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Crea una figura y dos subplots

# Inicializar datos para los canales
xdata, ydata_ch1, ydata_ch2 = [], [], []  # Listas para almacenar datos de las gráficas
ln1, = ax1.plot([], [], 'r-', animated=True, label="CH1")  # Línea para el canal 1
ln2, = ax2.plot([], [], 'b-', animated=True, label="CH2")  # Línea para el canal 2

# Configurar límites de los gráficos
for ax in (ax1, ax2):
    ax.set_xlim(0, timelaps)  # Establece el límite x
    ax.set_ylim(0, 1024)  # Establece el límite y


ax1.set_title("Señal del Canal 1")  # Título del primer gráfico
ax2.set_title("Señal del Canal 2")  # Título del segundo gráfico

# Función para leer del ADC
def analogRead(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])  # Envía datos SPI para leer el valor del canal
    lec = ((adc[1] & 3) << 8) + adc[2]  # Convierte los datos leídos en un valor
    return lec  # Retorna el valor leído

# Función para inicializar la gráfica
def init():
    ln1.set_data([], [])  # Inicializa el gráfico del canal 1 vacío
    ln2.set_data([], [])  # Inicializa el gráfico del canal 2 vacío
    return ln1, ln2  # Retorna las líneas de los gráficos

def update(frame):
    # Leer los datos de los dos canales
    lectura_ch1 = analogRead(0)  # Lee el canal 1
    lectura_ch2 = analogRead(1)  # Lee el canal 2

    # Almacenar datos en listas y mantener el tamaño de `timelaps`
    if len(Sensor1) < timelaps:
        Sensor1.append(lectura_ch1)  # Agrega dato al canal 1
        Sensor2.append(lectura_ch2)  # Agrega dato al canal 2
    else:
        # Detener la animación al llenar las listas
        ani.event_source.stop()
        print("Límite alcanzado, guardando datos...")

        # Guardar los datos en archivos CSV
        np.savetxt("grafica8.csv", Sensor1, delimiter=",", header="Valor", comments="")
        np.savetxt("grafica9.csv", Sensor2, delimiter=",", header="Valor", comments="")
        return ln1, ln2  # No actualizar más después de guardar

    # Agregar datos a los arreglos correspondientes
    xdata.append(frame)  # Agrega el cuadro actual a xdata
    ydata_ch1.append(lectura_ch1)  # Agrega el valor de canal 1 a ydata_ch1
    ydata_ch2.append(lectura_ch2)  # Agrega el valor de canal 2 a ydata_ch2

    # Actualizar los datos en las líneas
    ln1.set_data(xdata, ydata_ch1)
    ln2.set_data(xdata, ydata_ch2)

    return ln1, ln2  # Retorna las líneas actualizadas

# Crear un canvas de Matplotlib dentro de tkinter
frame_graficas = tk.Frame(root, width=(root.winfo_screenwidth() * 2) // 3, bg="white")
frame_graficas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Coloca el marco a la derecha
canvas = FigureCanvasTkAgg(fig, master=frame_graficas)  # Crea un canvas de Matplotlib en el marco
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Empaqueta el canvas

# Iniciar el bucle de la interfaz gráfica
plt.tight_layout