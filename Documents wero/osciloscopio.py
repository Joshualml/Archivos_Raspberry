import serial
import time
import matplotlib.pyplot as plt
plt.close('all')
# Lista para almacenar datos
datos = []

def main():
    puerto = "COM9"  # Cambiar al puerto correcto
    baud_rate = 9600

    try:
        # Conectar al puerto serial
        arduino = serial.Serial(port=puerto, baudrate=baud_rate, timeout=1)
        print(f"Conectado al puerto {puerto} con baud rate {baud_rate}.")
        
        time.sleep(2)  # Dar tiempo al Arduino para inicializar

        # Configuración del gráfico
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)
        ax.set_xlim(0, 1000)  # Últimos 100 datos
        ax.set_ylim(0, 500)  # Cambiar según el rango esperado
        ax.set_title("Señal Arduino en Tiempo Real")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Valor de la Señal")

        print("Presiona Ctrl+C para detener la lectura.")
        
        # Bucle manual para sincronizar con 5 ms
        start_time = time.time()
        while True:
            try:
                # Leer dato desde el puerto serial
                if arduino.in_waiting > 0:
                    linea = arduino.readline().decode('utf-8').strip()
                    if linea:
                        # print(f"Dato recibido: {linea}")
                        valor = float(linea)
                        datos.append(valor)
                        
                        # Mantener solo los últimos 100 datos
                        if len(datos) > 1000:
                            datos.pop(0)

                        # Actualizar el gráfico
                        line.set_data(range(len(datos)), datos)
                        ax.draw_artist(ax.patch)
                        ax.draw_artist(line)
                        fig.canvas.blit(ax.bbox)
                        fig.canvas.flush_events()

                # Sincronizar con 5 ms
                # time.sleep(max(0, 0.005 - (time.time() - start_time) % 0.005))
                time.sleep(0.001)

            except KeyboardInterrupt:
                print("Lectura detenida por el usuario.")
                break

    except serial.SerialException as e:
        print(f"Error de conexión: {e}")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("Conexión serial cerrada.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
