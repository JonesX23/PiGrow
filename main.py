import Adafruit_DHT
import RPi.GPIO as GPIO
import time



## Sensor Feuchtigkeit + Temperatur

sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO-Pin, an den der Sensor angeschlossen ist

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print(f'Temperatur: {temperature:.2f}°C, Luftfeuchtigkeit: {humidity:.2f}%')
else:
    print('Fehler beim Auslesen des Sensors')



## Lichtsteuerung





## Lüftersteuerung

import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# Sensor konfigurieren
sensor = Adafruit_DHT.DHT22
sensor_pin = 4  # GPIO-Pin, an den der Sensor angeschlossen ist

# Lüfter konfigurieren
fan_pin = 18  # GPIO-Pin, an den der Lüfter angeschlossen ist
fan_speed = 60 # Anfangsgeschwindigkeit der Lüfter (0-100%)

# Temperatur- und Luftfeuchtigkeitsgrenzwerte für den Lüfterbetrieb
temperature_threshold = 25.0  # in Grad Celsius
humidity_threshold = 65.0  # in Prozent

# Lüftersteuerungsfunktion
def control_fan(temperature, humidity):
    if temperature > temperature_threshold or humidity > humidity_threshold:
        # Falls die Temperatur oder Luftfeuchtigkeit den Schwellenwert überschreitet, schalte den Lüfter ein
        fan_speed = 100  # Maximale Geschwindigkeit
        GPIO.output(fan_pin, GPIO.HIGH)
    else:
        # Andernfalls schalte den Lüfter aus
        fan_speed = 60
        GPIO.output(fan_pin, GPIO.LOW)

# GPIO initialisieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT)

try:
    while True:
        # Sensorwerte auslesen
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

        if humidity is not None and temperature is not None:
            # Lüfter steuern basierend auf den aktuellen Sensorwerten
            control_fan(temperature, humidity)
            print(f'Temperatur: {temperature:.2f}°C, Luftfeuchtigkeit: {humidity:.2f}%, Lüftergeschwindigkeit: {fan_speed}%')
        else:
            print('Fehler beim Auslesen des Sensors')

        time.sleep(180)  # Alle 180 Sekunden aktualisieren

except KeyboardInterrupt:
    pass

# GPIO aufräumen
GPIO.cleanup()
