import matplotlib.pyplot as plt
import numpy as np
checktime = int(1572106718250/1e3)
path = './'
filename = 'power_08_01_raw'
steps = 1
with open('{!s}{!s}.csv'.format(path, filename), 'r') as data:
    samples = data.readlines()
timestamp, voltage, current, power = [], [], [], []
for i in np.arange(1, len(samples), steps):
    try:
        # timestamp
        timestamp.append(float(samples[i].split(',')[0][:].strip()) - float(samples[0].split(',')[0][:].strip()))
        # timestamp.append(float(samples[i].split(',')[0][:].strip()) )
        # voltage
        voltage.append(float(samples[i].split(',')[1][:].strip()))
        # current
        current.append(float(samples[i].split(',')[2][:].strip()))
        # power
        power.append(float(samples[i].split(',')[3][:].strip()))
    except ValueError:
        timestamp = timestamp[:i-1]
        voltage = voltage[:i-1]
        current = current[:i-1] * 6
        power = power[:i-1]
dt = np.abs(np.array(timestamp)-checktime)
loc = dt.argmin()
power_at_time = round(power[loc]/1e3, 1)
current_at_time = round(current[loc], 2)
print('Power at lookup time: {!s}kW'.format(power_at_time))
print('Current at lookup time: {!s}A'.format(current_at_time))
print('dT = {!s}'.format(round(min(dt)), 2))
# plt.scatter(timestamp[loc], power[loc], c='r', s=10)
# plt.annotate('P = {!s}kW'.format(power_at_time), (timestamp[loc], power[loc]))
# plt.subplot(311)
# plt.plot(timestamp, power)
# plt.grid(True)
#
# plt.subplot(312)
# plt.plot(timestamp, voltage)
# plt.grid(True)
#
# plt.subplot(313)
plt.plot(timestamp, current)
# plt.plot(timestamp,power,c='g')
plt.plot(timestamp, voltage,c='r')
plt.grid(True)
plt.show()