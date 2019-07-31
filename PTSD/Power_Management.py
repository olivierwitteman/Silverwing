import time
import delta_sm3300 as d
delta = d.DeltaComm()

print('\n\n!!! Ctr+C anytime to switch off power !!!\n\n')

# V_set = 120.
V_set = float(input('Voltage [V] (0-672): '))
I_max = float(input('Current [A] (0-300): '))

if V_set > 60.:
    print('\n\nYou have entered a high voltage, make sure you follow the guidelines for safety!\n\n')
    time.sleep(5.)
    print('Engaging HV')

pre_I = 5.
# I = 15000./V


def log(voltage, current, power):
    with open('./power.csv', 'a') as a:
        a.write('{!s},{!s},{!s},{!s}\n'.format(time.time(), voltage, current, power))


def precharge():
    print('Precharging...')
    # delta.enable_watchdog()
    delta.set_voltage(V_set)
    delta.set_current(min(pre_I, I_max))
    delta.set_state(1)

    t0_pre, t = time.time(), time.time()

    while t - t0_pre < 5.:
        print('\rPrecharge Voltage: {!s}, precharge current: {!s}, precharge power: {!s}'.format(round(delta.ask_voltage(), 2),
                                                                          round(delta.ask_current(), 2),
                                                                          round(delta.ask_power(), 2)), end='')

        time.sleep(0.1)
        t = time.time()

    if abs(delta.ask_voltage() - V_set) < 60.:
        precharged = True
        delta.set_current(I_max)
        print('\r', end='')
    else:
        delta.set_state(0)
        print('\n\nPrecharging failed\n\n')
        precharged = False
        raise KeyboardInterrupt
    return precharged


def discharge():
    delta.set_state(0)
    print('\nDischarging...\n')
    while delta.ask_voltage() > 10.:
        vlst, ilst, plst = [], [], []
        for _ in range(10):
            vlst.append(delta.ask_voltage())
            ilst.append(delta.ask_current())
            plst.append(delta.ask_power())
        u = sum(vlst) / len(vlst)
        i = sum(ilst) / len(ilst)
        p = sum(plst) / len(plst)
        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}'.format(round(u, 2), round(i, 2), round(p, 2)),
              end='')
        log(u, i, p)
        time.sleep(0.2)

    print('\nSuccessfully discharged.\n')


def monitor():
    print('\n\n\n')
    while True:
        vlst, ilst, plst = [], [], []
        for _ in range(10):
            vlst.append(delta.ask_voltage())
            ilst.append(delta.ask_current())
            plst.append(delta.ask_power())

        u = sum(vlst)/len(vlst)
        i = sum(ilst)/len(ilst)
        p = sum(plst)/len(plst)

        print('\rVoltage: {!s}, actual current: {!s}, power: {!s}'.format(round(u, 2), round(i, 2), round(p, 2)), end='')

        log(u, i, p)
        time.sleep(0.2)


try:
    precharge()
    monitor()


finally:
    discharge()
    delta.close_connection()

