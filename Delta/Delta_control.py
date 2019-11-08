import time
# import delta_sm3300 as d
import Delta_comm as d

delta = d.DeltaComm()

# name = 'esc_left'


def clear_log(filename):
    with open('/home/pi/Silverwing/battery_tests/{!s}.log'.format(filename), 'w') as d:
        d.write('')


def log(filename, timestamp, voltage, current):
    with open('/home/pi/Silverwing/battery_tests/{!s}.log'.format(filename), 'a') as d:
        d.write('t{!s} U{!s} I{!s}\n'.format(timestamp, voltage, current))


dt = 0.01
vlst, ilst, tlst = [], [], []
delta.set_voltage(input('Voltage: '))
delta.set_current(input('Current: '))
delta.set_power(input('Power: '))
delta.set_state(1)

state = bool(input('Are you sure [1/0]? '))
if state:
    print('ok')
else:
    state = 0
    print('Aborted')
    raise KeyboardInterrupt

delta.set_state(state)

t0 = time.time()

try:
    print('Sampling at {!s}Hz'.format(1./dt))
    while True:
        vlst.append(delta.ask_voltage())
        ilst.append(delta.ask_current())
        tlst.append(time.time()-t0)
        time.sleep(dt)

finally:
    delta.set_state(0)
    # mst = min(len(vlst), len(ilst))
    # vlst = vlst[:mst]
    # ilst = ilst[:mst]
    # tlst = tlst[:mst]

    # print('Saving sample data')
    # clear_log(name)
    # for i in range(len(tlst)):
    #     log(name, tlst[i], vlst[i], ilst[i])

    delta.close_connection()
    print('Connection closed')



# delta.open_connection()


# delta.set_voltage(50.4)
# delta.set_current(4.125)
# delta.set_state(1)

# delta.set_voltage(25.1)
# delta.set_current(1.)
# delta.set_state(1)
# time.sleep(10)
# delta.set_state(0)

# print 'voltage: {!s}, actual current: {!s}, power: {!s}'\
#     .format(delta.ask_voltage(), delta.ask_current(), delta.ask_power())

