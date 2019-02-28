import matplotlib.pyplot as plt
import numpy as np
import math


def u(q):
    # rho = (p+1e-3)/(287.*temp)
    rho = 1.225
    print('rho: {!s}'.format(rho))
    airspeed = np.sqrt(2.*abs(q)/rho)
    return airspeed


filename = 'data1551287369.83'
with open('{!s}.dump'.format(filename), 'r') as d:
    data = d.read()[1:-2].split(',')
    data = [float(i) for i in data]

p_range = 103420.

tp = 'B'
if tp == 'A':
    rel_range = 90.
else:
    rel_range = 80.
marg = (100. - rel_range)/2.
p_min = -p_range
p_max = p_range
p0 = p_min - (p_max - p_min)*5./90.
p100 = p_max + (p_max - p_min)*5./90.

fac = 1.

tlst = data[0*len(data)/5:len(data)/5]
i = 1
a0 = data[i*len(data)/5:(i+1)*len(data)/5]
i = 2
a1 = (np.array(data[i*len(data)/5:(i+1)*len(data)/5]) - 100) * fac
a1 = u(a1)

i = 3
a2 = data[i*len(data)/5:(i+1)*len(data)/5]
i = 4
a3 = data[i*len(data)/5:(i+1)*len(data)/5]


ax0 = plt.subplot(221)
ax0.plot(tlst, a0)

ax1 = plt.subplot(222)
ax1.plot(tlst, a1)

ax2 = plt.subplot(223)
ax2.plot(tlst, a2)

ax3 = plt.subplot(224)
ax3.plot(tlst, a3)


plt.show()
