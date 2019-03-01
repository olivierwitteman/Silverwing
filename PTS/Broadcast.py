#!/usr/bin python
__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"

import socket
import time
import smbus

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x28
DEVICE_REG_MODE1 = 0
DEVICE_REG_MODE2 = 1


def connect():
    ap = ('', 50002)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(ap)
    s.listen(1)
    return s.accept()


conn, addr = connect()

try:
    while True:
        a = bus.read_i2c_block_data(0x28, 0, 32)
        print a
        conn.sendall(a)
        time.sleep(0.1)

finally:
    conn.close()
