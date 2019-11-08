from __future__ import print_function
import time
import delta_sm3300 as d
# import Delta_comm as d

delta = d.DeltaComm()

print('Ctr+C anytime to exit')


def get_data():
    vlst, ilst, plst = [], [], []
    for _ in range(10):
        vlst.append(delta.ask_voltage())
        ilst.append(delta.ask_current())
        plst.append(delta.ask_power())

    u = sum(vlst) / len(vlst)
    i = sum(ilst) / len(ilst)
    p = sum(plst) / len(plst)

    V = round(u, 1)
    I = round(i, 1)
    P = round(p, 1)
    log(V, I, P)

    return V, I, P


def log(voltage, current, power):
    with open('./power.csv', 'a') as a:
        a.write('{!s},{!s},{!s},{!s}\n'.format(time.time(), voltage, current, power))


try:
    while True:
        V, I, P = get_data()
        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
            .format(V, I, P), end="")
        time.sleep(0.1)

finally:
    delta.close_connection()

