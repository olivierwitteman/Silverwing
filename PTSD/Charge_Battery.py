import time
import sys
import delta_sm3300 as d
import statistics
delta = d.DeltaComm()

print('\n\n!!! Ctr+C anytime to interrupt power !!!\n\n')

print('Parameters are set for battery pack Emrax (BPE)')


VTC6 = {'max_cell_volt': 4.2, 'min_cell_volt': 2.5, 'nominal_cell_volt': 3.7, 'capacity': 3.1}
BPE = {'series': 160, 'parallel': 8, 'target_voltage': 640}
SM3300 = {'max_voltage': 660., 'min_voltage': 0., 'max_current': 5., 'min_current': 0.}

mode = input('Mode [charge, store, fully charge]: ')


def sanity_check(batt_voltage):
    if BPE['series'] * VTC6['max_cell_volt'] > batt_voltage > 0.95 * BPE['series'] * VTC6['min_cell_volt']:
        return True, batt_voltage
    else:
        return False, batt_voltage


def log(voltage, current, power):
    with open('./power.csv', 'a') as a:
        a.write('{!s},{!s},{!s},{!s},charging\n'.format(time.time(), voltage, current, power))


def filt_current():
    ilst = []
    for _ in range(10):
        ilst.append(delta.ask_current())
    return statistics.median(ilst)


def filt_voltage():
    vlst = []
    for _ in range(10):
        vlst.append(delta.ask_voltage())
    return statistics.median(vlst)


try:
    check = sanity_check(delta.ask_voltage())
    if check[0]:
        if mode == 'charge':
            # v_set = min(BPE['series'] * VTC6['max_cell_volt'], SM3300['max_voltage'])
            v_set = BPE['target_voltage']
            I_set = min(BPE['parallel'] * VTC6['capacity'], SM3300['max_current'])

        elif mode == 'store':
            v_set = min(BPE['series'] * VTC6['nominal_cell_volt'], SM3300['max_voltage'])
            I_set = min(BPE['parallel'] * VTC6['capacity'], SM3300['max_current'])

        elif mode == 'fully charge':
            v_set = min(BPE['series'] * VTC6['max_cell_volt'], SM3300['max_voltage'])
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
            time.sleep(10.)
            while filt_current() > 0.005 * BPE['parallel'] *\
                    VTC6['capacity'] and 0.8 * BPE['series'] * VTC6['min_cell_volt'] < filt_voltage() < \
                    1.005 * BPE['series'] * VTC6['max_cell_volt']:
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
