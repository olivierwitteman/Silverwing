import matplotlib.pyplot as plt
import numpy as np

path = './'
# path = '/Users/olivierwitteman/Downloads/'
name = 'esc_right'

with open('{!s}{!s}.log'.format(path, name), 'r') as data:
    samples = data.readlines()

    Us, Is, ts, = [], [], []
    for i in range(len(samples)):
        try:
            Us.append(float(samples[i].split()[1][1:].strip()))
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip()))
        except:
            pass


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax2.grid()

ax1.plot(ts, Us, label='Voltage', color='b')
ax2.plot(ts, Is, label='Current', color='r')

ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Voltage [V]')
ax2.set_ylabel('Current [A]')
plt.title(name)
ax1.set_xlim(0, 10)
ax2.set_xlim(0, 10)

ax1.set_ylim(0, 25)
ax2.set_ylim(0, 1.5)

ax1.grid(True)
plt.show()
