#!/usr/bin python
__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"

import socket
import time

path = './'
filename = 'tempdata'


def connect():
    ap = ('', 50002)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(ap)
    s.listen(1)
    return s.accept()


def read_data():
    with open('{!s}{!s}.csv'.format(path, filename)) as d:
        lastline = d.readlines()[-1]

    return lastline


conn, addr = connect()
print('connect_check')

try:
    while True:
        a = read_data()
        print(a)
        conn.sendall(bytes(a))
        print('check')
        time.sleep(0.1)

finally:
    conn.close()
