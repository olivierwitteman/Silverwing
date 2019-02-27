__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"


import socket, time
import matplotlib.pyplot as plt


while True:
    tlst, dlst = [], []
    ap = ('olipi.local', 50002)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(ap)
    while True:
        time.sleep(0.2)
        data = s.recv(1024)
        if not data or data.split(',')[0][0] is not 'd':
            print 'Data format error'
            break
        else:
            try:
                print data
                tlst.append(data[0])
                dlst.append(data[1:])
                plt.plot(tlst, dlst)
                plt.draw()
            except KeyboardInterrupt:
                break
                print 'Ctr+c again to kill'
                time.sleep(1)
            except:
                print 'Error writing data to file'


