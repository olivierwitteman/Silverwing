import os
import time
import subprocess
from Delta_comm import DeltaComm
import pigpio

os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)

path = '/home/pi/cfts'

pd = subprocess.Popen(['python', '/home/pi/motor_control/ESC_daemon.py'])

delta = DeltaComm()
delta.open_connection()

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
    with open('/home/pi/motor_control/target.esc', 'w') as d:
        d.write('power,{!s}'.format(int(dc)))


def log(n, t_id, timestamp, a_rpm, a_power, s_deflection):
    with open('./cfts.log', 'a') as l:
        l.writelines('{!s},{!s},{!s},{!s},{!s},{!s}\n'.format(n, t_id, timestamp, a_rpm, a_power, s_deflection))


def delta_power():
    n, p = 10, 0
    for _ in range(n):
        p += delta.ask_power()/n
        time.sleep(0.01)
    return p


voltage, current = 16, 50.

try:
    delta.set_voltage(voltage)
    print 'Voltage set to {!s}'.format(delta.ask_voltage)
    delta.set_current(current)
    set_power(100)
    time.sleep(2.)
    delta.set_state(1)
    time.sleep(2.)
    set_power(0)
    time.sleep(3.)


    while True:
        req_power = float(input('Power (0-100): '))

        set_power(req_power)

        time.sleep(2)
        print 'Power: {!s}\nCurrent: {!s}\n'.format(delta_power(), delta.ask_current())

finally:
    set_power(0)
    delta.set_state(0)