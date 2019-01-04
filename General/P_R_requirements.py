__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"

import numpy as np
import matplotlib.pyplot as plt


U_range = np.arange(2.5, 3.8, 0.01)
C_rates = [1., 4.]
capacity = 3.24e-3  # Ah
I_rates = np.array(C_rates) * capacity


def resisting(u, c):
    r = np.array(u)/(capacity*c)
    return r


def power_dissipation(i, u):
    p = np.array(u)*np.array(i)
    return p


for i in range(len(C_rates)):
    R = np.empty((len(C_rates), len(U_range)))
    R[i, :] = resisting(U_range, C_rates[i])

# print '{!s} < R < {!s}'.format(R[1:, :].min(), R[1:].max())
