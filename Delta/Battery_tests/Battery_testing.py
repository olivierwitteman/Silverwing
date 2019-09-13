import time
import RPi.GPIO as gp
import delta_sm3300 as d
import subprocess

# TODO: Temp_sens moved to general
pat = subprocess.Popen(['python', '/home/pi/Silverwing/General/Temp_sens.py'])  # ESC daemon

delta = d.DeltaComm()

safe_operation = False
capacity = float(input('Capacity [Ah]: '))
# crate_dischar = [(6., 80), (1.71, 1080), (6., 40), (1.71, 0)]
power_per_cell_target = float(input('Power per cell target [W]: '))
target_temp = float(input('Target cell temperature [C]: '))
discharge_time = int(input('Discharge time [s]: '))

crate_dischar = 10 * [(power_per_cell_target/(capacity * 3.7), discharge_time)]
# (C, duration [s]) duration=0 for full discharge
name = '{!s}_t{!s}_T{!s}_P{!s}'.format(input('Cell name: '), discharge_time, target_temp, power_per_cell_target)
print(name)
minvolt = 2.5  # OCV
# R_sys = 0.03

max_cell_temp = 80.

pin = 4
gp.setmode(gp.BCM)
gp.setwarnings(False)
gp.setup(pin, gp.OUT)

if not safe_operation:
    print('\n\nWARNING, lowered cutoff voltage to allow for higher discharge rate. Do not leave this process ' \
          'unattended.\n\nBattery degradation will be accelerated in this mode.')
maxvolt, series, parallel, crate_char = 4.2, 1, 1, 0.7
R_sys = 0.33/40. + 0.0128 * series/parallel
print('Please review below parameters carefully within 60 seconds.\n\nMaximum cell voltage: {!s}V\nMinimum cell '
      'voltage: {!s}V\nCells in series: {!s}\nCells in parallel: {!s}\n'
      'Discharge rate: {!s}C\nCharge rate: {!s}C\nCell capacity {!s}Ah'.format(maxvolt, minvolt, series, parallel,
                                                                               crate_dischar, crate_char, capacity))


time.sleep(60.)

def log(timestamp, voltage, current, temperature=0.0, remark=''):
    with open('/home/pi/Silverwing/Delta/Battery_tests/Data/{!s}.log'.format(name), 'a') as d:
        d.write('t{!s} U{!s} I{!s} T{!s}, {!s}\n'.format(timestamp, voltage, current, temperature, remark))


def temp_read():
    with open('/home/pi/Silverwing/General/ambient.temp', 'r') as t:
        raw = t.read()
        try:
            t_f = float(raw.split(',')[0])
            value = float(raw.split(',')[1])
            t = time.time()
            if t - t_f > 10.:
                value = 'Outdated'
            t0 = time.time()
        except:
            value = 20
            # if time.time() - t0 > 10.:
            #     value = 'Outdated'

        return value


def charge():
    log(time.time(), 0., 0., temperature=-103., remark='Charging started: {}'.format(name))
    delta.set_voltage(delta.ask_voltage())
    t_current = crate_char * capacity * parallel
    t_voltage = maxvolt * series
    delta.set_voltage(t_voltage)
    delta.set_current(t_current)
    delta.set_state(1)
    t0 = time.time()

    try:
        while True:
            c_voltage = delta.ask_voltage()
            c_current = delta.ask_current()
            c_temp = temp_read()

            log(time.time(), c_voltage, c_current, c_temp)
            time.sleep(10.)
            if c_current < t_current/15. and time.time() - t0 > 22:
                print('Charging complete')
                break
            elif 0. > c_temp > 60.:
                print('Temperature threshold exceeded at {!s}'.format(c_temp))
                delta.set_state(0)
                time.sleep(60)
                delta.set_state(1)

    finally:
        delta.set_state(0)
        log(time.time(), 0., 0., temperature=-104., remark='Charging completed/interrupted: {}'.format(name))


def discharge(c_rate, duration=0, status='empty'):
    # Temperature timeout
    while temp_read() > target_temp:
        time.sleep(60.)

    Kp, Ki, Kd, c_current_error, c_temp, dt = 0.025/capacity, 0*5./capacity, 0.004/capacity, 0, 0., 0.1
    c_power_error = 0
    t_current = -c_rate * capacity * parallel
    t_power = t_current * series * 3.7

    if safe_operation:
        minv = minvolt
    else:
        minv = minvolt + t_current * R_sys

    print('Cutoff voltage: {!s}V'.format(minv))

    c_voltage = delta.ask_voltage()
    set_voltage = c_voltage
    delta.set_voltage(c_voltage)
    delta.set_state(1)
    if duration != 0:
        t_init = time.time()

    if c_voltage/series > minvolt:
        try:
            if status != 'next':
                log(time.time(), 0., 0., temperature=-101., remark='Discharging started: {}'.format(name))
            log(time.time(), c_voltage, 0, temperature=c_temp)
            while True:
                if duration != 0:
                    if time.time() - t_init > duration:
                        status = 'next'
                        break
                c_temp = temp_read()
                p_current_error = c_current_error
                c_current_error = t_current - delta.ask_current()
                dc_current_error = c_current_error - p_current_error

                p_power_error = c_power_error
                c_power_error = t_power - delta.ask_power()
                dc_power_error = c_power_error - p_power_error

                set_voltage = min(maxvolt * series, max(minv * series, set_voltage + (c_power_error * Kp / 3.7) +
                                                        (dc_power_error * Kd / 3.7) / dt))

                # set_voltage = min(maxvolt*series, max(minv * series, set_voltage + c_current_error * Kp +
                #                                       dc_current_error * Kd/dt))

                delta.set_voltage(set_voltage)

                c_voltage = delta.ask_voltage()
                c_current = delta.ask_current()
                log(time.time(), c_voltage, c_current, temperature=c_temp)
                print('\rVoltage: {!s}V, Current: {!s}A, Power: {!s}W, Temperature: {!s} C'.
                      format(c_voltage, c_current, c_voltage*c_current, c_temp), end='')

                time.sleep(dt)

                if abs((c_voltage/series - minv)) < 0.1 and c_current > t_current/2.:
                    print('Discharge completed')
                    status = 'discharged'
                    break

                if c_temp > max_cell_temp:
                    print('Temperature threshold exceeded at {!s}'.format(c_temp))
                    status = 'temp'
                    break

                else:
                    status = 'empty'
                    pass

        finally:
            if status != 'next':
                log(time.time(), 0., 0., temperature=-102., remark='Discharging completed/interrupted: {}'.format(name))
            delta.set_state(0)
            return status
    else:
        print('Voltage too low')
        return 'low voltage'


def cycle():
    status = 'empty'
    i = 1
    for c in crate_dischar:
        print('Discharge starts')
        status = discharge(c[0], duration=c[1], status=status)
        if i == len(crate_dischar):
            status = 'empty'
        if status != 'next':
            print('Charging starts in 1min')
            time.sleep(60)
            charge()
            time.sleep(10)
        i += 1

try:
    gp.output(pin, 1)
    charge()
    print('Sequence will start in 10s')
    time.sleep(10)
    cycle()

finally:
    delta.close_connection()
    gp.output(pin, 0)
    gp.cleanup()
    pat.terminate()
