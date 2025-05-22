import spidev
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.signal import find_peaks
import serial

# Configura el puerto serial para la comunicación con el Arduino
arduino = serial.Serial('/dev/serial0', 115200, timeout=1)
sleep(2)  # Espera a que se establezca la conexión serial

# Configurar SPI
spi = spidev.SpiDev()
spi.open(1, 0)  # SPI1, CE2
spi.max_speed_hz = 1350000  # Establecer velocidad una vez

# Inicializar la gráfica con Matplotlib
fig, ax = plt.subplots()
xdata, ydata, presion_data = [], [], []  # Lista adicional para la presión
ln, = plt.plot([], [], 'r-', animated=True)
peaks_plot, = plt.plot([], [], 'bo', label="Picos", animated=True)  # Picos detectados (puntos azules)
presion_plot, = plt.plot([], [], 'g-', label="Presión", animated=True, linewidth=2)  # Presión (línea verde)

# Configurar los límites del gráfico
timelaps = 1400
ax.set_xlim(0, timelaps)  # 45 segundos (900 muestras, 20 muestras/segundo)
ax.set_ylim(0, 1023)  # Rango de la variable 'lectura' (0-1024)

# Se inician variables de Control de bomba
pico = 0
key = 0
keyZero = 0
promedio = []
peaks = []
final_peaks = []

# Función para leer del ADC
def analogRead(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    lec = ((adc[1] & 3) << 8) + adc[2]
    return lec

# Función para inicializar la gráfica
def init():
    ln.set_data([], [])
    peaks_plot.set_data([], [])
    presion_plot.set_data([], [])
    return ln, peaks_plot, presion_plot

# Función para actualizar los datos de la gráfica
def update(frame):
    global pico
    global key
    global peaks

    lectura = analogRead(1) * -1 + 1024   # Presión Oscilometrica
    sensor = analogRead(0)                # Presión Base

    Vout0 = sensor * 3.25;
    Vout = Vout0 / 1023;
    print(Vout)
    sujetador = (Vout - 1.8) / (3.3 - 1.8) * (4.5 - 0.44) + 0.44;
    print(sujetador)
    Presion = (sujetador - 0.54) * 450 / 4;
    print(Presion)


    xdata.append(frame)
    ydata.append(lectura)
    presion_data.append(Presion)  # Guardar el valor de la presión

    # Si ya tenemos más de 900 puntos, eliminamos los más antiguos
    if len(xdata) > timelaps:
        xdata.pop(0)
        ydata.pop(0)
        presion_data.pop(0)  # También eliminar el valor de presión más antiguo


    old_len = len(peaks) # tamaño anterior de los picos

    # Detectar picos máximos en los datos de la señal
    peaks, _ = find_peaks(ydata)

    if arduino.in_waiting > 0:  # Si hay datos disponibles en el buffer
        data = arduino.readline().decode('utf-8').rstrip()  # Leer la línea de datos y decodificarla
        print(Presion)

    if (Presion >= 185):
        #print("Apagar bomba...")
        arduino.write(b'1')
        print(Presion)

    # Si se detectan picos, obtener el valor máximo de los picos
    if len(peaks) > 0:  # Si se detectan picos
        pico = len(peaks) - 1
        peak_values = np.array(ydata)[peaks]  # Obtener los valores de los picos

        """
        if (old_len < len(peaks)):   # De esta forma sabemos que ya se encontró un nuevo pico
            # print(f"Pico(s) detectado(s) en el frame {frame}: {peak_values[pico]}")  # Imprimir el valor de los picos

            if ((peak_values[pico] > 750) & (key != 2)):
                key += 1
            if ((peak_values[pico] < 560) & (key == 2)):
                key += 1
                if arduino.isOpen():
                    print("Apagar bomba...")
                    arduino.write(b'1')
                    print(Presion)
        """


    # Actualizar los datos de la gráfica
    ln.set_data(xdata, ydata)
    peaks_plot.set_data(np.array(xdata)[peaks], np.array(ydata)[peaks])
    presion_plot.set_data(xdata, presion_data)  # Actualizar la gráfica de la presión

    return ln, peaks_plot, presion_plot

# Animar los datos de la gráfica en tiempo real
ani = animation.FuncAnimation(fig, update, frames=range(timelaps),  # 900 frames para 45 segundos
                              init_func=init, blit=True, interval=50)  # Intervalo de 50ms (20 muestras por segundo)

# Mostrar la gráfica
plt.legend()  # Añadir la leyenda para los picos y la presión
plt.show()

# Al finalizar, cierra el SPI
spi.close()