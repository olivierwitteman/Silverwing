import matplotlib.pyplot as plt
import numpy as np
import sys

path = './'
# path = '/Users/olivierwitteman/Downloads/'
name = 'BTS_1'

with open('{!s}{!s}.log'.format(path, name), 'r') as data:
    samples = data.readlines()
    Us, Is, ts, tsa, tsp = [], [], [], [], []
    for i in range(len(samples)):
        try:
            Us.append(float(samples[i].split()[1][1:].strip()))
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip()))
            tsa.append(float(samples[i].split()[4][3:-2].strip()))
            tsp.append(float(samples[i].split()[3][1:].strip()))
            if tsa[-1] < -99.:
                raise ValueError
        except:
            Us = Us[:-2]
            ts = ts[:-2]
            Is = Is[:-2]
            tsa = tsa[:-2]
            tsp = tsp[:-2]
            pass

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.grid()
s = 0.5

ax1.scatter(ts, Us, label='Voltage', color='b', s=s)
ax2.scatter(ts[0], 0, label='Voltage', color='b', s=s)
ax2.scatter(ts, Is, label='Current', color='r', s=s)
ax2.scatter(ts, tsa, label='Water temperature', s=s)
ax2.scatter(ts, tsp, label='Thermistor temperature', s=s)

ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax2.set_ylabel('Current [A] / Temperature [C]')

plt.title(name)
# ax1.set_xlim(0, 10)
# ax2.set_xlim(0, 10)

# ax1.set_ylim(0, 25)
# ax2.set_ylim(0, 1.5)
ax2.legend()
ax1.grid(True)
plt.show()
