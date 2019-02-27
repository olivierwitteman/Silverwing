__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"


import socket, time
import matplotlib.pyplot as plt


while True:
    tlst, alst, blst, clst, dlst = [], [], [], [], []
    ap = ('olipi.local', 50002)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(ap)
    while True:
        time.sleep(0.2)
        data = s.recv(8)
        print data
        if not data:
            print 'Data format error'
            break
        else:
            try:
                tlst.append(time.time())
                alst.append(data[0][1:])
                blst.append(data[1][1:])
                clst.append(data[2][1:])
                dlst.append(data[3][1:])

                plt.plot(tlst, alst)
                plt.plot(tlst, blst)
                plt.plot(tlst, clst)
                plt.plot(tlst, dlst)

                plt.pause(0.01)
            except KeyboardInterrupt:
                break
                print 'Ctr+c again to kill'
                time.sleep(1)
            except:
                print 'Error writing data to file'


