import spidev
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configurar SPI
spi = spidev.SpiDev()
spi.open(1, 2)  # SPI1, CE2
spi.max_speed_hz = 1350000  # Establecer velocidad una vez

# Inicializar la gráfica con Matplotlib
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)

# Configurar los límites del gráfico
timelaps = 2100
ax.set_xlim(0, timelaps)  # 45 segundos (900 muestras, 20 muestras/segundo)
ax.set_ylim(0, 1024)  # Rango de la variable 'lectura' (0-1024)

# Función para leer del ADC
def analogRead(pin):
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    lec = ((adc[1] & 3) << 8) + adc[2]
    return lec

# Función para inicializar la gráfica
def init():
    ln.set_data([], [])
    return ln,

# Función para actualizar los datos de la gráfica
def update(frame):
    lectura = analogRead(0)  # Leer del canal 0 del ADC
    xdata.append(frame)
    ydata.append(lectura)

    # Si ya tenemos más de 900 puntos, eliminamos los más antiguos
    if len(xdata) > timelaps:
        xdata.pop(0)
        ydata.pop(0)

    ln.set_data(xdata, ydata)
    return ln,


# Animar los datos de la gráfica en tiempo real
ani = animation.FuncAnimation(fig, update, frames=range(timelaps),  # 900 frames para 45 segundos
                              init_func=init, blit=True, interval=50)  # Intervalo de 50ms (20 muestras por segundo)

# Mostrar la gráfica
plt.show()

# Al finalizar, cierra el SPI
spi.close()