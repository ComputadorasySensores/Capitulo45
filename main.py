import machine, network, time, urequests
from machine import Pin, I2C
import bme280_float

ssid = 'Coloca tu nombre de red'
password = 'tu password'
url = "https://api.thingspeak.com/update?api_key=TU WRITE API KEY"

red = network.WLAN(network.STA_IF)

red.active(True)
red.connect(ssid, password)

while red.isconnected() == False:
  pass

print('Conexión correcta')
print(red.ifconfig())

ultima_peticion = 0
intervalo_peticiones = 30

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bme = bme280_float.BME280(i2c=i2c)

def reconectar():
    print('Fallo de conexión. Reconectando...')
    time.sleep(10)
    machine.reset()

while True:
    try:
        if (time.time() - ultima_peticion) > intervalo_peticiones:
            temperatura, presion, humedad = bme.read_compensated_data()
            temp = round(temperatura, 1)
            hum = round(humedad, 1)
            pres = round(presion/100, 1)
            print(bme.values)
            respuesta = urequests.get(url + "&field1=" + str(temp) + "&field2=" + str(hum) + "&field3=" + str(pres))
            print ("Respuesta: " + str(respuesta.status_code))
            respuesta.close ()
            ultima_peticion = time.time()
    except OSError as e:
        reconectar()
