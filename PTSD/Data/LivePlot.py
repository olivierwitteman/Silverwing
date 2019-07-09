import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter
import time
import glob
import os

path = './'

# filename = 'loggerCommands_18'
# filename = str(input('filename: '))
# filename = 'loggerCommands_inv2'

list_of_files = glob.glob('{!s}*.csv'.format(path)) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print('\nlatest file: {!s}\n'.format(latest_file))

steps = 10
lastline = 0

fig, (ax1, ax3, ax5) = plt.subplots(3, 1, sharex=True)
ax2 = ax1.twinx()
ax4 = ax3.twinx()
ax6 = ax5.twinx()

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()
ax5.grid()
ax6.grid()

ax1.set_ylabel('voltage, current, speed')
# ax1.set_ylim([-2, 16])
ax3.set_ylabel('torque, temperature')

ax5.set_ylabel('analog input, power')
ax5.set_xlabel('Time since epoch [s]')

colors = 2 * ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']
linestyles = ['-', '--', '-.', ':']
it = 0

while True:
    it += 1
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()
    timestamp, rel_time, data_id, p_mech, dc_current, ac_current, ac_voltage, dc_voltage, set_speed, feedback_speed, \
    timestamp_feedback_speed, set_torque, feedback_torque, timestamp_feedback_torque, PCB_temperature, \
    motor_temperature, ain1, ain5, ain3, ain4, ain6, inv_temp_A, inv_temp_B, inv_temp_C = [], [], [], [], [], [], [], [], \
                                                                                    [], [], [], [], [], [], [], [], \
                                                                                    [], [], [], [], [], [], [], []

    with open('{!s}{!s}'.format(path, latest_file), 'r') as data:
        samples = data.readlines()[1:]

    # lastline += len(samples)

    for i in np.arange(-6000, -1, steps):
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
        # Analog input 5
        ain5.append(float(samples[i].split(',')[20][:].strip()))
        # Analog input 3
        ain3.append(float(samples[i].split(',')[21][:].strip()))
        # Analog input 4
        ain4.append(float(samples[i].split(',')[22][:].strip()))
        # Analog input 6
        ain6.append(float(samples[i].split(',')[23][:].strip()))


        n = 30
        dc_current_filt = lfilter([1.0 / n] * n, 1, dc_current)
        motor_temperature_filt = lfilter([1.0 / n] * n, 1, motor_temperature)
        PCB_temperature_filt = lfilter([1.0 / n] * n, 1, PCB_temperature)
        inv_temp_A_filt = lfilter([1.0 / n] * n, 1, inv_temp_A)
        inv_temp_B_filt = lfilter([1.0 / n] * n, 1, inv_temp_B)
        inv_temp_C_filt = lfilter([1.0 / n] * n, 1, inv_temp_C)
        feedback_torque_filt = lfilter([1.0 / n] * n, 1, feedback_torque)
        timestamp = list(np.array(timestamp)-timestamp[-1] / 1e3)

    # return lastline, feedback_torque, dc_current

    # Power usage
    # ax1.plot(timestamp, p_mech, label='Mechanical power [kW]', c=colors[0])
    ax2.plot(timestamp, dc_current_filt, label='DC current (filtered) [I]', c=colors[1])
    # ax2.plot(timestamp, ac_current, label='AC current [A]', c=colors[2])
    ax1.plot(timestamp, ac_voltage, label='AC voltage [V]', c=colors[3])
    ax1.plot(timestamp, dc_voltage, label='DC voltage [V]', c=colors[4])

    # ax2.set_ylim([0, 50])
    ax2.plot(timestamp, np.array(dc_current_filt) * np.array(dc_voltage) / 1000., label='Power (filtered) [kW]',
             c=colors[5])

    # Speed and torque
    ax3.plot(timestamp, set_speed, label='set speed [rpm]', c=colors[6])
    ax3.plot(timestamp, feedback_speed, label='feedback speed [rpm]', c=colors[7])
    ax4.plot(timestamp, set_torque, label='set torque [Nm]', c=colors[8])
    # ax4.plot(timestamp, np.abs(feedback_torque), label='feedback torque [Nm]', c=colors[9])
    ax4.plot(timestamp, np.abs(feedback_torque_filt), label='feedback torque (filtered) [Nm]', c=colors[15])

    # Temperature
    ax5.set_ylim([20, 120])
    ax5.plot(timestamp, PCB_temperature_filt, label='Inv. PCB temp. (filtered) [deg C]', c=colors[10],
             linestyle=linestyles[1])
    ax5.plot(timestamp, motor_temperature_filt, label='Motor temp. (filtered) [deg C]', c=colors[11],
             linestyle=linestyles[1])
    ax5.plot(timestamp, inv_temp_A_filt, label='Inv. temp. A (filtered) [deg C]', c=colors[12], linestyle=linestyles[1])
    ax5.plot(timestamp, inv_temp_B_filt, label='Inv. temp. B (filtered) [deg C]', c=colors[13], linestyle=linestyles[1])
    ax5.plot(timestamp, inv_temp_C_filt, label='Inv. temp. C (filtered) [deg C]', c=colors[14], linestyle=linestyles[1])
    ax6.plot(timestamp, ain1, label='AIN 1 [V]', c=colors[15], linestyle=linestyles[1])
    ax6.plot(timestamp, ain5, label='AIN 5 [V]', c=colors[16], linestyle=linestyles[1])
    ax6.plot(timestamp, ain3, label='AIN 3 [V]', c=colors[17], linestyle=linestyles[1])
    ax6.plot(timestamp, ain4, label='AIN 4 [V]', c=colors[18], linestyle=linestyles[1])
    ax6.plot(timestamp, ain6, label='AIN 6 [V]', c=colors[19], linestyle=linestyles[1])

    if it == 1:
        fig.suptitle(latest_file)
    ax1.legend(loc='upper left', fontsize=5.)
    ax2.legend(loc='upper right', fontsize=5.)
    ax3.legend(loc='upper left', fontsize=5.)  # loc='upper right'
    ax4.legend(loc='upper right', fontsize=5.)
    ax5.legend(loc='upper left', fontsize=5.)
    ax6.legend(loc='upper right', fontsize=5.)

    plt.pause(1.)
