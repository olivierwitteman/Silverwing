import smbus
import time
import math

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


DEVICE_ADDRESS = 0x28      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0
DEVICE_REG_MODE2 = 1


def cas(qc, p0):
    v = 0.51 * 661.4788 * math.sqrt(5.*((qc/p0 + 1.)**(2./7.) - 1.))
    return v


def u(q, temp, p):
    # rho = (p+1e-3)/(287.*temp)
    rho = 1.225
    print('rho: {!s}'.format(rho))
    airspeed = math.sqrt(2.*abs(q)/rho)
    return airspeed


def poll_q(delta=0.):
    p3s, p4s = [], []
    for i in range(16):
        block = bus.read_i2c_block_data(0x28, 0, 4)
        p3s.append(block[0])
        p4s.append(block[1])

    p4s.sort(), p3s.sort()

    # print min(lst), max(lst)
    p3 = p3s[int(len(p3s) / 2.)]
    p4 = p4s[int(len(p3s) / 2.)]

    p0 = p3s[int(len(p3s) / 2)] * 3386.389/1000.  # inch mercury
    q = abs(p3 - p4) - delta #* 6894.757/1000.
    # q = (abs(min(lst) - p0)) * 3386.389/1000. - delta

    return q, p0


try:
    dqs = []
    for _ in range(10):
        dqs.append(poll_q()[0])

    dq = sum(dqs)/len(dqs)

    print('dq: {!s}'.format(dq))

    while True:
        q = poll_q(delta=dq)
        print('p0: {!s}, q: {!s}'.format(q[1], q[0]))
        print('airspeed: {!s}\n\n'.format(u(q[0], temp=283., p=q[1])))
        # print(bus.read_word_data(DEVICE_ADDRESS, DEVICE_REG_MODE2))
        time.sleep(1)

finally:
    print('\nDone\n')