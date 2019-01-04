import os
import time
import subprocess
from Delta_comm import DeltaComm
import pigpio

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)

path = '/home/pi/Silverwing/cfts'

pd = subprocess.Popen(['python', '/home/pi/Silverwing/esc/ESC_daemon.py'])

delta = DeltaComm()

channel = 18  # pin 35

pi = pigpio.pi()
pi.hardware_PWM(channel, 50, 1500.)

minw, maxw = 553., 2500.


def set_angle(dc):
    flap = [0, 5, 10, 15, 20, 25, 30]
    ser = [102, 91, 79, 67, 51, 38, 18]
    angle = ser[flap.index(int(dc))]
    pw = int((angle/180.)*(maxw-minw) + minw)
    pi.set_servo_pulsewidth(channel, pw)


def set_power(dc):
    with open('/home/pi/Silverwing/esc/target.esc', 'w') as d:
        d.write('power,{!s}'.format(int(dc)))


def log(n, t_id, timestamp, a_rpm, a_power, s_deflection):
    with open('./cfts.log', 'a') as l:
        l.writelines('{!s},{!s},{!s},{!s},{!s},{!s}\n'.format(n, t_id, timestamp, a_rpm, a_power, s_deflection))


try:
    voltage, current = 25.2, 75.
    delta.set_voltage(voltage)
    print 'Voltage set to {!s}'.format(delta.ask_voltage())
    delta.set_current(current)
    delta.set_state(1)
    with open(path + '/Sheet1-Table_1.csv', 'r') as d:
        inputs = d.readlines()

        linenumber, id, r_pwr, deflection = [], [], [], []
        for i in range(1, len(inputs)):
            try:
                linenumber.append(int(inputs[i].split(',')[0][:]))
                id.append(str(inputs[i].split(',')[1][:].strip()))
                r_pwr.append(int(inputs[i].split(',')[2][:].strip()))
                deflection.append(float(inputs[i].split(',')[3][:].strip()))
            except:
                linenumber = linenumber[:i-1]
                id = id[:i-1]
                r_pwr = r_pwr[:i-1]
                deflection = deflection[:i-1]
                break

    line = 0
    while True:
        try:
            line = int(input('Line number (1 to {!s}): '.format(linenumber[-1]))) - 1
        except SyntaxError:
            line += 1

        print linenumber[line], id[line], r_pwr[line], deflection[line]
        set_power(r_pwr[line])
        set_angle(deflection[line])

        actual_rpm = 'Unknown'
        print 'RPM: {!s}'.format(actual_rpm)
        time.sleep(1)
        print delta.ask_power()

        log(linenumber[line], id[line], time.time(), actual_rpm, delta.ask_power(), deflection[line])

finally:
    set_power(0)
    delta.set_state(0)
    pd.terminate()

    delta.close_connection()
