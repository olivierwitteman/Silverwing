from __future__ import print_function
import time
import RPi.GPIO as gp
import delta_sm3300 as d
import sys
import subprocess
delta = d.DeltaComm()

pt = subprocess.Popen(['python3', '/home/pi/Silverwing/BTS/Pack_Temperature.py'])  # ESC daemon
pat = subprocess.Popen(['python', '/home/pi/Silverwing/General/Temp_sens.py'])  # ESC daemon

time.sleep(1)

path = ''
filename = 'BTS.csv'

s1 = 5, 0, 'charging'
s2 = 6, 0, 'contactor'
s3 = 19, 3.34, 'R1'
s4 = 13, 1.7, 'R2'
s5 = 26, 0.622, 'R3'

ss = [s1, s2, s3, s4, s5]


# crate_dischar = [(-6., 10), (-1, 10), (-3, 10)]
# crate_dischar = [(0.7, 10)]
maxvolt = 4.2
minvolt = 2.5
capacity = 3.
series = 6
parallel = 4
R_sys = 0.03


def initiate_relay_control():
    gp.setmode(gp.BCM)
    gp.setwarnings(False)
    for i in range(len(ss)):
        gp.setup(ss[i][0], gp.OUT)
        gp.output(ss[i][0], 1)


def read_matrix():
    with open(str(path+filename), 'r') as m:
        inputs = m.readlines()

        id, duration, c_rate, data = [], [], [], []
        for i in range(1, len(inputs)):
            try:
                id.append(str(inputs[i].replace(';', ',').split(',')[0][:]))
                duration.append(int(inputs[i].replace(';', ',').split(',')[1][:].strip()))
                c_rate.append(float(inputs[i].replace(';', ',').split(',')[2][:].strip()))
                data.append((c_rate[-1], duration[-1], id[-1]))
            except:
                id = id[:i-1]
                duration = duration[:i-1]
                c_rate = c_rate[:i-1]
    print('\n\nTest sequence: {!s}\n\n'.format(data))

    return data


def log(name, timestamp, voltage, current, amb_temp, temperature=0.0, remark=''):
    with open('/home/pi/Silverwing/BTS/data/{!s}.log'.format(name), 'a') as d:
        d.write('t{!s} U{!s} I{!s} T{!s} T_a{!s}, {!s}\n'.format(timestamp, voltage, current, amb_temp, temperature, remark))


def temp_ambient():
    with open('/home/pi/Silverwing/General/ambient.temp', 'r') as t:
        raw = t.read()
        try:
            t_f = float(raw.split(',')[0])
            value = float(raw.split(',')[1])
            t = time.time()
            if t - t_f > 10.:
                value = 'Outdated temperature measurement'
                print(value)
            t0 = time.time()
        except:
            value = 20
            # if time.time() - t0 > 10.:
            #     value = 'Outdated'

        return value


def temp_pack():
    with open('/home/pi/Silverwing/BTS/data/pack.temp', 'r') as t:
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


def charge(crate_char, name='untitled'):
    log(name, time.time(), 0., 0., -103, temperature=-103., remark='Charging started: {!s}'.format(name))
    delta.set_voltage(delta.ask_voltage())
    t_current = crate_char * capacity * parallel
    t_voltage = maxvolt * series
    delta.set_voltage(t_voltage)
    delta.set_current(t_current)
    print('\n\nCharging CC-CV with {!s}A at {!s}V\n\n'.format(round(t_current, 1), round(t_voltage, 1)))
    gp.output(s1[0], 0)
    delta.set_state(1)

    t0 = time.time()

    try:
        while True:
            c_voltage = delta.ask_voltage()
            c_current = delta.ask_current()
            a_temp = temp_ambient()
            c_temp = temp_pack()

            print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
                  .format(c_voltage, c_current, c_voltage * c_current), end="")

            log(name, time.time(), c_voltage, c_current, a_temp, c_temp, a_temp)
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
        gp.output(s1[0], 1)
        log(name, time.time(), 0., 0., -104, temperature=-104., remark='Charging completed/interrupted: {}'.format(name))


