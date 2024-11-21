import tkinter as tk
import serial
import time
import spidev
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Configura el puerto serial para la comunicación con el Arduino en el puerto COM3
arduino = serial.Serial('/dev/serial0', 9600, timeout=1)
time.sleep(2)  # Espera a que se establezca la conexión serial

##########################################################################################################
###########################################################################################################

def activar_bomba():
    """Envía el comando para activar la bomba"""
    if arduino.isOpen():
        print("Activando bomba...")
        arduino.write(b'1')  # Envía el comando '1' para activar la bomba en el Arduino
        time.sleep(0.1)
        verificar_estado()

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
    """Envía el comando para activar la función extra"""
    if arduino.isOpen():
        print("Desactivando Bomba")
        arduino.write(b'2')  # Envía el comando '2' para activar la función extra en el Arduino
        time.sleep(0.1)

def cerrar():
    """Cierra la conexión serial y la interfaz"""
    arduino.close()
    root.destroy()
    print("Conexión serial cerrada y aplicación terminada.")

##########################################################################################################
###########################################################################################################


##########################################################################################################
###########################################################################################################


# Configurar SPI
spi = spidev.SpiDev()
spi.open(1, 2)  # Ajusta según tu configuración de SPI (por ejemplo, SPI0, CE0)
spi.max_speed_hz = 1350000  # Establecer velocidad adecuada para el MCP3204

# Inicializar la figura y dos subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # 2 filas, 1 columna

# Inicializar datos para los canales
xdata, ydata_ch1, ydata_ch2 = [], [], []
ln1, = ax1.plot([], [], 'r-', animated=True, label="CH1")
ln2, = ax2.plot([], [], 'b-', animated=True, label="CH2")

# Configurar límites de los gráficos
timelaps = 700
for ax in (ax1, ax2):
    ax.set_xlim(0, timelaps)  # Rango de tiempo
    ax.set_ylim(0, 1024)  # Rango de 12 bits para el MCP3204 (0-4095)

ax1.set_title("Señal del Canal 1")
ax2.set_title("Señal del Canal 2")

# Configuración de la interfaz gráfica en pantalla completa sin bordes
root = tk.Tk()
root.attributes("-fullscreen", True)  # Modo pantalla completa
root.configure(bg="black")  # Fondo negro opcional para mejor contraste

# Configura el tamaño de fuente y estilo de los botones
button_font = ("Arial", 32, "bold")  # Fuente grande para los botones

# Botón para activar la bomba
boton_activar = tk.Button(root, text="Activar Bomba", font=button_font, command=activar_bomba, bg="green", fg="white")
boton_activar.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Llena toda la pantalla

# Botón para activar la función extra
boton_funcion_extra = tk.Button(root, text="Desactivador de emergencia", font=button_font, command=funcion_extra, bg="blue", fg="white")
boton_funcion_extra.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Llena toda la pantalla

# Botón para cerrar la aplicación
boton_salir = tk.Button(root, text="Salir", font=button_font, command=cerrar, bg="red", fg="white")
boton_salir.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Llena toda la pantalla

# Iniciar el bucle de la interfaz gráfica
root.mainloop()