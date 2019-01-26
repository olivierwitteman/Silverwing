# !!! Run as python3 !!!

# from __future__ import print_function
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math

# path = '.'
path = '/home/pi/Silverwing/BTS'


class ADC:

    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1015(i2c)

        # Create single-ended input on channel 0
        self.chan = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2), AnalogIn(ads, ADS.P3)]

    def calibration(self, v0):
        a = -0.8439588476E-3
        b = 4.036819533E-4
        c = -3.081516640E-7

        r = -v0*100e3/(v0-3.3)

        T = 1./(a + b * math.log(r) + c * (math.log(r))**3) - 273.15

        return T, r

    def pack_temp(self, input0=2):
        v0 = lc.chan[input0].voltage
        return self.calibration(v0)

    # def ambient_temp(self):
    #     with open('/home/pi/Silverwing/General/ambient.temp', 'r') as t:
    #         raw = t.read()
    #         try:
    #             t_f = float(raw.split(',')[0])
    #             value = float(raw.split(',')[1])
    #             t = time.time()
    #             if t - t_f > 10.:
    #                 value = 'Outdated'
    #             t0 = time.time()
    #         except:
    #             value = 20
    #             # if time.time() - t0 > 10.:
    #             #     value = 'Outdated'
    #
    #         return value

    def log_temp(self, c_temp):
        with open('/home/pi/Silverwing/BTS/data/pack.temp', 'w') as d:
            d.write('{!s},{!s}'.format(time.time(), c_temp))


lc = ADC()

while True:
    ts, rs = [], []
    for _ in range(10):
        t, r = lc.pack_temp()
        ts.append(t)
        rs.append(r)
        time.sleep(0.05)
    t_av = sum(ts)/len(ts)
    r_av = sum(rs)/len(rs)
    # t_a = lc.ambient_temp()

    lc.log_temp(t_av)

    # print('T pack: {!s}C, T ambient: {!s}C, R: {!s}kOhm'.format(round(t_av, 5), round(t_a, 5), round(r_av), end=""))
    time.sleep(1)


