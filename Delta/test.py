import matplotlib.pyplot as plt
import numpy as np

f = [0, 1.77, 4.27]
u = [2.035, 1.67, 1.14]

plt.plot(f, u)

print((f[2]-f[0])/(u[2]-u[0]))
plt.grid()
correlation = np.corrcoef(f, u)[0,1]
r2 = correlation*correlation

print('R^2: {!s}'.format(r2))
# plt.show()
