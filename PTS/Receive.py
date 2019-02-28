__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"


import socket, time
import matplotlib.pyplot as plt

try:
    while True:
        tlst, alst, blst, clst, dlst = [], [], [], [], []
        ap = ('olipi.local', 50002)

        ax0 = plt.subplot(221)
        ax0.set_ylabel('Parameter a')
        ax1 = plt.subplot(222)
        ax1.set_ylabel('Parameter b')
        ax2 = plt.subplot(223)
        ax2.set_ylabel('Parameter c')
        ax3 = plt.subplot(224)
        ax3.set_ylabel('Parameter d')

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(ap)
        t0 = time.time()
        tplot = time.time()
        while True:
            time.sleep(0.03)
            data = s.recv(1024).split(',')
            print data[0][1:]
            if not data:
                print 'Data format error'
                break
            else:
                try:
                    tlst.append(time.time()-t0)
                    alst.append(float(data[0][1:]))
                    blst.append(float(data[1][1:]))
                    clst.append(float(data[2][1:]))
                    dlst.append(float(data[3][1:]))

                    ax0.plot(tlst, alst)
                    ax1.plot(tlst, blst)
                    ax2.plot(tlst, clst)
                    ax3.plot(tlst, dlst)

                    if time.time() - tplot > 2:
                        plt.pause(0.01)
                        tplot = time.time()
                except KeyboardInterrupt:
                    print 'Ctr+c again to kill'
                    break
                    time.sleep(1)
                except:
                    trim = min(len(tlst), len(alst), len(blst), len(clst), len(dlst))
                    tlst = tlst[:trim]
                    alst = alst[:trim]
                    blst = blst[:trim]
                    clst = clst[:trim]
                    dlst = dlst[:trim]
finally:
    with open('./data{!s}.dump'.format(time.time()), 'w') as d:
        d.write(str(tlst+alst+blst+clst+dlst))
    plt.show()




