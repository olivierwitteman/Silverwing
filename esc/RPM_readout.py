from __future__ import print_function
import pigpio
import time

import os
os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)

pi = pigpio.pi()
dt = 1.
poles = 28.


def get_tally(pin):
    t0 = time.time()
    cb3 = pi.callback(pin)
    time.sleep(dt)
    edges = cb3.tally()
    t1 = time.time()
    rpm = int(edges * 60. * 2. / ((t1 - t0) * poles))
    cb3.reset_tally()
    return rpm

try:
    while True:
        rpm0 = get_tally(13)
        rpm1 = get_tally(16)

        with open('/home/pi/Silverwing/esc/actual0.rpm', 'w') as d:
            d.write(str(rpm0))
        with open('/home/pi/Silverwing/esc/actual1.rpm', 'w') as d:
            d.write(str(rpm1))
        # print('\rM0: {!s} RPM, M1: {!s} RPM'.format(rpm0, rpm1), end='')


finally:
    pi.stop()
