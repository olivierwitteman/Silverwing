import matplotlib.pyplot as plt
from scipy.signal import lfilter
import numpy as np
import scipy.signal as scs

'''OCV'''

# nom_voltage = float(input('Nominal voltage of tested cell [V]: '))
mode = 0

# R_battery = 0.0
R_battery = 6.*0.0128/4.
textsize = 17.5
width = 7.5

path = './'
# path = '/Users/olivierwitteman/Downloads/'
# name = 'BT-B-1_1'
# name = 'BT-E-1800_1200-80_40-6_PCC'
name = 'US18650_VTC6_fp_feb'


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scs.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scs.filtfilt(b, a, data)
    return y


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

for i in np.arange(0, len(samples), 1):
    try:

        Us.append(float(samples[i].split()[1][1:].strip()))
        ts.append(float(samples[i].split()[0][1:].strip()))
        Is.append(float(samples[i].split()[2][1:].strip()))
        # print(float(samples[i].split()[3][3:-2].strip()))
        # Tsa.append(float(samples[i].split()[3][3:].strip()))
        # print(float(samples[i].split()[4][3:-2].strip()))
        Tsp.append(float(samples[i].split()[3][1:-2].strip()))

        # if Tsp[-1] < -100.:
        #     raise KeyboardInterrupt

        if i > 0:
            dt = ts[-1] - ts[-2]
            As.append(float(As[-1] + Is[-1] * dt / 3600.))

            if Tsp[-1] < 10:
                Tsa = [0, 0]
                raise KeyboardInterrupt

    except:
        # print('ass\n\n\n')
        Tsa = [0, 0]
        Us, ts, Is, Tsp, Tsa, As = remove_last(Us, ts, Is, Tsp, Tsa, As)
        pass


maxlength = min(len(Us), len(ts), len(Is), len(Tsp), len(As))
Us = Us[:maxlength]
ts = ts[:maxlength]
Is = Is[:maxlength]
Tsp = Tsp[:maxlength]
# Tsa = Tsa[:maxlength]
As = As[:maxlength]

As = [-x + max(As) for x in As]


fig, ax1 = plt.subplots(figsize=(width, width/1.6))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']

# start, stop = ts.index(d_s_mark[0]) + 1, ts.index(d_e_mark[0]) - 1

caps = []

R_sys = 0.0
R_total = R_sys + R_battery

ax2 = ax1.twinx()
ax2.grid()

endurance = round((ts[-1]-ts[0])/60., 0)
n = 15  # the larger n is, the smoother curve will be

dOCV = np.array([R_total * -x for x in Is[:]])
OCV = np.array(Us[:]) + dOCV

av_current = round(-np.average(Is), 1)
av_voltage = np.average(OCV)

# Filter requirements.
order = 1
fs = 10.  # sample rate, Hz
cutoff = .1  # desired cutoff frequency of the filter, Hz

Tsp_butter = butter_lowpass_filter(Tsp, cutoff, fs, order=order)

# smooth_Us = lfilter([1.0 / n] * n, 1, Us[start:stop])[1:]
smooth_Us = lfilter([1.0 / n] * n, 1, OCV)
smooth_Is = -lfilter([1.0 / n] * n, 1, Is[:])
smooth_Tsp = lfilter([1.0 / n] * n, 1, Tsp[:])
# smooth_Tsa = lfilter([1.0 / n] * n, 1, Tsa[:])

A_zero = min(As[:])
As_i = [x - A_zero for x in As[:]]
capacity = max(As_i)
caps.append(capacity)
actual_energy = round(capacity*av_voltage, 1)
energy = round(capacity * sum(smooth_Us)/len(smooth_Us), 1)

c = np.array(smooth_Is)/capacity


ax1.scatter(np.nan, np.nan, label='$E$ = {!s} Wh'.format(actual_energy))
ax1.scatter(np.nan, np.nan, label='$t$ = {!s} mins'.format(endurance))
ax1.plot(As_i, smooth_Us, c=colors[0], ls='-', label='Voltage')
ax2.plot(As_i, Tsp_butter, c='r', ls='-.', label='Temperature'.format(av_current))
ax1.plot(As_i, c, c='g', ls=':', label='C-rate'.format(av_current), lw=2.)


ax1.set_xlabel('Capacity [Ah]', fontsize=textsize)
ax1.set_ylabel('Voltage [V], Disch. Rate', fontsize=textsize)
ax2.set_ylabel('Temperature [deg C]', fontsize=textsize)

label1 = 'I_avg = {!s}A, E_extracted = {!s}Wh, endurance = {!s}min'\
    .format(av_current, actual_energy, endurance)


# ax2.plot(As_i, Tsp_butter, c=colors[0], ls='-.', label='{!s}A [T]'.format(av_current))

# ax2.plot(As_i, smooth_Tsa, c=colors[0], ls='-.', label='{!s}A [T]'.format(av_current))

# ax2.plot(As_i, smooth_Is, c=colors[0], ls=':', label='{!s}A [A]'.format(av_current), lw=2.)

ax1.set_xlim(0, 1.02*max(caps))
ax1.set_ylim(0, 7)
ax2.set_ylim(20, 45)

# ax1.plot(np.nan, np.nan, ls=':', label='Current', c='k', lw=2.)
ax1.plot(np.nan, np.nan, ls='-.', label='Temperature', c='r')

# plt.title('ID: {!s}, charged CC-CV at 0.7C with cutoff at 0.05C'.format(name))
# plt.title('Sony VTC6 at flight profile', fontsize=textsize)

ax1.legend(loc='center', fontsize=textsize, ncol=3, bbox_to_anchor=(0.5, 1.18))

# ax1.set_yticks([20, 30, 40, 50, 60, 70])
# ax2.set_yticks([0, 2.5, 5.])
ax1.tick_params(labelsize=14)
ax2.tick_params(labelsize=14)

plt.tight_layout()

ax1.grid(True)
plt.savefig('./{!s}.eps'.format(name), dpi=255, format='eps')  # Use eps for LaTeX, other options: png, pdf, ps, eps
plt.show()
