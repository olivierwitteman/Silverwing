import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter


path = './'
filename = 'loggerCommands_18'
# filename = 'loggerCommands_inv2'
steps = 20

with open('{!s}{!s}.csv'.format(path, filename), 'r') as data:
    samples = data.readlines()
    timestamp, rel_time, data_id, p_mech, dc_current, ac_current, ac_voltage, dc_voltage, set_speed, feedback_speed,\
    timestamp_feedback_speed, set_torque, feedback_torque, timestamp_feedback_torque, PCB_temperature, \
    motor_temperature, ain1, ain2, ain3, ain4, inv_temp_A, inv_temp_B, inv_temp_C = [], [], [], [], [], [], [], [], \
                                                                                    [], [], [], [], [], [], [], [], [],\
                                                                                    [], [], [], [], [], []

for i in np.arange(1, len(samples), steps):
    # timestamp
    timestamp.append(float(samples[i].split(',')[0][:].strip()))
    # relative time
    rel_time.append(float(samples[i].split(',')[1][:].strip()))
    # id
    data_id.append(str(samples[i].split(',')[2][:].strip()))
    # # mechanical power
    # p_mech.append(float(samples[i].split(',')[3][:].strip()))
    # dc current
    dc_current.append(float(samples[i].split(',')[4][:].strip()))
    # ac current
    ac_current.append(float(samples[i].split(',')[5][:].strip()))
    # ac voltage
    ac_voltage.append(float(samples[i].split(',')[6][:].strip()))
    # dc voltage
    dc_voltage.append(float(samples[i].split(',')[7][:].strip()))
    # set speed
    set_speed.append(float(samples[i].split(',')[8][:].strip()))
    # feedback speed
    feedback_speed.append(float(samples[i].split(',')[9][:].strip()))
    # timestamp speed measurement
    timestamp_feedback_speed.append(float(samples[i].split(',')[10][:].strip()))
    # set torque
    set_torque.append(float(samples[i].split(',')[11][:].strip()))
    # feedback torque
    feedback_torque.append(float(samples[i].split(',')[12][:].strip()))
    # timestamp torque measurement
    timestamp_feedback_torque.append(float(samples[i].split(',')[13][:].strip()))
    # PCB temperature
    PCB_temperature.append(float(samples[i].split(',')[14][:].strip()))
    # INV terminal A temperature
    inv_temp_A.append(float(samples[i].split(',')[15][:].strip()))
    # INV terminal B temperature
    inv_temp_B.append(float(samples[i].split(',')[16][:].strip()))
    # INV terminal C temperature
    inv_temp_C.append(float(samples[i].split(',')[17][:].strip()))
    # Motor temperature
    motor_temperature.append(float(samples[i].split(',')[18][:].strip()))
    # Analog input 1
    ain1.append(float(samples[i].split(',')[19][:].strip()))
    # Analog input 2
    ain2.append(float(samples[i].split(',')[20][:].strip()))
    # Analog input 3
    ain3.append(float(samples[i].split(',')[21][:].strip()))
    # Analog input 4
    ain4.append(float(samples[i].split(',')[22][:].strip()))


samplerate = round(len(timestamp)/(timestamp[-1] - timestamp[0])*1e3, 1)
print('Sampled rate: {!s} Hz'.format(samplerate))
print('Available sample rate: {!s} Hz'.format(round(samplerate*steps)))


n = 30
feedback_torque = lfilter([1.0 / n] * n, 1, feedback_torque)
dc_current = lfilter([1.0 / n] * n, 1, dc_current)


width = 10.
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']
fig, ax1 = plt.subplots(figsize=(width, width/1.6))
ax2 = ax1.twinx()
ax2.grid()

ax1.set_ylabel('Power, torque, current')
ax1.set_ylim([-2, 16])
ax1.set_xlabel('Timestamp [s since epoch]')

ax2.set_ylabel('Voltage, speed')

# ax1.plot(timestamp, p_mech, label='Mechanical power [kW]', c=colors[0])
ax1.plot(timestamp, dc_current, label='DC current [I]', c=colors[1])
# ax1.plot(timestamp, ac_current, label='AC current [A]', c=colors[2])
ax2.plot(timestamp, ac_voltage, label='AC voltage [V]', c=colors[3])
ax2.plot(timestamp, dc_voltage, label='DC voltage [V]', c=colors[4])
ax1.plot(timestamp, np.array(dc_current)*np.array(dc_voltage)/1000., label='Power [kW]', c=colors[5])
ax2.plot(timestamp, set_speed, label='set speed [rpm]', c=colors[6])
ax2.plot(timestamp, feedback_speed, label='feedback speed [rpm]', c=colors[7])
ax1.plot(timestamp, set_torque, label='set torque [Nm]', c=colors[8])
ax1.plot(timestamp, feedback_torque, label='feedback torque [Nm]', c=colors[9])
# ax1.plot(timestamp, )


ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title(filename)
plt.show()
