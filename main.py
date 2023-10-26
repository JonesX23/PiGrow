import RPi.GPIO as GPIO
import Adafruit_DHT
import sqlite3
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


# Sensor konfigurieren
sensor = Adafruit_DHT.DHT22
sensor_pin = 4  # GPIO-Pin, an den der Sensor angeschlossen ist

# Datenbank erstellen und Verbindung herstellen
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# Datenbanktabelle erstellen, falls sie nicht vorhanden ist
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                  (timestamp DATETIME, temperature NUMERIC, humidity NUMERIC)''')
conn.commit()

try:
    while True:
        # Sensorwerte auslesen
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

        if humidity is not None and temperature is not None:
            # Aktuelles Datum und Uhrzeit abrufen
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            # Daten in die Datenbank einfügen
            cursor.execute("INSERT INTO sensor_data (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                           (timestamp, temperature, humidity))
            conn.commit()

            print(f'Temperatur: {temperature:.2f}°C, Luftfeuchtigkeit: {humidity:.2f}%, Zeitstempel: {timestamp}')
        else:
            print('Fehler beim Auslesen des Sensors')

        time.sleep(60)  # Alle 60 Sekunden aktualisieren

except KeyboardInterrupt:
    print("Programm beendet.")
    conn.close()
