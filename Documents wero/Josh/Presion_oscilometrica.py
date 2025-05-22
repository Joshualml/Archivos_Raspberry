# -*- coding: utf-8 -*-
"""
Created on Tue May  6 13:10:17 2025

@author: joshu
"""

import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv("senal_oscilometrica_realista.csv")

# Graficar
plt.figure(figsize=(12, 6))
plt.plot(df["Time (s)"], df["Pressure (mmHg)"], label="Señal oscilométrica", color='green')
plt.title("Señal Oscilométrica de Presión Arterial (Simulada)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Presión (mmHg)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
