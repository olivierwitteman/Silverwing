import os
import time
import subprocess
import delta_sm3300 as d
import pigpio

path = '/home/pi/Silverwing/WaTT'
# path = '.'

pd = subprocess.Popen(['python', '/home/pi/Silverwing/esc/ESC_daemon.py'])  # ESC daemon
time.sleep(2)
delta = d.DeltaComm()  # Delta communication


def read_rpm():
    with open('/home/pi/Silverwing/esc/actual0.rpm', 'r') as rpm0file:
        try:
            rpm0 = float(rpm0file.read())
        except ValueError:
            rpm0 = 'Unknown'
    with open('/home/pi/Silverwing/esc/actual1.rpm', 'r') as rpm1file:
        try:
            rpm1 = float(rpm1file.read())
        except ValueError:
            rpm1 = 'Unknown'
    return rpm0, rpm1


def set_power(dc):
    with open('/home/pi/Silverwing/esc/target.esc', 'w') as d:
        d.write('power,{!s}'.format(int(dc)))


def set_rpm(rpm):
    with open('/home/pi/esc/target.esc', 'w') as e:
        e.write('rpm,{!s}'.format(int(rpm)))


def log(day, n, t_id, timestamp, a_rpm0, a_rpm1, a_power, a_voltage, a_current, f0, f1, a0, b0, a1, b1, df0, df1):
    with open('{!s}/Data/WaTT_{!s}jan.log'.format(path, day), 'a') as logfile:
        logfile.writelines('{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s}\n'.
                           format(n, t_id, timestamp, a_rpm0, a_rpm1, a_power, a_voltage, a_current,
                                  f0, f1, a0, b0, a1, b1, df0, df1))


def readdf(path, day):
    cal_lines = []
    with open('{!s}/Data/WaTT_{!s}jan.log'.format(path, day), 'r') as logfile:
        dfs = logfile.readlines()
    for i in range(len(dfs)):
        if int(dfs[i].replace(';', ',').split(',')[0]) == 0:
            cal_lines.append(i)
    lastcal = max(cal_lines)

    return float(dfs[lastcal].replace(';', ',').split(',')[14]), float(dfs[lastcal].replace(';', ',').split(',')[15])


def get_prefix():
    pr = time.strftime("%Y_%m_%d")
    return pr


def get_forces():
    with open('/home/pi/Silverwing/WaTT/for.ces', 'r') as ffile:
        try:
            fs = ffile.readline().replace(';', ',').split(',')
            f0 = float(fs[1])
            f1 = float(fs[2])
            a0 = float(fs[3])
            b0 = float(fs[4])
            a1 = float(fs[5])
            b1 = float(fs[6])
        except ValueError:
            f0 = 'Unknown'
            f1 = 'Unknown'
            a0 = 'Unknown'
            b0 = 'Unknown'
            a1 = 'Unknown'
            b1 = 'Unknown'
    return f0, f1, a0, b0, a1, b1


try:
    ymd = get_prefix()
    voltage, current = 25.2, 75.
    delta.set_voltage(voltage)
    print('Voltage set to {!s}\n'.format(delta.last_voltage()))
    delta.set_current(current)
    delta.set_state(1)
    day = int(input('Day (8-11): '))
    with open(path + '/WaTT test matrix/{!s}jan-Table 1.csv'.format(day), 'r') as d:
        inputs = d.readlines()

        linenumber, id, r_pwr, deflection = [], [], [], []
        for i in range(2, len(inputs)):
            try:
                linenumber.append(int(inputs[i].replace(';', ',').split(',')[0][:]))
                id.append(str(inputs[i].replace(';', ',').split(',')[1][:].strip()))
                r_pwr.append(int(inputs[i].replace(';', ',').split(',')[4][:].strip()))
            except:
                pass
                linenumber = linenumber[:i-1]
                id = id[:i-1]
                r_pwr = r_pwr[:i-1]

    line = -1
    print('\nTo (re)calibrate load cells go to line {!s} of the test matrix at any time\n------------------------------'
          '-----------------------------\n'.format(linenumber[0]))
    while True:
        try:
            line = int(input('Line number ({!s} to {!s}) / leave empty for next line: '.format(linenumber[0],
                                                                                               linenumber[-1])))
        except SyntaxError:
            line += 1

        except IndexError:
            print('\nEnd of test matrix reached\nCongrats on making it through!\n')
            break

        if line == 0:
            print('\nCalibrating load cells, please do not touch anything and make sure V_inf = 0.')
            time.sleep(1)
            force_offset = get_forces()
            df0, df1 = force_offset[0], force_offset[1]
            print('Force offset at dF0: {!s}N, dF1: {!s}N\n\n'.format(round(df0, 1), round(df1, 1)))
        else:
            df0, df1 = readdf(path, day)

        print('LineNumber: {!s}, ID: {!s}, Power: {!s}%\n'.format(linenumber[line], id[line], r_pwr[line]))
        set_power(r_pwr[line])
        time.sleep(3)

        a_rpm0, a_rpm1 = read_rpm()
        print('W0: {!s} rpm, W1: {!s} rpm, P: {!s} W'.format(a_rpm0, a_rpm1, round(delta.ask_power(), 1)))
        f0, f1, a0, b0, a1, b1 = get_forces()
        f0 -= df0
        f1 -= df1
        print('F0: {!s} N,   F1: {!s} N\n\n-------------------------------'
              '----------------------------'.format(round(f0, 1), round(f1, 1)))
        # f0, f1 = 0, 0
        log(day, linenumber[line], id[line], time.time(), a_rpm0, a_rpm1, delta.ask_power(), delta.ask_voltage(),
            delta.ask_current(), f0, f1, a0, b0, a1, b1, df0, df1)

finally:
    set_power(0)
    delta.set_state(0)
    pd.terminate()
    delta.close_connection()
    print('\nPower switched off successfully ')
