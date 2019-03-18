# !!! Run as python3 !!!
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math
import subprocess


# path = '.'
path = '/home/pi/Silverwing/BTS'
# pat = subprocess.Popen(['python', '/home/pi/Silverwing/General/Temp_sens.py'])  # ESC daemon


class ADC:

    def __init__(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1015(i2c)

        # Create single-ended input on channel 0
        self.chan = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2), AnalogIn(ads, ADS.P3)]

    def calibration(self, v0):
        a = -0.1809802231E-3
        b = 3.319163836E-4
        c = -1.868674690E-7

        r = -v0*100e3/(v0-3.3)

        T = 1./(a + b * math.log(r) + c * (math.log(r))**3) - 273.15

        return T, r

    def pack_temp(self):
        v0 = lc.chan[2].voltage
        v3 = lc.chan[3].voltage
        v1 = lc.chan[1].voltage
        dv = abs(v3-v1)*503./33.

        T, r = self.calibration(v0)
        return T, r, dv

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

    def log_voltage(self, voltage):
        with open('/home/pi/Silverwing/BTS/data/pack.voltage', 'w') as d:
            d.write('{!s},{!s}'.format(time.time(), voltage))


lc = ADC()

try:
    while True:
        ts, rs, vs = [], [], []
        for _ in range(10):
            t, r, v = lc.pack_temp()
            ts.append(t)
            rs.append(r)
            vs.append(v)
            time.sleep(0.05)
        t_av = sum(ts)/len(ts)
        r_av = sum(rs)/len(rs)
        v_av = sum(vs)/len(vs)
        # t_a = lc.ambient_temp()

        lc.log_temp(t_av)
        lc.log_voltage(v_av)
        print(t_av)
        # print(r_av)
        # print(lc.ambient_temp())
        # print('\n\n------\n\n')
        # print(v_av)
        time.sleep(1)

finally:
    # pat.terminate()
    pass