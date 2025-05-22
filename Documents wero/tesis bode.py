import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, bode

# Parámetros del filtro pasa altas
fc_high = 0.6  # Frecuencia de corte en Hz
Q_high = 0.707  # Factor de calidad
wc_high = 2 * np.pi * fc_high  # Frecuencia angular de corte

# Coeficientes de la función de transferencia pasa altas
num_high = [1, 0, 0]  # Numerador (s^2)
den_high = [1, wc_high / Q_high, wc_high**2]  # Denominador (s^2 + wc/Q * s + wc^2)

# Parámetros del filtro pasa bajas
fc_low = 6  # Frecuencia de corte en Hz
Q_low = 0.707  # Factor de calidad
wc_low = 2 * np.pi * fc_low  # Frecuencia angular de corte

# Coeficientes de la función de transferencia pasa bajas
num_low = [wc_low**2]  # Numerador (wc^2)
den_low = [1, wc_low / Q_low, wc_low**2]  # Denominador (s^2 + wc/Q * s + wc^2)

# Crear las funciones de transferencia
tf_high = TransferFunction(num_high, den_high)
tf_low = TransferFunction(num_low, den_low)

# Frecuencias para el análisis
w = np.logspace(-1, 2, 1000)  # De 0.1 Hz a 100 Hz (frecuencia angular)

# Obtener la respuesta en magnitud y fase
w_high, mag_high, phase_high = bode(tf_high, w=w)
w_low, mag_low, phase_low = bode(tf_low, w=w)

# Convertir frecuencia angular a frecuencia en Hz
freq_high = w_high / (2 * np.pi)
freq_low = w_low / (2 * np.pi)

# Límites para las gráficas
x_limits = [0.4, 10]  # Límites del eje X (frecuencia en Hz)
y_limits_mag = [-5, 5]  # Límites del eje Y para la magnitud (dB)
y_limits_phase = [-180, 180]  # Límites del eje Y para la fase (grados)

# Gráfica de la respuesta de magnitud
plt.figure(figsize=(10, 6))
plt.semilogx(freq_high, mag_high, label="Filtro pasa altas (0.6 Hz)")
plt.semilogx(freq_low, mag_low, label="Filtro pasa bajas (6 Hz)")
plt.axvline(fc_high, color="r", linestyle="--", label="Frecuencia de corte (0.6 Hz)")
plt.axvline(fc_low, color="g", linestyle="--", label="Frecuencia de corte (6 Hz)")
plt.axhline(-3, color="gray", linestyle="--", label="-3 dB")

# Etiquetas de intersección
# Para el filtro pasa altas
idx_high = np.argmin(np.abs(freq_high - fc_high))
plt.annotate(
    f"({freq_high[idx_high]:.2f}, {mag_high[idx_high]:.2f})",
    xy=(fc_high, mag_high[idx_high]),
    xytext=(fc_high + 0.2, mag_high[idx_high] + 5),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=10,
    color="red",
)

# Para el filtro pasa bajas
idx_low = np.argmin(np.abs(freq_low - fc_low))
plt.annotate(
    f"({freq_low[idx_low]:.2f}, {mag_low[idx_low]:.2f})",
    xy=(fc_low, mag_low[idx_low]),
    xytext=(fc_low +0.4, mag_low[idx_low] + 5),
    arrowprops=dict(facecolor="black", arrowstyle="->"),
    fontsize=10,
    color="green",
)

plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud (dB)")
plt.title("Respuesta en Magnitud de los Filtros")
plt.xlim(x_limits)
plt.ylim(y_limits_mag)
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()
# Gráfica de la respuesta de fase
plt.figure(figsize=(10, 6))
plt.semilogx(freq_high, phase_high, label="Filtro pasa altas (0.6 Hz)")
plt.semilogx(freq_low, phase_low, label="Filtro pasa bajas (6 Hz)")
plt.axvline(fc_high, color="r", linestyle="--", label="Frecuencia de corte (0.6 Hz)")
plt.axvline(fc_low, color="g", linestyle="--", label="Frecuencia de corte (6 Hz)")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Fase (grados)")
plt.title("Respuesta en Fase de los Filtros")
plt.xlim(x_limits)
plt.ylim(y_limits_phase)
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.show()

