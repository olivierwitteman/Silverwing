import time
import RPi.GPIO as gp
import delta_sm3300 as d

delta = d.DeltaComm()

safe_operation = False
capacity = 3.0
crate_dischar = [(8.37, 10), (8.37, 20), (9.44, 15), (4.74, 15), (1.71, 1100), (1.42, 15), (9.44, 15), (7.35, 10), (0., 60), (1.71, 0)]
# crate_dischar = [(6., 0), (5., 0), (4., 0), (3., 0), (2., 0), (1., 0)]
# (C, duration [s]) duration=0 for full discharge
name = 'US18650_VTC6_fp_dec'
minvolt = 2.8  # OCV
R_sys = 0.03

pin = 4
gp.setmode(gp.BCM)
gp.setwarnings(False)
gp.setup(pin, gp.OUT)

if not safe_operation:
    print '\n\nWARNING, lowered cutoff voltage to allow for higher discharge rate. Do not leave this process ' \
          'unattended.\n\nBattery degradation will be accelerated in this mode.'
maxvolt, series, parallel, crate_char = 4.2, 1, 1, 1.
print 'Maximum cell voltage: {!s}V\nMinimum cell voltage: {!s}V\nCells in series: {!s}\nCells in parallel: {!s}\n' \
      'Discharge rate: {!s}C\nCharge rate: {!s}C'.format(maxvolt, minvolt, series, parallel, crate_dischar, crate_char)


def log(timestamp, voltage, current, temperature=0.0, remark=''):
    with open('/home/pi/Silverwing/battery_tests/data/{!s}.log'.format(name), 'a') as d:
        d.write('t{!s} U{!s} I{!s} T{!s}, {!s}\n'.format(timestamp, voltage, current, temperature, remark))


def temp_read():
    with open('/home/pi/Silverwing/battery_tests/data/current.temp', 'r') as t:
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
    Kp, Ki, Kd, c_current_error, c_temp, dt = 0.025/capacity, 0*5/capacity, 0.004/capacity, 0, 0., 0.1
    t_current = -c_rate * capacity * parallel

    if safe_operation:
        minv = minvolt
    else:
        minv = minvolt + t_current * R_sys

    print 'Cutoff voltage: {!s}V'.format(minv)

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

                set_voltage = min(maxvolt*series, max(minv * series, set_voltage + c_current_error * Kp +
                                                      dc_current_error * Kd/dt))
                delta.set_voltage(set_voltage)

                c_voltage = delta.ask_voltage()
                c_current = delta.ask_current()
                log(time.time(), c_voltage, c_current, temperature=c_temp)

                time.sleep(dt)

                if abs((c_voltage/series - minv)) < 0.1 and c_current > t_current/3.:
                    print('Discharge completed')
                    status = 'discharged'
                    break

                elif c_temp > 60.:
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
        print 'Voltage too low'
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
