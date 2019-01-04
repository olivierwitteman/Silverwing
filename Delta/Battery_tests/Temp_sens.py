import time
from ds18b20 import DS18B20  # pip ds18b20
import sys

sensor = DS18B20()


def get_temp():
    temp = float(sensor.get_temperature(DS18B20.DEGREES_C))
    return temp


def log_temp(c_temp):
    with open('/home/pi/Silverwing/battery_tests/data/current.temp', 'w') as d:
        d.write('{!s},{!s}'.format(time.time(), c_temp))


while True:
    try:
        t = get_temp()
        log_temp(t)
        # log_temp(20.)
    except:
        print('Error getting temperature: {!s}'.format(sys.exc_info()[0]))

    time.sleep(1.)