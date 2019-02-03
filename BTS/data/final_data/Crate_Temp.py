import numpy as np
import matplotlib.pyplot as plt



R_battery = 6.*0.0128/4.


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