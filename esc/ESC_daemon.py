import os
import pigpio
import time
import subprocess
import commands


# see if it is running already
status, process = commands.getstatusoutput('sudo pidof pigpiod')

if status:  #  it wasn't running, so start it
    print "pigpiod was not running"
    commands.getstatusoutput('sudo pigpiod')  # try to  start it
    time.sleep(1)
    # check it again
    status, process = commands.getstatusoutput('sudo pidof pigpiod')

if not status:  # if it was started successfully (or was already running)...
    pigpiod_process = process
    print "pigpiod is running, process ID is {} ".format(pigpiod_process)

    try:
        pi = pigpio.pi()  # local GPIO only
    except Exception, e:
        start_pigpiod_exception = str(e)
        print "problem instantiating pi: {}".format(start_pigpiod_exception)


# os.system("sudo pigpiod")  # Launching GPIO library
# time.sleep(2)

prpm = subprocess.Popen(['python', '/home/pi/Silverwing/esc/RPM_readout.py'])  # ESC daemon

channel0 = 19  # pin 35
channel1 = 18

pi = pigpio.pi()
pi.hardware_PWM(channel0, 30e3, 0)
pi.hardware_PWM(channel1, 30e3, 0)

minw, maxw = 1100., 1900.


def throttle(dc):
    pi.set_servo_pulsewidth(channel0, int((dc / 100.) * (maxw - minw) + minw))
    pi.set_servo_pulsewidth(channel1, int((dc / 100.) * (maxw - minw) + minw))


rpm_power, kp, t0, steps, value = 0, 0.003, time.time(), 10, 0


try:
    while True:
        p_value = value
        with open('/home/pi/Silverwing/esc/target.esc', 'r') as e:
            raw = e.read()
            try:
                mode = raw.split(',')[0]
                value = float(raw.split(',')[1])
                t0 = time.time()
            except IndexError:
                if time.time()-t0 > 3:
                    throttle(0)
                    break

        if mode == 'power':
            # for i in range(p_value, value + int((value-p_value)/steps), int((value-p_value)/steps)):
            throttle(value)
            time.sleep(0.1)

        elif mode == 'rpm':
            with open('/home/pi/Silverwing/esc/actual0.rpm', 'r') as d:
                try:
                    rpm = float(d.read())
                except ValueError:
                    rpm = 'Unknown'
            t_rpm = int(value)

            if t_rpm < 800:
                t_rpm = 0

            e = t_rpm-rpm
            if abs(e) < 40.:
                e = 0
            else:
                if rpm < 100 and t_rpm > 0:
                    rpm_power = 8
                else:
                    rpm_power += kp * e
                throttle(rpm_power)
            time.sleep(0.8)

        else:
            # print('error')
            time.sleep(0.5)

finally:
    throttle(0)
    pi.stop()
    prpm.terminate()
    os.system("sudo killall pigpiod")

    print '\nCleaned up'
