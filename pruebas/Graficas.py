import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV en un DataFrame de pandas
data1 = pd.read_csv("grafica8.csv")
data2 = pd.read_csv("grafica9.csv")

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
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV en un DataFrame de pandas
data1 = pd.read_csv("grafica8.csv")
data2 = pd.read_csv("grafica9.csv")

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