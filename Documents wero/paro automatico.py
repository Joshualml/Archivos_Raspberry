# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 14:18:22 2025

@author: mater
"""

# -*- coding: utf-8 -*-
import tkinter as tk
import serial
import time
import threading  # Importa la librería threading para crear hilos

# Configurar la conexión serial con el Arduino (ajusta el puerto según corresponda)
arduino = serial.Serial('COM4', 115200)  # En Windows puede ser COM3, en Linux /dev/ttyACM0
time.sleep(2)  # Esperar que se establezca la conexión


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