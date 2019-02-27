import smbus
import time

bus = smbus.SMBus(1)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


DEVICE_ADDRESS = 0x28      #7 bit address (will be left shifted to add the read write bit)
DEVICE_REG_MODE1 = 0
DEVICE_REG_MODE2 = 1

try:
    while True:
        for i in range(16):
            print(bus.read_word_data(DEVICE_ADDRESS, i))
        # print(bus.read_word_data(DEVICE_ADDRESS, DEVICE_REG_MODE2))
        print('\n\n')
        time.sleep(1)

finally:
    print('\nDone\n')