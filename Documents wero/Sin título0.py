# -*- coding: utf-8 -*-
"""
Calculo de Filtros Pasa-Bandas
"""

#FORMULA 

import numpy as np

# Valores
fc = 2  # Frecuencia en Hz
R1 = 10000  # Resistencia R1 en ohmios
C1 = C2 = 10e-6  # Capacitancia en faradios

# Despeje de R2
R2 = 1 / ((2 * np.pi * fc) ** 2 * R1 * C1 * C2)

print(R2)

