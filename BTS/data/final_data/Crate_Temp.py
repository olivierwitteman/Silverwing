import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

R_battery = 6.*0.0128/4.

name = 'BT-E-1800_1200-80_40-6'
namePCC = 'BT-E-1800_1200-80_40-6_PCC'

fig, ax1 = plt.subplots(figsize=(10, 6.25))
ax2 = ax1.twinx()


def plot(x, y, label, axis='l', color='b'):
    # You can change plot to scatter or whatever if you'd like
    # colors: b, g, r, c, m, y, k, w or HEX values as '#eeefff'

    if axis == 'l':
        ax1.plot(x, y)
        ax2.plot(np.nan, np.nan, label=label)

    elif axis == 'r':
        ax1.plot(x, y, label=label)

    else:
        print('Please choose axis="l" or axis="r"')


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


def pack_data(name):
    path = './'
    with open('{!s}{!s}.log'.format(path, name), 'r') as data:
        samples = data.readlines()
        Us, Is, ts, As, Tsp, Tsa, rmrk = [], [], [], [0.], [], [], []

    for i in np.arange(0, len(samples), 10):
        try:
            Us.append(float(samples[i].split()[1][1:].strip()))
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip()))
            Tsa.append(float(samples[i].split()[3][3:].strip()))
            Tsp.append(float(samples[i].split()[4][3:].strip()))

            if i > 1:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt / 3600.))

            if Is[-1] > 0 or Tsp[-1] < -100. or Tsa[-1] < -100.:
                # print(len(Us))
                raise KeyboardInterrupt

        except:
            Us, ts, Is, Tsp, Tsa, As = remove_last(Us, ts, Is, Tsp, Tsa, As)
            # pass

    maxlength = min(len(Us), len(ts), len(Is), len(Tsp), len(Tsa), len(As))
    Us = Us[:maxlength]
    ts = ts[:maxlength]
    Is = Is[:maxlength]
    Tsp = Tsp[:maxlength]
    Tsa = Tsa[:maxlength]
    As = As[:maxlength]

    As = [-x + max(As) for x in As]

    caps = []

    R_sys = 0.0
    R_total = R_sys + R_battery

    ax2 = ax1.twinx()
    ax2.grid()

    endurance = round((ts[-1] - ts[0]) / 60., 1)
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
    actual_energy = round(capacity * av_voltage, 1)
    energy = round(capacity * sum(smooth_Us) / len(smooth_Us), 1)

    return As, smooth_Us, smooth_Is, smooth_Tsp


As0, Us0, Is0, Tsp0 = pack_data(name)
As1, Us1, Is1, Tsp1 = pack_data(namePCC)


title = 'Asshat'
plt.title(title)

ax1.set_xlabel('Time [s]')
ax1.set_xlim(0, 4)
ax2.set_xlim(0, 4)

ax1.set_ylabel('Voltage [V]')
ax1.set_ylim(0, 5)

ax2.set_ylabel('Current [A] / Temperature [C]')
ax2.set_ylim(0, 80)

ax2.legend(loc=0)
ax1.grid(True)
ax2.grid(True)

plt.savefig('./{!s}'.format(title), dpi=255, format='eps')  # Use eps for LaTeX, other options: png, pdf, ps, eps

plt.show()
