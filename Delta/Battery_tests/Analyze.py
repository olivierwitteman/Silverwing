import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np

'''OCV'''

# nom_voltage = float(input('Nominal voltage of tested cell [V]: '))
mode = 0

modes = ['reg', 'fp', 'cycle']
# R_battery = 0.013/4.
# R_battery = 0.0016
R_battery = 0
filename = 'VTC5A_t40_T30.0_P60.0'
with open('./Data/{!s}.log'.format(filename), 'r') as data:
    samples = data.readlines()

    Us, Is, ts, As, c_s_mark, d_s_mark, c_e_mark, d_e_mark, Ts, rmrk = [], [], [], [0.], [], [], [], [], [], []
    for i in range(len(samples)):
        try:
            Us.append(float(samples[i].split()[1][1:].strip()))
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip()))
            Ts.append(float(samples[i].split()[3][1:-2].strip()))
            try:
                rmrk.append(str(samples[i].split()[6][:].strip()))
            except:
                pass

            if float(Ts[-1]) == -101.:
                d_s_mark.append(ts[-1])

            elif float(Ts[-1]) == -102.:
                d_e_mark.append(ts[-1])

            elif float(Ts[-1]) == -103.:
                c_s_mark.append(ts[-1])

            elif float(Ts[-1]) == -104.:
                c_e_mark.append(ts[-1])

            if i > 0:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt/3600.))

        except:
            pass

print(np.average(Us))


As = [-x + max(As) for x in As]

fig, ax1 = plt.subplots()
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']

start, stop = ts.index(d_s_mark[0]) + 1, ts.index(d_e_mark[0]) - 1
av_current = abs(round(sum(Is[start:stop]) / (stop - start), 1))
av_voltage = round(sum(Us[start:stop]) / (stop - start), 1)
caps = []

R_sys = 0.03
R_total = R_sys + R_battery

# print R_sys
# lst = [0, -1]
if modes[mode] != 'cycle':
    ax2 = ax1.twinx()
    ax2.grid()


lst = [0]
# for j in range(len(d_s_mark)):  # '-1!!!!!!!!!!'
for j in lst:
    start, stop = ts.index(d_s_mark[j])+1, ts.index(d_e_mark[j])-1
    endurance = round((d_e_mark[j] - d_s_mark[j])/60., 1)
    n = 10  # the larger n is, the smoother curve will be

    av_voltage = round(sum(Us[start:stop]) / (stop-start), 1)
    av_current = -round(sum(Is[start:stop]) / (stop - start))

    dOCV = np.array([R_total * -x for x in Is[start:stop]])
    OCV = np.array(Us[start:stop]) + dOCV

    smooth_Us = lfilter([1.0 / n] * n, 1, Us[start:stop])
    # smooth_Us = lfilter([1.0 / n] * n, 1, OCV)
    smooth_Is = -lfilter([1.0 / n] * n, 1, Is[start:stop])
    smooth_Ts = lfilter([1.0 / n] * n, 1, Ts[start:stop])

    A_zero = min(As[start:stop])
    As_i = [x - A_zero for x in As[start:stop]]
    capacity = max(As_i)
    caps.append(capacity)
    actual_energy = round(capacity*av_voltage, 1)
    energy = round(capacity * sum(smooth_Us)/len(smooth_Us), 1)

    if modes[mode] == 'reg':
        ax1.plot(As_i, smooth_Us, c='b', ls='-', label='I_avg = {!s}A, E_extracted = {!s}Wh'.
                 format(av_current, actual_energy))

        ax2.plot(As_i, np.array(smooth_Us)*np.array(smooth_Is), label='Power [W]', c='g')
        ax1.plot(np.nan, np.nan, label='Power [W]', c='g', lw=1.5)

    elif modes[mode] == 'fp':
        ax1.plot(As_i, smooth_Us, c=colors[j], ls='-', label='I_avg = {!s}A, E_extracted = {!s}Wh, endurance = {!s}min'.
                 format(av_current, actual_energy, endurance))

    if modes[mode] == 'reg' or modes[mode] == 'fp':
        ax2.plot(As_i, smooth_Ts, c='r', ls='-.', label='{!s}A [T]'.format(av_current))
        ax2.plot(As_i, smooth_Is, c='b', ls=':', label='{!s}A [A]'.format(av_current), lw=2.)
        ax1.set_xlabel('Capacity [Ah]')
        ax1.set_ylabel('Open Circuit Voltage [V]')
        ax2.set_ylabel('Temperature [deg C], Current [A]')
        ax1.set_xlim(0, max(caps))
        ax1.set_ylim(2.0, 4.5)
        ax2.set_ylim(0, 120)
        # if j == len(d_s_mark)-1:
        ax1.plot(np.nan, np.nan, ls=':', label='Current', c='k', lw=2.)
        ax1.plot(np.nan, np.nan, ls='-.', label='Temperature', c='k', lw=1.5)

    else:
        if j == len(d_s_mark)-1:
            ax1.set_xlim(0, len(caps) * 1.1)
            ax1.plot(range(len(caps)), caps, label='Capacity loss over {!s} cycles of GoFly Silverwing flight '
                                                   'profile'.format(len(caps)))
            ax1.set_ylim(0.9*caps[-1], 1.1*caps[0])

# plt.title('Battery: {!s}, charged CC-CV at 1C with cutoff at 0.07C'.format(rmrk[0]))

ax1.legend(loc=0)

ax1.grid(True)
plt.savefig('./{!s}.png'.format(filename))
plt.show()
