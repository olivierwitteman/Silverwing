import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import scipy.signal as scs

R_battery = 6.*0.0128/4.
textsize = 15
interval = 1

name = 'BT-E-1800_1200-80_40-6'
namePCC = 'BT-E-1800_1200-80_40-6_PCC'
namecell = 'US18650_VTC6_fp_feb'

# axarr[0] = plt.subplots(211)
# axarr[1] = plt.subplot(212)

# Two subplots, the axes array is 1-d
width = 7.5
fig, axarr = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [2, 1]}, figsize=(width, width/1.5))


def plot(x, y, label, axis='l', color='b', linetype='-'):
    # You can change plot to scatter or whatever if you'd like
    # colors: b, g, r, c, m, y, k, w or HEX values as '#eeefff'

    if axis == 'u':
        # axarr[0].plot(x, y)
        # axarr[1].plot(np.nan, np.nan, label=label)

        axarr[0].plot(x, y, label=label, c=color, ls=linetype)

    elif axis == 'l':
        # axarr[1].plot(x, y, label=label)
        axarr[1].plot(x, y, label=label, c=color, ls=linetype)

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

    return Us, ts, Is, Tsp, Tsa, As, Cs


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scs.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = scs.filtfilt(b, a, data)
    return y


def pack_data(name):
    # Filter requirements.
    order = 5
    fs = 10.  # sample rate, Hz
    cutoff = 0.01  # desired cutoff frequency of the filter, Hz

    path = './'
    with open('{!s}{!s}.log'.format(path, name), 'r') as data:
        samples = data.readlines()
        Us, Is, ts, As, Tsp, Tsa, rmrk, Cs = [], [], [], [0.], [], [], [], []

    for i in np.arange(0, len(samples), interval):
        try:
            Us.append(float(samples[i].split()[1][1:].strip())/6.)
            ts.append(float(samples[i].split()[0][1:].strip()))
            Is.append(float(samples[i].split()[2][1:].strip())/4.)
            Cs.append(-Is[-1]/3.)
            Tsa.append(float(samples[i].split()[3][3:].strip()))
            if name == 'BT-E-1800_1200-80_40-6':
                Tsp.append(float(samples[i].split()[4][3:].strip()) + 8.)
            else:
                Tsp.append(float(samples[i].split()[4][3:].strip()))
            if i > 1:
                dt = ts[-1] - ts[-2]
                As.append(float(As[-1] + Is[-1] * dt / 3600.))

            if Is[-1] > 0 or Tsp[-1] < -100. or Tsa[-1] < -100.:
                # print(len(Us))
                raise KeyboardInterrupt

        except:
            Us, ts, Is, Tsp, Tsa, As, Cs = remove_last(Us, ts, Is, Tsp, Tsa, As, Cs)
            pass

    maxlength = min(len(Us), len(ts), len(Is), len(Tsp), len(Tsa), len(As))
    Us = Us[:maxlength]
    ts = ts[:maxlength]
    Is = Is[:maxlength]
    Tsp = Tsp[:maxlength]
    Tsa = Tsa[:maxlength]
    As = As[:maxlength]
    Cs = Cs[:maxlength]

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

    smooth_Us = lfilter([1.0 / n] * n, 1, OCV)
    smooth_Is = -lfilter([1.0 / n] * n, 1, Is[:])
    smooth_Tsp = lfilter([1.0 / n] * n, 1, Tsp[:])
    smooth_Tsa = lfilter([1.0 / n] * n, 1, Tsa[:])

    A_zero = min(As[:])
    As_i = [x - A_zero for x in As[:]]

    Tsp_butter = butter_lowpass_filter(Tsp, cutoff, fs, order=order)

    capacity = max(As_i)
    As_i = [x*100./capacity for x in As_i]

    caps.append(capacity)
    actual_energy = round(capacity * av_voltage, 1)
    energy = round(capacity * sum(smooth_Us) / len(smooth_Us), 1)

    return As_i, smooth_Us, smooth_Is, Tsp_butter, Cs, ts


