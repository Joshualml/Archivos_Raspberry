import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV en un DataFrame de pandas
data1 = pd.read_csv("grafica1.csv")
data2 = pd.read_csv("grafica2.csv")

# Graficar los datos
plt.figure(figsize=(10, 5))

# Gráfica para el primer archivo
plt.subplot(2, 1, 1)
plt.plot(data1["Valor"], label="Canal 1")
plt.title("Datos del Canal 1")
plt.xlabel("Muestras")
plt.ylabel("Valor")
plt.legend()

# Gráfica para el segundo archivo
plt.subplot(2, 1, 2)
plt.plot(data2["Valor"], label="Canal 2", color="orange")
plt.title("Datos del Canal 2")
plt.xlabel("Muestras")
plt.ylabel("Valor")
plt.legend()

# Mostrar la gráfica
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import interp1d

# Cargar datos desde el archivo CSV
data1 = np.loadtxt("grafica1.csv", delimiter=",", skiprows=1)  # Saltar la cabecera

# Crear un vector de tiempo según el tamaño de los datos
t = np.arange(len(data1))

# Detectar picos en la señal
peaks, _ = find_peaks(data1)
peak_values = data1[peaks]

# Interpolación de los picos para obtener la envolvente
f_interp = interp1d(t[peaks], peak_values, kind='cubic', fill_value="extrapolate")
envelope = f_interp(t)

# Graficar la señal original y su envolvente
plt.plot(t, data1, label="Señal original")
plt.plot(t, envelope, label="Envolvente (Interpolación de Picos)", color="orange")
plt.title("Señal y su Envolvente usando Interpolación de Picos")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.legend()
plt.show()