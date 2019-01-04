# !!! Run as python3 !!!

# from __future__ import print_function
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# path = '.'
path = '/home/pi/Silverwing/WaTT'


class LoadCells:

    def __init__(self):
        self.g = 9.80665
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1015(i2c)

        # Create single-ended input on channel 0
        self.chan = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2), AnalogIn(ads, ADS.P3)]

    def calibration(self, v0, v1):
        self.a0, self.b0 = -4.84931506849, 2.04
        self.a1, self.b1 = -6.80769230769, 2.02

        f0 = self.g * ((v0 - self.b0) * self.a0)
        f1 = self.g * ((v1 - self.b1) * self.a1)

        return f0, f1

    def forces(self, input0=2, input1=3):
        v0, v1 = lc.chan[input0].voltage, lc.chan[input1].voltage
        return self.calibration(v0, v1)

    def log(self, timestamp, f0, f1, a0, b0, a1, b1):
        with open('{!s}/for.ces'.format(path), 'w') as logfile:
            logfile.writelines('{!s},{!s},{!s},{!s},{!s},{!s},{!s}\n'.format(timestamp, f0, f1, a0, b0, a1, b1))


lc = LoadCells()

while True:
    f0s, f1s = [], []
    for _ in range(10):
        f0, f1 = lc.forces()
        f0s.append(f0)
        f1s.append(f1)
        time.sleep(0.1)
    f0 = sum(f0s)/len(f0s)
    f1 = sum(f1s)/len(f1s)
    lc.log(time.time(), f0, f1, lc.a0, lc.b0, lc.a1, lc.b1)

    # print('f0: {!s}N, f1: {!s}N'.format(round(f0, 2), round(f1, 2)), end="")
    time.sleep(0)


