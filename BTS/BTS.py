import time
import RPi.GPIO as gp
import delta_sm3300 as d
delta = d.DeltaComm()

path = '/'
filename = 'matrix.csv'

s1 = 5, 0, 'charging'
s2 = 6, 0, 'contactor'
s3 = 13, 3.34, 'R1'
s4 = 19, 1.7, 'R2'
s5 = 26, 0.622, 'R3'

ss = [s1, s2, s3, s4, s5]


maxvolt = 4.2
minvolt = 2.5
capacity = 3.
series = 6
parallel = 4


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


def read_temperature():
    return 0


def log(name, timestamp, voltage, current, amb_temp, temperature=0.0, remark=''):
    with open('/home/pi/Silverwing/battery_tests/data/{!s}.log'.format(name), 'a') as d:
        d.write('t{!s} U{!s} I{!s} T{!s} T_a{!s}, {!s}\n'.format(timestamp, voltage, current, amb_temp, temperature, remark))


def temp_ambient():
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


def temp_pack():
    return 0


def charge(crate_char, name):
    log(name, time.time(), 0., 0., -103, temperature=-103., remark='Charging started: {!s}'.format(name))
    delta.set_voltage(delta.ask_voltage())
    t_current = crate_char * capacity * parallel
    t_voltage = maxvolt * series
    delta.set_voltage(t_voltage)
    delta.set_current(t_current)
    delta.set_state(1)

    gp.output(s1[0], 1)
    gp.output(s2[0], 1)

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


def delta_discharge(name, minvolt, maxvolt, current, R, duration):
    delta.set_voltage(maxvolt)
    delta.set_current(current)
    t0, dt = time.time(), 0


    while dt < duration or duration == 0:

        c_voltage = delta.ask_voltage()
        c_current = delta.ask_current()
        a_temp = temp_ambient()
        c_temp = temp_pack()

        log(name, time.time(), c_voltage, c_current, a_temp, c_temp, a_temp)
        dt = time.time() - t0


def discharge(name, c_rate, duration=0):
    pack_minvolt = series*minvolt
    pack_maxvolt = series*maxvolt
    current = c_rate*capacity*parallel

    if 0.67 <= c_rate < 1.3:
        R = 3.34
        config = [0, 1, 1, 0, 0]

    elif 1.3 <= c_rate < 1.95:
        R = s2[1]
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

    R = 0
    for i in range(len(ss)):
        if i > 1:
            R += config[i]/ss[i][1]
        gp.output(ss[i][0], config[i])

    delta_discharge(name, pack_minvolt, pack_maxvolt, current, R, duration)


try:
    initiate_relay_control()
    matrix = read_matrix()

    c_rate = matrix[1]
    name = matrix[0]
    if c_rate > 0.:
        charge(c_rate, name)
    elif c_rate < 0.:
        discharge(c_rate, name)



finally:
    delta.set_state(0)
    gp.output(s2[0], 0)
    gp.cleanup()


