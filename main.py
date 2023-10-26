import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO-Pin, an den der Sensor angeschlossen ist

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print(f'Temperatur: {temperature:.2f}°C, Luftfeuchtigkeit: {humidity:.2f}%')
else:
    print('Fehler beim Auslesen des Sensors')