__author__ = "Olivier Witteman"
__email__ = "olivier@2001.net"

import matplotlib.pyplot as plt
import numpy as np

Clst = [4, 4, 1, 1, 4, 4]
tlst = [0, 3, 3, 17, 17, 20]
SoC = [100, 80, 80, 50, 50, 30]
EoLSoC = [90, 70, 70, 40, 40, 20]

fig, ax0 = plt.subplots()
ax0.plot(tlst, Clst, label='C-rate w.r.t. original battery capacity', c='b')
ax0.plot(np.nan, label='Ideal State of Charge (SoC)', c='r')
ax0.plot(np.nan, label='EoL State of Charge', c='g')
ax0.set_ylabel('C-rate')

ax1 = ax0.twinx()
ax1.plot(tlst, SoC, label='Ideal State of Charge (SoC)', c='r')
ax1.plot(tlst, EoLSoC, c='g', linewidth=2.)
ax1.plot(tlst, EoLSoC, c='g', linewidth=2.)
ax1.set_ylabel('SoC [%]')

ax0.set_xlabel('Time [minutes]')

ax0.grid(), ax1.grid(), ax0.legend(loc=0), plt.title('Discharge test')

plt.show()