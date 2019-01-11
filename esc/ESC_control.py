import os
import time
import subprocess
import delta_sm3300 as d

delta = d.DeltaComm()

# os.system("sudo pigpiod")  # Launching GPIO library
# time.sleep(1)

pd = subprocess.Popen(['python', '/home/pi/Silverwing/esc/ESC_daemon.py'])
pr = subprocess.Popen(['python', '/home/pi/Silverwing/esc/RPM_readout.py'])

time.sleep(1.)


def set_rpm(rpm):
    with open('/home/pi/Silverwing/esc/target.esc', 'w') as d:
        d.write('rpm,{!s}'.format(int(rpm)))


def set_power(dc):
    with open('/home/pi/Silverwing/esc/target.esc', 'w') as d:
        d.write('power,{!s}'.format(int(dc)))


set_power(0)

try:
    voltage, current = 25.2, 75.
    delta.set_voltage(voltage)
    print 'Voltage set to {!s}'.format(delta.last_voltage())
    delta.set_current(current)
    delta.set_state(1)

    mode = str(raw_input('power or rpm?: '))
    while True:
        if mode == 'power':
            set_power(float(input('Power (0-100): ')))

        elif mode == 'rpm':
            set_rpm(int(input('rpm: ')))

        else:
            print('Select a valid mode')

finally:
    set_power(0)
    delta.set_state(0)
    pd.terminate()
    pr.terminate()
    delta.close_connection()
