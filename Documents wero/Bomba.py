# -*- coding: utf-8 -*-
import tkinter as tk
import serial
import time

# Configurar la conexión serial con el Arduino (ajusta el puerto según corresponda)
arduino = serial.Serial('COM4', 9600)  # En Windows puede ser COM3, en Linux /dev/ttyACM0
time.sleep(2)  # Esperar que se establezca la conexión

# Función para encender la bomba
def encender_bomba():
    arduino.write(b'1')  # Enviar '1' al Arduino para encender la bomba
    print("Bomba encendida")

# Función para apagar la bomba
def apagar_bomba():
    arduino.write(b'0')  # Enviar   '0' al Arduino para apagar la bomba
    print("Bomba apagada")

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Bomba de Aire")

# Crear un botón para encender la bomba
boton_encender = tk.Button(root, text="Encender Bomba", command=encender_bomba)
boton_encender.pack(pady=10)

# Crear un botón para apagar la bomba
boton_apagar = tk.Button(root, text="Apagar Bomba", command=apagar_bomba)
boton_apagar.pack(pady=10)

# Iniciar el loop de la interfaz gráfica
root.mainloop()

# Cerrar la conexión serial al salir
arduino.close()


