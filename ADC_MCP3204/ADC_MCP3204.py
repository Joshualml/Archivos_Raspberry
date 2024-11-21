import spidev
from time import sleep
import RPi.GPIO as GPIO

# Configurar SPI
spi = spidev.SpiDev()
spi.open(1, 2)  # SPI1, CE2
spi.max_speed_hz = 1350000  # Establecer velocidad una vez

# Si no usas GPIO, puedes omitir esta línea
GPIO.setmode(GPIO.BOARD)

def analogRead(pin):
    # Leer del canal ADC
    adc = spi.xfer2([1, (8 + pin) << 4, 0])
    lec = ((adc[1] & 3) << 8) + adc[2]
    return lec

try:
    while True:
        #lectura voltaje de referencia
        #referencia = analogRead(3)
        #referencia = referencia * 3.3 / 1024
        #print("referencia: ", referencia)

        #lectura sensor
        lectura = analogRead(0)
        #voltage = (lectura * 2.5) / 1024
        valor = lectura * 2650 / 1024 / 50
        Pascales = 0.2 * valor -4

        #print(f"Sensor: {voltage}, Referencia: {referencia}")
        print(("sensor: ", Pascales, "ref: ", 0, "max: ", 10))
        #print("")
        #print("")
        sleep(0.050)
finally:
    spi.close()  # Cerrar SPI cuando termines