import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np

'''OCV'''

# nom_voltage = float(input('Nominal voltage of tested cell [V]: '))
mode = 0

# R_battery = 0.0
R_battery = 6.*0.0128/4.

path = './'
# path = '/Users/olivierwitteman/Downloads/'
# name = 'BT-B-1_1'
name = 'BT-E-1800_1200-80_40-6'


def remove_last(Us, ts, Is, Tsp, Tsa, As):

    Us = Us[:-2]
    ts = ts[:-2]
    Is = Is[:-2]
    Tsp = Tsp[:-2]
    Tsa = Tsa[:-2]
    As = As[:-2]

    # new_array = []
    # print array
    #
    # for j in range(len(array)):
    #     new_array.append([array[j][:-2]])
    #
    # print new_array
    # return new_array

    return Us, ts, Is, Tsp, Tsa, As


with open('{!s}{!s}.log'.format(path, name), 'r') as data:
    samples = data.readlines()
    Us, Is, ts, As, Tsp, Tsa, rmrk = [], [], [], [0.], [], [], []

for i in np.arange(0, len(samples), 10):
    try:
        Us.append(float(samples[i].split()[1][1:].strip()))
        ts.append(float(samples[i].split()[0][1:].strip()))
        Is.append(float(samples[i].split()[2][1:].strip()))
        # print(float(samples[i].split()[3][3:-2].strip()))
        Tsa.append(float(samples[i].split()[3][3:].strip()))
        # print(float(samples[i].split()[4][3:-2].strip()))
        Tsp.append(float(samples[i].split()[4][3:].strip()))

        if i > 1:
            dt = ts[-1] - ts[-2]
            As.append(float(As[-1] + Is[-1] * dt / 3600.))

        if Is[-1] > 0 or Tsp[-1] < -100. or Tsa[-1] < -100.:
            # print(len(Us))
            raise KeyboardInterrupt

    except:
        # print('ass\n\n\n')
        # print('Us: ', len(Us))
        Us, ts, Is, Tsp, Tsa, As = remove_last(Us, ts, Is, Tsp, Tsa, As)
        # print('Us: ', len(Us))
        pass


maxlength = min(len(Us), len(ts), len(Is), len(Tsp), len(Tsa), len(As))
Us = Us[:maxlength]
ts = ts[:maxlength]
Is = Is[:maxlength]
Tsp = Tsp[:maxlength]
Tsa = Tsa[:maxlength]
As = As[:maxlength]

As = [-x + max(As) for x in As]

fig, ax1 = plt.subplots(figsize=(10, 6.25))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']

# start, stop = ts.index(d_s_mark[0]) + 1, ts.index(d_e_mark[0]) - 1

caps = []

R_sys = 0.0
R_total = R_sys + R_battery

ax2 = ax1.twinx()
ax2.grid()

endurance = round((ts[-1]-ts[0])/60., 1)
n = 3  # the larger n is, the smoother curve will be


dOCV = np.array([R_total * -x for x in Is[:]])
OCV = np.array(Us[:]) + dOCV

av_current = round(-np.average(Is), 1)
av_voltage = np.average(OCV)

# smooth_Us = lfilter([1.0 / n] * n, 1, Us[start:stop])[1:]
smooth_Us = lfilter([1.0 / n] * n, 1, OCV)
smooth_Is = -lfilter([1.0 / n] * n, 1, Is[:])
smooth_Tsp = lfilter([1.0 / n] * n, 1, Tsp[:])
smooth_Tsa = lfilter([1.0 / n] * n, 1, Tsa[:])

A_zero = min(As[:])
As_i = [x - A_zero for x in As[:]]
capacity = max(As_i)
caps.append(capacity)
actual_energy = round(capacity*av_voltage, 1)
energy = round(capacity * sum(smooth_Us)/len(smooth_Us), 1)


ax1.plot(As_i, smooth_Us, c=colors[0], ls='-', label='I_avg = {!s}A, E_extracted = {!s}Wh, endurance = {!s}min'.
         format(av_current, actual_energy, endurance))


ax2.plot(As_i, smooth_Tsp, c=colors[0], ls='-.', label='{!s}A [T]'.format(av_current))
# ax2.plot(As_i, smooth_Tsa, c=colors[0], ls='-.', label='{!s}A [T]'.format(av_current))

ax2.plot(As_i, smooth_Is, c=colors[0], ls=':', label='{!s}A [A]'.format(av_current), lw=2.)
ax1.set_xlabel('Capacity [Ah]')
ax1.set_ylabel('Open Circuit Voltage [V]')
ax2.set_ylabel('Temperature [deg C], Current [A]')
ax1.set_xlim(0, 1.1*max(caps))
ax1.set_ylim(10, 30)
ax2.set_ylim(0, 80)

ax1.plot(np.nan, np.nan, ls=':', label='Current', c='k', lw=2.)
ax1.plot(np.nan, np.nan, ls='-.', label='Temperature', c='k', lw=1.5)

plt.title('ID: {!s}, charged CC-CV at 0.7C with cutoff at 0.05C'.format(name))

ax1.legend(loc=0)

ax1.grid(True)
plt.savefig('./{!s}.png'.format(name), dpi=250, format='png')  # Use eps for LaTeX, other options: png, pdf, ps, eps
plt.show()
