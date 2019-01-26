import time
import RPi.GPIO as gp
import delta_sm3300 as d
import subprocess
delta = d.DeltaComm()

pt = subprocess.Popen(['python3', '/home/pi/Silverwing/BTS/Pack_Temperature.py'])  # ESC daemon
pat = subprocess.Popen(['python', '/home/pi/Silverwing/General/Temp_sens.py'])  # ESC daemon

time.sleep(1)

path = '/'
filename = 'matrix.csv'

s1 = 5, 0, 'charging'
s2 = 6, 0, 'contactor'
s3 = 13, 3.34, 'R1'
s4 = 19, 1.7, 'R2'
s5 = 26, 0.622, 'R3'

ss = [s1, s2, s3, s4, s5]


crate_dischar = [(-1., 0)]
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
        gp.output(ss[i][0], 0)


def read_matrix():
    with open(str(path+filename), 'r') as m:
        lines = m.readlines()
    # TODO parse data
    data = [(0., 0.)]
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
                print value
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
    gp.output(s1[0], 1)
    gp.output(s2[0], 1)
    delta.set_state(1)

    t0 = time.time()

    try:
        while True:
            c_voltage = delta.ask_voltage()
            c_current = delta.ask_current()
            a_temp = temp_ambient()
            c_temp = temp_pack()

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
        gp.output(s2[0], 0)
        gp.output(s1[0], 0)
        log(name, time.time(), 0., 0., -104, temperature=-104., remark='Charging completed/interrupted: {}'.format(name))


def delta_discharge(name, minvolt, maxvolt, current, R, duration, status='empty'):
    delta.set_voltage(maxvolt)
    delta.set_current(-current)

    print(maxvolt, current)

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

        while dt < duration or duration == 0 and bat_voltage > minvolt:

            a_current = delta.ask_current()
            a_voltage = delta.ask_voltage()
            bat_voltage = a_current * R - a_voltage

            a_temp = temp_ambient()
            c_temp = temp_pack()

            log(name, time.time(), bat_voltage, a_current, a_temp, c_temp, a_temp)
            dt = time.time() - t0
            time.sleep(0.1)

            if bat_voltage < minvolt:
                print('Discharge completed')
                status = 'discharged'
                break

            elif -20. > c_temp > 60.:
                print('Temperature threshold exceeded at {!s}'.format(c_temp))
                status = 'temp'
                break

            else:
                status = 'empty'
                pass

    finally:
        if status != 'next':
            log(name, time.time(), 0., 0., a_temp, temperature=-102., remark='Discharging completed/interrupted: {}'.format(name))
        delta.set_state(0)
        return status


def discharge(c_rate, duration=0, status='empty', name='untitled'):
    pack_minvolt = series*minvolt
    pack_maxvolt = series*maxvolt
    current = c_rate*capacity*parallel

    if 0.67 <= c_rate < 1.3:
        config = [0, 1, 1, 0, 0]

    elif 1.3 <= c_rate < 1.95:
        config = [0, 1, 1, 0, 0]

    elif 1.95 <= c_rate < 3.54:
        config = [0, 1, 1, 0, 0]

    elif 3.54 <= c_rate < 4.2:
        config = [0, 1, 1, 0, 0]

    elif 4.2 <= c_rate < 4.84:
        config = [0, 1, 1, 0, 0]

    elif 4.84 <= c_rate < 5.5:
        config = [0, 1, 1, 0, 0]

    elif 5.5 <= c_rate < 9.15:
        config = [0, 1, 1, 0, 0]

    else:
        config = [0, 0, 0, 0, 0]

    R = R_sys
    for i in range(len(ss)):
        if i > 1:
            R += config[i]/ss[i][1]
        gp.output(ss[i][0], config[i])
    time.sleep(1)
    status = delta_discharge(name, pack_minvolt, pack_maxvolt, current, R, duration, status=status)
    return status


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
    initiate_relay_control()
    # matrix = read_matrix()

    # c_rate = matrix[1]
    # name = matrix[0]
    c_rate = crate_dischar[0][0]

    if c_rate > 0.:
        pass
        # charge(c_rate, name='untitled')
    elif c_rate < 0.:
        discharge(c_rate, duration=0, name='untitled')

    # print('Sequence will start in 10s')
    # time.sleep(10)
    # cycle()

finally:
    delta.set_state(0)
    gp.output(s2[0], 0)
    gp.cleanup()
    delta.close_connection()
    pt.terminate()
    pat.terminate()









