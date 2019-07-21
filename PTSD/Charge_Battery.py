import time
import sys
import delta_sm3300 as d
delta = d.DeltaComm()

print('\n\n!!! Ctr+C anytime to interrupt power !!!\n\n')

print('Parameters are set for battery pack Emrax (BPE)')


VTC6 = {'max_cell_volt': 4.2, 'min_cell_volt': 2.5, 'nominal_cell_volt': 3.7, 'capacity': 3.1}
BPE = {'series': 160, 'parallel': 8}
SM3300 = {'max_voltage': 600., 'min_voltage': 0., 'max_current': 5.5, 'min_current': 0.}

mode = input('Mode [charge, store]: ')

# class d:
#     def __init__(self):
#         pass
#     def ask_voltage(self):
#         return 394.
#     def set_voltage(self, volt):
#         print('Voltage set to {!s}'.format(volt))
#     def set_state(self, state):
#         print('State set to {!s}'.format(state))
#     def set_current(self, cur):
#         print('Current set to {!s}'.format(cur))
#     def ask_current(self):
#         return 2.5
#     def close_connection(self):
#         print('connection closed')
#
#     def ask_power(self):
#         return 2.5*620
#
# delta = d()


def sanity_check(batt_voltage):
    if BPE['series'] * VTC6['max_cell_volt'] > batt_voltage > 0.95 * BPE['series'] * VTC6['min_cell_volt']:
        return True, batt_voltage
    else:
        return False, batt_voltage


def log(voltage, current, power):
    with open('./power.csv', 'a') as a:
        a.write('{!s},{!s},{!s},{!s},charging\n'.format(time.time(), voltage, current, power))


try:
    check = sanity_check(delta.ask_voltage())
    if check[0]:
        if mode == 'charge':
            v_set = min(BPE['series'] * VTC6['max_cell_volt'], SM3300['max_voltage'])
            I_set = min(BPE['parallel'] * VTC6['capacity'], SM3300['max_current'])

        elif mode == 'store':
            v_set = min(BPE['series'] * VTC6['nominal_cell_volt'], SM3300['max_voltage'])
            I_set = min(BPE['parallel'] * VTC6['capacity'], SM3300['max_current'])

        else:
            print('That mode is not programmed.')
            raise KeyboardInterrupt

        print('\n\nPlease review these parameters:\nTarget voltage: {!s} V\nTarget current: {!s}'
              ' A\n\nBattery pack:\n{!s}S{!s}P\nMax voltage: {!s} V\n\n'.
              format(v_set, I_set, BPE['series'], BPE['parallel'], BPE['series']*VTC6['max_cell_volt']))
        time.sleep(10.)

        if v_set > check[1]:
            delta.set_voltage(v_set)
            delta.set_current(I_set)
            delta.set_state(1)
            time.sleep(1.)
            print('{!s} > {!s}'.format(abs(v_set - delta.ask_voltage()), 0.1))
            print('{!s} > {!s}'.format(delta.ask_current(), 0.1 * BPE['parallel'] *VTC6['capacity']))
            print('{!s} < {!s} < {!s}'.format(0.8 * BPE['series'] * VTC6['min_cell_volt'], delta.ask_voltage(),  1.001 * BPE['series'] * VTC6['max_cell_volt']))

            while abs(v_set - delta.ask_voltage()) > 0.1 and delta.ask_current() > 0.1 * BPE['parallel'] *\
                    VTC6['capacity'] and 0.8 * BPE['series'] * VTC6['min_cell_volt'] < delta.ask_voltage() < \
                    1.001 * BPE['series'] * VTC6['max_cell_volt']:
                log(delta.ask_voltage(), delta.ask_current(), delta.ask_power())
                time.sleep(1.)

        else:
            print('\nBattery voltage higher than requested voltage at {!s} V\n'.format(check[1]))
            raise KeyboardInterrupt

    else:
        print('Sanity check failed. Battery voltage: {!s} V'.format(check[1]))

except:
    error = sys.exc_info()[0]
    print(error)

finally:
    delta.set_state(0)
    delta.close_connection()