def cell_data(name):
    # Filter requirements.
    order = 1
    fs = 10.  # sample rate, Hz
    cutoff = 0.1  # desired cutoff frequency of the filter, Hz
    with open('./{!s}.log'.format(name), 'r') as data:
        samples = data.readlines()

        Us, Is, ts, As, c_s_mark, d_s_mark, c_e_mark, d_e_mark, Ts, rmrk, Cs = [], [], [], [0.], [], [], [],\
                                                                               [], [], [], []
        for i in range(0, len(samples), interval):
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
                #
                # if float(Ts[-1]) == -101.:
                #     d_s_mark.append(ts[-1])
                #
                # elif float(Ts[-1]) == -102.:
                #     d_e_mark.append(ts[-1])
                #
                # elif float(Ts[-1]) == -103.:
                #     c_s_mark.append(ts[-1])
                #
                # elif float(Ts[-1]) == -104.:
                #     c_e_mark.append(ts[-1])

                if i > 0:
                    dt = ts[-1] - ts[-2]
                    As.append(float(As[-1] + Is[-1] * dt / 3600.))

                    if Ts[-1] < 10 or Is[-1] > -1.:
                        Tsa = [0, 0]
                        Us, ts, Is, Ts, Tsa, As, Cs = remove_last(Us, ts, Is, Ts, Tsa, As, Cs)

            except:
                pass

    As = [-x + max(As) for x in As]

    maxlength = min(len(Us), len(ts), len(Is), len(Ts), len(As))
    Us = Us[:maxlength]
    ts = ts[:maxlength]
    Is = Is[:maxlength]
    Ts = Ts[:maxlength]
    As = As[:maxlength]
    Cs = Cs[:maxlength]


    # av_current = abs(round(sum(Is[start:stop]) / (stop - start), 1))
    # av_voltage = round(sum(Us[start:stop]) / (stop - start), 1)
    caps = []

    R_sys = 0.008
    R_total = R_sys + R_battery

    start, stop = 0, -1
    endurance = round((ts[stop] - ts[start])/60.)
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

    As_i = [x*100./capacity for x in As_i]

    caps.append(capacity)

    Ts_butter = butter_lowpass_filter(Ts[start:stop], cutoff, fs, order=order)

    actual_energy = round(capacity * av_voltage, 1)
    energy = round(capacity * sum(smooth_Us) / len(smooth_Us), 1)

    # return As_i, smooth_Us, smooth_Is, Ts[start:stop], Cs
    return As_i, smooth_Us, smooth_Is, Ts_butter, Cs[start:stop]


As0, Us0, Is0, Tsp0, Cs0, ts0 = pack_data(name)
As1, Us1, Is1, Tsp1, Cs1, ts1 = pack_data(namePCC)
As2, Us2, Is2, Tsp2, Cs2 = cell_data(namecell)

start = 0
# plot(As0[start:], Tsp0[start:], 'Pack w/o PCC', 'u', color='b', linetype='-.')
# plot(As1[start:], Tsp1[start:], 'Pack with PCC', 'u', color='r', linetype='-')
# plot(As2[start:], Tsp2[start:], 'Cell', 'u', color='g', linetype='--')


plot(As0[start:], Tsp0[start:], 'Pack w/o PCC', 'u', color='b', linetype='-.')
plot(As1[start:], Tsp1[start:], 'Pack with PCC', 'u', color='r', linetype='-')
# plot(ts[start:], Tsp2[start:], 'Cell', 'u', color='g', linetype='--')

plot(As2[:], Cs2[:], 'C-rate', 'l', color='k')
# plot(ts1[:], Cs1[:], 'C-rate', 'l', color='k')

title = 'BTS thermal data'

# axarr[0].set_title(title, fontsize=textsize)

axarr[1].set_xlabel('Depth of Discharge [%]', fontsize=textsize)

axarr[0].set_ylabel('Temp. [deg C]', fontsize=textsize)
axarr[0].set_ylim(10, 70)

axarr[1].set_ylabel('Disch. rate [c]', fontsize=textsize)
axarr[1].set_ylim(0, 7)

axarr[0].legend(loc='upper center', fontsize=textsize, ncol=3, bbox_to_anchor=(0.5, 1.3))
# axarr[1].legend(loc='center', fontsize=textsize, ncol=3, bbox_to_anchor=(0.5, 1.15))
axarr[0].grid(True)
axarr[1].grid(True)


axarr[0].set_yticks([20, 30, 40, 50, 60, 70])
axarr[1].set_yticks([0, 2.5, 5.])
axarr[0].tick_params(labelsize=14)
axarr[1].tick_params(labelsize=14)

plt.tight_layout()

plt.savefig('./{!s}'.format('BTS_Thermal.eps'), dpi=255, format='eps')  # Use eps for LaTeX, other options: png, pdf, ps, eps
plt.show()
