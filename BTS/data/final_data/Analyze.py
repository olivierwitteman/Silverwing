import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np

'''OCV'''

# nom_voltage = float(input('Nominal voltage of tested cell [V]: '))
mode = 0

R_battery = 0.013/4.
# R_battery = 0.0016

with open('./BT-B-1_1.log', 'r') as data:
    samples = data.readlines()

    Us, Is, ts, As, Tsp, Tsa, rmrk = [], [], [], [0.], [], [], []
    for i in range(len(samples)):
        try:
            Us.append(float(samples[i].split()[1][1:].strip()))
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip()))
            Tsp.append(float(samples[i].split()[3][1:-2].strip()))
            Tsa.append(float(samples[i].split()[3][1:-2].strip()))
            try:
                rmrk.append(str(samples[i].split()[6][:].strip()))
            except:
                pass

            if i > 0:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt/3600.))

        except:
            pass

As = [-x + max(As) for x in As]

fig, ax1 = plt.subplots()
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']

start, stop = ts.index(d_s_mark[0]) + 1, ts.index(d_e_mark[0]) - 1
av_current = abs(round(sum(Is[start:stop]) / (stop - start), 1))
av_voltage = round(sum(Us[start:stop]) / (stop - start), 1)
caps = []

R_sys = 0.008
R_total = R_sys + R_battery



ax2 = ax1.twinx()
ax2.grid()

endurance = round((ts[-1]-ts[0])/60., 1)
n = 25  # the larger n is, the smoother curve will be

av_voltage = np.average(Us)
av_current = -np.average(Is)

dOCV = np.array([R_total * -x for x in Is[start:stop]])
OCV = np.array(Us[start:stop]) + dOCV

# smooth_Us = lfilter([1.0 / n] * n, 1, Us[start:stop])
smooth_Us = lfilter([1.0 / n] * n, 1, OCV)
smooth_Is = -lfilter([1.0 / n] * n, 1, Is[start:stop])
smooth_Ts = lfilter([1.0 / n] * n, 1, Ts[start:stop])

A_zero = min(As[start:stop])
As_i = [x - A_zero for x in As[start:stop]]
capacity = max(As_i)
caps.append(capacity)
actual_energy = round(capacity*av_voltage, 1)
energy = round(capacity * sum(smooth_Us)/len(smooth_Us), 1)

if modes[mode] == 'reg':
    ax1.plot(As_i, smooth_Us, c=colors[j], ls='-', label='I_avg = {!s}A, E_extracted = {!s}Wh'.
             format(av_current, actual_energy))
elif modes[mode] == 'fp':
    ax1.plot(As_i, smooth_Us, c=colors[j], ls='-', label='I_avg = {!s}A, E_extracted = {!s}Wh, endurance = {!s}min'.
             format(av_current, actual_energy, endurance))

if modes[mode] == 'reg' or modes[mode] == 'fp':
    ax2.plot(As_i, smooth_Ts, c=colors[j], ls='-.', label='{!s}A [T]'.format(av_current))
    ax2.plot(As_i, smooth_Is, c=colors[j], ls=':', label='{!s}A [A]'.format(av_current), lw=2.)
    ax1.set_xlabel('Capacity [Ah]')
    ax1.set_ylabel('Open Circuit Voltage [V]')
    ax2.set_ylabel('Temperature [deg C], Current [A]')
    ax1.set_xlim(0, max(caps))
    ax1.set_ylim(2.0, 4.5)
    ax2.set_ylim(0, 80)
    if j == len(d_s_mark)-1:
        ax1.plot(np.nan, np.nan, ls=':', label='Current', c='k', lw=2.)
        ax1.plot(np.nan, np.nan, ls='-.', label='Temperature', c='k', lw=1.5)

else:
    if j == len(d_s_mark)-1:
        ax1.set_xlim(0, len(caps) * 1.1)
        ax1.plot(range(len(caps)), caps, label='Capacity loss over {!s} cycles of GoFly Silverwing flight '
                                               'profile'.format(len(caps)))
        ax1.set_ylim(0.9*caps[-1], 1.1*caps[0])

plt.title('Battery: {!s}, charged CC-CV at 1C with cutoff at 0.07C (1.5hrs)'.format(rmrk[0]))

ax1.legend(loc=0)

ax1.grid(True)
plt.show()



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

            if i > 0:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt/3600.))


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