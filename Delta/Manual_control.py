from __future__ import print_function
import time
import sys
import delta_sm3300 as d

delta = d.DeltaComm()

print('Ctr+C anytime to switch off power')


def set_parameters():
    try:
        V = float(input('Voltage: '))
        I = float(input('Current: '))
        delta.set_voltage(V)
        delta.set_current(I)
        return 1

    except KeyboardInterrupt:
        time.sleep(1)
        return 0

    except:
        print(sys.exc_info()[0])
        return 0

try:
    state = set_parameters()
    delta.set_state(state)

    while True:
        set_parameters()
        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
            .format(delta.ask_voltage(), delta.ask_current(), delta.ask_power()), end='')

finally:
    delta.set_state(0)
    delta.close_connection()

