import time
import sys
import delta_sm3300 as d

delta = d.DeltaComm()

print('Ctr+C anytime to switch off power')

# V_set = 120.
V_set = float(input('Voltage: '))

if V_set > 60.:
    print('\n\nYou have entered a high voltage, make sure you follow the guidelines for safety!\n\n')
    time.sleep(5.)
    print('Engaging HV')

pre_I = 2.
# I = 15000./V
I_max = 5.5

precharged = False


def precharge():
    print('Precharging...')
    delta.set_voltage(V_set)
    delta.set_current(pre_I)
    delta.set_state(1)
    time.sleep(2.5)
    if abs(delta.ask_voltage() - V_set) < 40.:
        precharged = True
        delta.set_current(I_max)
    else:
        delta.set_state(0)
        print('\n\nPrecharging failed\n\n')
        precharged = False
        raise KeyboardInterrupt
    return precharged


def monitor():
    while True:
        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
          .format(delta.ask_voltage(), delta.ask_current(), delta.ask_power()), end='')
        time.sleep(0.2)


try:
    precharge()
    monitor()


finally:
    delta.set_state(0)
    delta.close_connection()

