import spidev
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.signal import find_peaks

# Configurar SPI
spi = spidev.SpiDev()  # Crear un objeto SPI
spi.open(1, 0)         # Conectar al bus SPI 0, dispositivo CE0
spi.max_speed_hz = 1350000  # Configurar velocidad SPI (1.35 MHz)

# Función para leer un canal específico del MCP3204
def read_mcp3204(channel):
    if channel < 0 or channel > 3:
        raise ValueError("El canal debe estar entre 0 y 3")
    
    # Comando para el MCP3204: Start bit + Single/Diff + D2, D1, D0
    cmd = [1, (8 + channel) << 4, 0]
    adc_response = spi.xfer2(cmd)  # Enviar el comando y recibir la respuesta
    result = ((adc_response[1] & 3) << 8) + adc_response[2]  # Procesar la respuesta a un valor de 12 bits
    return result

# Variables para graficar
xdata, ydata, env_data = [], [], []
timelaps = 600  # Número de muestras para mostrar en la gráfica

# Variables dinámicas para ajustar el umbral 'height'
initial_values = []  # Para almacenar los valores iniciales cuando no hay señal activa
dynamic_height = 300  # Umbral inicial de 'height'

# Inicializar la figura
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label="Señal ECG")
env_line, = ax.plot([], [], 'r-', label="Envolvente (Picos)")

# Configurar la gráfica
ax.set_xlim(0, timelaps)
ax.set_ylim(0, 4095)  # Rango para 12 bits
ax.set_title("Señal ECG y Envolvente")
ax.set_xlabel("Muestras")
ax.set_ylabel("Valor")
ax.legend()

# Función de inicialización
def init():
    line.set_data([], [])
    env_line.set_data([], [])
    return line, env_line

# Función para actualizar la gráfica
def update(frame):
    global dynamic_height, initial_values

    # Leer el canal 4 (índice 3)
    value = read_mcp3204(3)
    xdata.append(frame)
    ydata.append(value)

    # Mantener el tamaño de los datos en el rango de timelaps
    if len(xdata) > timelaps:
        xdata.pop(0)
        ydata.pop(0)

    # Establecer el umbral dinámico solo con los primeros 100 valores
    if len(initial_values) < 100:  # Usamos los primeros 100 valores para calcular el umbral
        initial_values.append(value)
    elif len(initial_values) == 100:  # Solo se calcula una vez
        # Calcular el umbral dinámico como un valor por encima de la media de los primeros valores
        dynamic_height = np.mean(initial_values) * 1.1  # Ajuste el 1.1 según la sensibilidad que necesites

    # Aplicar filtro pasabajo a la señal
    if len(ydata) > 9:  # Compara con el tamaño del filtro (padlen)
        smoothed_signal = butter_lowpass_filter(ydata, cutoff=3, fs=500)  # Ajusta según sea necesario
    else:
        smoothed_signal = np.array(ydata)

    # Detectar los picos máximos de la señal suavizada
    peaks, _ = find_peaks(smoothed_signal, height=dynamic_height)  # Utilizar el umbral dinámico

    # Crear la envolvente basada en los picos detectados
    env_signal = np.zeros_like(smoothed_signal)
    env_signal[peaks] = smoothed_signal[peaks]  # Asignar los valores de los picos detectados

    # Mantener el tamaño de los datos de la envolvente
    env_data.append(env_signal[-1])  # Agregar la última parte de la envolvente
    if len(env_data) > timelaps:
        env_data.pop(0)

    # Actualizar los gráficos
    line.set_data(xdata, ydata)  # Señal original
    env_line.set_data(xdata, env_data)  # Envolvente (picos)
    return line, env_line

# Animar la gráfica en tiempo real
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, timelaps), init_func=init, blit=True, interval=50)

# Mostrar la gráfica
plt.tight_layout()
plt.show()

# Cerrar el SPI al finalizar
spi.close()
