import pigpio
import time
import os
import sys


os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)
channel = 18  # pin 35

pi = pigpio.pi()
pi.hardware_PWM(channel, 50, 1500.)

minw, maxw = 553., 2500.


def set_angle(dc):
    pw = int((dc/180.)*(maxw-minw) + minw)
    pi.set_servo_pulsewidth(channel, pw)
    print pw


# dt = 0.004
# try:
#     while True:
#         for i in range(140):
#             time.sleep(dt)
#             set_angle(i)
#         for i in range(140):
#             time.sleep(dt)
#             set_angle(140-i)
#
# finally:
#     pi.stop()


# try:
#     while True:
#         set_angle(min(180., max(0., float(input('Angle (0 - 180 deg): ')))))
#
# finally:
#     pi.stop()


# if len(sys.argv) > 1:
#
# else:
#     try:
#         c.main()
#     finally:
#         c.cleanup()