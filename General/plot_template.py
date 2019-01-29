import matplotlib.pyplot as plt
import numpy as np

fig, ax1 = plt.subplots()
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


# Example usage
plot([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], label='Nice')

title = 'Title'
plt.title(title)

ax1.set_xlabel('Time [s]')
ax1.set_xlim(0, 10)
ax2.set_xlim(0, 10)

ax1.set_ylabel('Voltage [V]')
ax1.set_ylim(0, 25)

ax2.set_ylabel('Current [A] / Temperature [C]')
ax2.set_ylim(0, 1.5)


ax2.legend()
ax1.grid(True)
ax2.grid(True)


plt.savefig('./{!s}'.format(title), dpi=255, format='eps')  # Use eps for LaTeX, other options: png, pdf, ps, eps
# plt.show()
