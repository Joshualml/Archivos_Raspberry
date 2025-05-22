import spidev
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import CubicSpline

# Configurar SPI
spi = spidev.SpiDev()
spi.open(1, 0)  # SPI1, CE2
spi.max_speed_hz = 1350000  # Establecer velocidad una vez

# Inicializar la gráfica con Matplotlib
fig, ax = plt.subplots()
xdata, ydata, envelope_data = [], [], []
ln, = plt.plot([], [], 'r-', animated=True)
envelope_ln, = plt.plot([], [], 'b--', animated=True)  # Línea de la envolvente

# Lista para almacenar los valores de la envolvente
envelope_history = []

# Configurar los límites del gráfico
timelaps = 2100
ax.set_xlim(0, timelaps)  # 45 segundos (900 muestras, 20 muestras/segundo)
ax.set_ylim(0, 1024)  # Rango de la variable 'lectura' (0-1024)

key = 0

# Función para leer del ADC
def analogRead(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    lec = ((adc[1] & 3) << 8) + adc[2]
    return lec

# Función para inicializar la gráfica
def init():
    ln.set_data([], [])
    envelope_ln.set_data([], [])
    return ln, envelope_ln

# Función para actualizar los datos de la gráfica
def update(frame):
    global key
    lectura = analogRead(0)  # Leer del canal 0 del ADC

    xdata.append(frame)
    ydata.append(lectura)

    # Si ya tenemos más de 900 puntos, eliminamos los más antiguos
    if len(xdata) > timelaps:
        xdata.pop(0)
        ydata.pop(0)

    # Detectar picos máximos en los datos de la señal
    peaks, _ = find_peaks(ydata)

    # Si hay picos, generar la envolvente utilizando interpolación cúbica
    if len(peaks) > 2:
        # Interpolación cúbica entre los picos máximos
        cs = CubicSpline([xdata[i] for i in peaks], [ydata[i] for i in peaks])
        envelope = cs(np.array(xdata))  # Generar la envolvente
        envelope_data = envelope

        # Almacenar la envolvente para poder acceder a ella más tarde
        #envelope_history.append(envelope)
        #current_envelope_value = envelope[frame]

        #if ((current_envelope_value > 700) & (key != 2)):
        #   key += 1
        #if (current_envelope_value < 650 & key == 2):
        #   print("Apagar bomba")
        #   sleep(4)

        # Solo imprimir los valores de la envolvente para los picos
        #print(f"Envolvente en el frame {frame}: {envelope[frame]}")  # Imprimir solo el valor en el frame actual


        envelope_history.append(envelope)

        # Si ya hemos acumulado al menos 15 frames de historia, obtener la envolvente 15 frames antes
        if len(envelope_history) > 15:
            # Obtener el valor de la envolvente de 15 frames atrás
            envelope_15_frames_ago = envelope_history[-16][frame]  # -16 porque estamos 15 frames atrás
            print(f"Envolvente 15 frames atrás en el frame {frame}: {envelope_15_frames_ago}")

    else:
        envelope_data = []

    # Actualizar los datos de la gráfica
    ln.set_data(xdata, ydata)
    # Verificar si hay datos para la envolvente antes de intentar graficarla
    if len(envelope_data) > 0:
        envelope_ln.set_data(xdata, envelope_data)

    return ln, envelope_ln

# Animar los datos de la gráfica en tiempo real
ani = animation.FuncAnimation(fig, update, frames=range(timelaps),  # 900 frames para 45 segundos
                              init_func=init, blit=True, interval=50)  # Intervalo de 50ms (20 muestras por segundo)

# Mostrar la gráfica
plt.show()

# Al finalizar, cierra el SPI
spi.close()