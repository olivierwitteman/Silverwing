import matplotlib.pyplot as plt
import numpy as np
import math
import struct

def u(q):
    # rho = (p+1e-3)/(287.*temp)
    rho = 1.225
    print('rho: {!s}'.format(rho))
    airspeed = np.sqrt(2.*abs(q)/rho)
    return airspeed


def pressure(dp_raw):
    diff_p_pa = -psi_to_pa * ((dp_raw - 0.1 * bits) * (p_max - p_min) / (0.8 * bits) + p_min)
    return diff_p_pa

def temperature(dt_raw):
    temp = ((200. * dt_raw) / 2047) - 50.
    return temp

filename = 'data1551287369.83'
with open('{!s}.dump'.format(filename), 'r') as d:
    data = d.read()[1:-2].split(',')
    data = [float(i) for i in data]


bits = 2**14
p_min = -1.
p_max = 1.
psi_to_pa = 6894.757

tlst = data[0*len(data)/5:len(data)/5]
i = 1
a0 = data[i*len(data)/5:(i+1)*len(data)/5]
i = 2
a1 = (np.array(data[i*len(data)/5:(i+1)*len(data)/5]) - 100)
a1 = pressure(a1)
# a1 = u(a1)

i = 3
a2 = np.array(data[i*len(data)/5:(i+1)*len(data)/5])

a2 = temperature(a2)

i = 4
a3 = np.array(data[i*len(data)/5:(i+1)*len(data)/5])

a3 = temperature(a3)


ax0 = plt.subplot(221)
ax0.plot(tlst, a0)

ax1 = plt.subplot(222)
ax1.plot(tlst, a1)

ax2 = plt.subplot(223)
ax2.plot(tlst, a2)

ax3 = plt.subplot(224)
ax3.plot(tlst, a3)


plt.show()
