import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

R_battery = 6.*0.0128/4.

name = 'BT-E-1800_1200-80_40-6'
namePCC = 'BT-E-1800_1200-80_40-6_PCC'
namecell = 'US18650_VTC6_fp_feb'

# axarr[0] = plt.subplots(211)
# axarr[1] = plt.subplot(212)

# Two subplots, the axes array is 1-d
fig, axarr = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]})


def plot(x, y, label, axis='l', color='b'):
    # You can change plot to scatter or whatever if you'd like
    # colors: b, g, r, c, m, y, k, w or HEX values as '#eeefff'

    if axis == 'u':
        # axarr[0].plot(x, y)
        # axarr[1].plot(np.nan, np.nan, label=label)

        axarr[0].plot(x, y, label=label, c=color)

    elif axis == 'l':
        # axarr[1].plot(x, y, label=label)
        axarr[1].plot(x, y, label=label, c=color)

    else:
        print('Please choose axis="l" or axis="r"')


def remove_last(Us, ts, Is, Tsp, Tsa, As, Cs):

    Us = Us[:-2]
    ts = ts[:-2]
    Is = Is[:-2]
    Tsp = Tsp[:-2]
    Tsa = Tsa[:-2]
    As = As[:-2]
    Cs = Cs[:-2]

    # new_array = []
    # print array
    #
    # for j in range(len(array)):
    #     new_array.append([array[j][:-2]])
    #
    # print new_array
    # return new_array

    return Us, ts, Is, Tsp, Tsa, As, Cs


def pack_data(name):
    path = './'
    with open('{!s}{!s}.log'.format(path, name), 'r') as data:
        samples = data.readlines()
        Us, Is, ts, As, Tsp, Tsa, rmrk, Cs = [], [], [], [0.], [], [], [], []

    for i in np.arange(0, len(samples), 10):
        try:
            Us.append(float(samples[i].split()[1][1:].strip())/6.)
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip())/4.)
            Cs.append(-Is[-1]/3.)
            Tsa.append(float(samples[i].split()[3][3:].strip()))
            Tsp.append(float(samples[i].split()[4][3:].strip()))

            if i > 1:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt / 3600.))

            if Is[-1] > 0 or Tsp[-1] < -100. or Tsa[-1] < -100.:
                # print(len(Us))
                raise KeyboardInterrupt

        except:
            Us, ts, Is, Tsp, Tsa, As, Cs = remove_last(Us, ts, Is, Tsp, Tsa, As, Cs)
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


    endurance = round((ts[-1] - ts[0]) / 60., 1)
    n = 10  # the larger n is, the smoother curve will be

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

    return As_i, smooth_Us, smooth_Is, smooth_Tsp, Cs


def cell_data(name):
    with open('./{!s}.log'.format(name), 'r') as data:
        samples = data.readlines()

        Us, Is, ts, As, c_s_mark, d_s_mark, c_e_mark, d_e_mark, Ts, rmrk, Cs = [], [], [], [0.], [], [], [],\
                                                                               [], [], [], []
        for i in range(len(samples)):
            try:
                Us.append(float(samples[i].split()[1][1:].strip()))
                ts.append(float(samples[i].split()[0][1:].strip()))
                Is.append(float(samples[i].split()[2][1:].strip()))
                Cs.append(-Is[-1]/3.)
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
                    As.append(float(As[-1] + Is[-1] * dt / 3600.))

            except:
                pass

    As = [-x + max(As) for x in As]

    start, stop = ts.index(d_s_mark[0]) + 1, ts.index(d_e_mark[0]) - 1
    av_current = abs(round(sum(Is[start:stop]) / (stop - start), 1))
    av_voltage = round(sum(Us[start:stop]) / (stop - start), 1)
    caps = []

    R_sys = 0.008
    R_total = R_sys + R_battery

    # print R_sys
    # lst = [0, -1]

    j = 0
    # for j in range(len(d_s_mark)):  # '-1!!!!!!!!!!'

    start, stop = ts.index(d_s_mark[j]) + 1, ts.index(d_e_mark[j]) - 1
    endurance = round((d_e_mark[j] - d_s_mark[j]) / 60., 1)
    n = 10  # the larger n is, the smoother curve will be

    av_voltage = round(sum(Us[start:stop]) / (stop - start), 1)
    av_current = -round(sum(Is[start:stop]) / (stop - start))

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
    actual_energy = round(capacity * av_voltage, 1)
    energy = round(capacity * sum(smooth_Us) / len(smooth_Us), 1)

    return As_i, smooth_Us, smooth_Is, smooth_Ts, Cs


As0, Us0, Is0, Tsp0, Cs0 = pack_data(name)
# As1, Us1, Is1, Tsp1, Cs1 = pack_data(namePCC)
As2, Us2, Is2, Tsp2, Cs2 = cell_data(namecell)

start = 10
plot(As0[start:], Tsp0[start:], 'Pack w/o PCC', 'u', color='b')
plot(As2[start:], Tsp2[start:], 'Individual cell', 'u', color='g')
plot(As0[:], Cs0[:], 'C-rate', 'l', color='k')

title = 'Normalized BTS thermal data'

axarr[0].set_title(title)

axarr[1].set_xlabel('Capacity [Ah]')

axarr[0].set_ylabel('Temperature [deg C]')
axarr[0].set_ylim(15, 70)

axarr[1].set_ylabel('Discharge rate [c]')
axarr[1].set_ylim(0, 7)

axarr[0].legend(loc=0)
axarr[1].legend(loc=0)
axarr[0].grid(True)
axarr[1].grid(True)


# plt.savefig('./{!s}'.format(title), dpi=255, format='eps')  # Use eps for LaTeX, other options: png, pdf, ps, eps
plt.show()
