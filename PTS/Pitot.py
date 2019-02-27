import smbus
import time
import math

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


DEVICE_ADDRESS = 0x28      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0
DEVICE_REG_MODE2 = 1


def cas(qc, p0):
    v = 0.51 * 661.4788 * math.sqrt(5.*((qc/p0 + 1.)**(2./7.) - 1))
    return v


def u(q, rho):
    airspeed = math.sqrt(2. * q/rho)
    return airspeed


def q(dq=0):
    lst = []
    for i in range(64):
        lst.append(bus.read_word_data(DEVICE_ADDRESS, i))

    lst.sort()
    print min(lst), max(lst)
    print sum(lst) / len(lst), lst[int(len(lst) / 2)]

    q = abs(max(lst) - lst[int(len(lst) / 2)]) - dq
    return q


try:
    dq = q()
    while True:
        q = q()
        print(u(q, 1.225))
        # print(bus.read_word_data(DEVICE_ADDRESS, DEVICE_REG_MODE2))
        print('\n\n')
        time.sleep(1)

finally:
    print('\nDone\n')