from __future__ import print_function
import time
# import delta_sm3300 as d
import Delta_comm as d

delta = d.DeltaComm()

print('Ctr+C anytime to exit')


def get_data():
    V = round(delta.ask_voltage(), 1)
    I = round(delta.ask_current(), 1)
    P = round(delta.ask_power(), 1)
    return V, I, P


try:
    while True:
        V, I, P = get_data()
        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
            .format(V, I, P), end="")
        time.sleep(0.1)

finally:
    delta.close_connection()