def delta_discharge(name, minvolt, maxvolt, current, R, duration, status='empty'):
    delta.set_voltage(maxvolt)
    delta.set_current(-current)

    t0, dt = time.time(), 0

    a_temp = temp_ambient()
    c_temp = temp_pack()

    try:
        if status != 'next':
            log(name, time.time(), 0., 0., a_temp, temperature=-101., remark='Discharging started: {}'.format(name))
        log(name, time.time(), 0., 0., a_temp, temperature=-101., remark='Discharging started: {}'.format(name))

        delta.set_state(1)
        time.sleep(10)

        a_current = delta.ask_current()
        a_voltage = delta.ask_voltage()
        bat_voltage = a_current * R - a_voltage

        while True:
            print('\rVoltage: {!s}, actual current: {!s}, power: {!s}' \
                  .format(a_voltage, a_current, a_voltage*a_current), end="")
            if bat_voltage < minvolt:
                print('Discharge completed')
                status = 'discharged'
                break

            if duration != 0:
                if dt > duration:
                    status = 'next'
                    break

            elif -20. > c_temp > 60.:
                print('Temperature threshold exceeded at {!s}'.format(c_temp))
                status = 'temp'
                break

            else:
                status = 'empty'
                pass

            a_current = delta.ask_current()
            a_voltage = delta.ask_voltage()
            bat_voltage = a_current * R - a_voltage

            a_temp = temp_ambient()
            c_temp = temp_pack()

            log(name, time.time(), bat_voltage, -a_current, a_temp, c_temp)
            dt = time.time() - t0
            time.sleep(0.1)

    finally:
        if status != 'next':
            log(name, time.time(), 0., 0., a_temp, temperature=-102., remark='Discharging completed/interrupted: {}'
                                                                             ''.format(name))
        delta.set_state(0)
        return status


def discharge(c_rate, duration=0, status='empty', name='untitled'):
    pack_minvolt = series*minvolt
    pack_maxvolt = series*maxvolt
    current = c_rate*capacity*parallel

    if 0.67 <= -c_rate < 1.3:
        config = [0, 1, 1, 0, 0]

    elif 1.3 <= -c_rate < 1.95:
        config = [0, 1, 0, 1, 0]

    elif 1.95 <= -c_rate < 3.54:
        config = [0, 1, 1, 1, 0]

    elif 3.54 <= -c_rate < 4.2:
        config = [0, 1, 0, 0, 1]

    elif 4.2 <= -c_rate < 4.84:
        config = [0, 1, 1, 0, 1]

    elif 4.84 <= -c_rate < 5.5:
        config = [0, 1, 0, 1, 1]

    elif 5.5 <= -c_rate < 9.15:
        config = [0, 1, 1, 1, 1]

    else:
        config = [0, 0, 0, 0, 0]

    R_inv = 0.
    for i in range(len(ss)):
        if i > 1:
            R_inv += config[i]/ss[i][1]
        gp.output(ss[i][0], abs(config[i]-1))
    R = 1/R_inv + R_sys

    time.sleep(1)
    status = delta_discharge(name, pack_minvolt, pack_maxvolt, current, R, duration, status=status)

    for i in range(len(ss)):
        gp.output(ss[i][0], 1)
    time.sleep(0.1)
    return status


def cycle():
    status = 'empty'
    i = 1
    for c in crate_dischar:
        print(c)
        try:
            oldname = newname
        except NameError:
            oldname = c[2]
        newname = c[2]
        print('Discharge starts')
        if c[0] > 0.:
            print('Charging initiated')
            charge(c[0], name=c[2])

        elif c[0] < 0.:
            print('Discharging initiated/continued')
            status = discharge(c[0], duration=c[1], status=status, name=c[2])
        else:
            print('Error at c-rating in input file')

        if oldname != newname:
            status = 'empty'

        if status != 'next':
            print('Charging starts in 1min')
            time.sleep(60)
            charge(0.7, c[2])
            time.sleep(10)
        i += 1


try:
    initiate_relay_control()
    crate_dischar = read_matrix()
    charge(0.7, name=crate_dischar[0][2])
    cycle()


except:
    print(sys.exc_info())

finally:
    delta.set_state(0)
    gp.output(s2[0], 0)
    gp.cleanup()
    delta.close_connection()
    pt.terminate()
    pat.terminate()









