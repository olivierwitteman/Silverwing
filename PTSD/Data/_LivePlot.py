import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter
import time
import glob
import os

path = './'

list_of_files = glob.glob('{!s}*.csv'.format(path)) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print('\nlatest file: {!s}\n'.format(latest_file))

steps = 10
lastline = 0


def filterfunc(data, type='outlier', m=2, n=30):
    if type == 'outlier':
        data = np.array(data)
        data[abs(data - np.median(data)) > m * np.std(data)] = np.median(data)
        data = list(data)
    elif type == 'linear':
        data = lfilter([1.0 / n] * n, 1, data)
    else:
        print('Unknown filter requested, data has not been filtered.')
    return data


def temperature_calibration(v0):
    a = -0.1809802231E-3
    b = 3.319163836E-4
    c = -1.868674690E-7

    r = -np.array(v0)*100e3/(np.array(v0)-5.)

    T = 1./(a + b * np.log(r) + c * (np.log(r))**3) - 273.15

    return T, r


colors = 3 * ['b', 'g', 'c', 'm', 'y', 'k', 'g', 'c']
linestyles = ['-', '--', '-.', ':']

width = 16.
fig, (ax1, ax3, ax5, ax7) = plt.subplots(4, 1, sharex=True, figsize=(width, width/1.6))
fig.suptitle(latest_file)
ax2 = ax1.twinx()
ax4 = ax3.twinx()
ax6 = ax5.twinx()
ax8 = ax7.twinx()
# ax10 = ax9.twinx()

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()
ax5.grid()
ax6.grid()
ax7.grid()
ax8.grid()
# ax9.grid()
# ax10.grid()

ax1.set_ylabel('')
# ax1.set_ylim([-2, 16])
ax3.set_ylabel('')

ax5.set_ylabel('')
ax7.set_xlabel('Time since epoch [s]')
it = 0

while True:
    it += 1
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    ax5.clear()
    ax6.clear()
    ax7.clear()
    ax8.clear()
    timestamp, rel_time, data_id, p_mech, dc_current, ac_current, ac_voltage, dc_voltage, set_speed, feedback_speed, \
    timestamp_feedback_speed, set_torque, feedback_torque, timestamp_feedback_torque, PCB_temperature, \
    motor_temperature, ain1, ain5, ain3, ain4, ain6, inv_temp_A, inv_temp_B, inv_temp_C = [], [], [], [], [], [], [], [], \
                                                                                    [], [], [], [], [], [], [], [], \
                                                                                    [], [], [], [], [], [], [], []

    with open('{!s}{!s}'.format(path, latest_file), 'r') as data:
        samples = data.readlines()[1:]

    # lastline += len(samples)
    for i in np.arange(max([-18000, it*-25*steps]), -1, steps):
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

        # Filters
        timestamp = list(np.array(timestamp) / 1e3)
        dc_current_filt = filterfunc(dc_current, type='linear')
        dc_voltage_filt = filterfunc(dc_voltage, type='linear')
        motor_temperature_filt = filterfunc(motor_temperature, type='linear')
        PCB_temperature_filt = filterfunc(PCB_temperature, type='linear')
        inv_temp_A_filt = filterfunc(inv_temp_A, type='linear')
        inv_temp_B_filt = filterfunc(inv_temp_B, type='linear')
        inv_temp_C_filt = filterfunc(inv_temp_C, type='linear')
        feedback_torque_filt = filterfunc(feedback_torque, type='linear')
        ac_current_filt = filterfunc(np.abs(ac_current), type='linear')
        ac_voltage_filt = filterfunc(ac_voltage, type='linear')
        ain1_temp = temperature_calibration(ain1)[0]
        ain3_temp = temperature_calibration(ain3)[0]
        ain4_temp = temperature_calibration(ain4)[0]
        ain5_temp = temperature_calibration(ain5)[0]
        ain6_temp = temperature_calibration(ain6)[0]

        feedback_speed_filt = filterfunc(feedback_speed, m=10)

    timestamp = list(np.array(timestamp)-timestamp[-1])
    # return lastline, feedback_torque, dc_current

    # General, ax1, ax2
    ax1.set_ylabel('General', fontweight='bold')
    ax1.plot(timestamp, set_torque, label='set torque [Nm]', c=colors[0])
    # ax1.plot(timestamp, np.abs(feedback_torque), label='feedback torque [Nm]', c=colors[9])
    ax1.plot(timestamp, np.abs(feedback_torque_filt), label='feedback torque (filtered) [Nm]', c=colors[1])
    ax1.plot(timestamp, np.array(dc_current_filt) * np.array(dc_voltage_filt) / 1000., label='Power (filtered) [kW]',
             c=colors[2])

    # ax2.set_ylabel('rotational velocity')
    # ax2.plot(timestamp, set_speed, label='set speed [rpm]', c=colors[3], linestyle=linestyles[1])
    ax2.plot(timestamp, feedback_speed_filt, label='feedback speed [rpm]', c=colors[4], linestyle=linestyles[1])

    # Battery, ax3, ax4
    # ax4.set_ylabel('dc voltage\ncurrent')
    ax4.plot(timestamp, dc_voltage, label='DC voltage [V]', c=colors[5], linestyle=linestyles[1])
    ax4.plot(timestamp, dc_current_filt, label='DC current (filtered) [I]', c=colors[7], linestyle=linestyles[1])

    ax3.set_ylim([10., 80])
    ax3.plot([timestamp[0], timestamp[-1]], [60, 60], c='r', linestyle=linestyles[3], linewidth=2.)
    ax3.set_ylabel('Battery', fontweight='bold')
    ax3.plot(timestamp, ain4_temp, label='AIN 4 [deg C]', c=colors[0], linestyle=linestyles[0])
    ax3.plot(timestamp, ain6_temp, label='AIN 6 [deg C]', c=colors[1], linestyle=linestyles[0])
    ax3.plot(timestamp, ain1_temp, label='AIN 1 [deg C]', c=colors[2], linestyle=linestyles[0])
    ax3.plot(timestamp, ain5_temp, label='AIN 5 [deg C]', c=colors[3], linestyle=linestyles[0])
    ax3.plot(timestamp, ain3_temp, label='AIN 3 [deg C]', c=colors[4], linestyle=linestyles[0])

    # Inverter(s), ax5, ax6
    ax5.set_ylim([20., 150.])
    ax5.plot([timestamp[0], timestamp[-1]], [120, 120], c='r', linestyle=linestyles[3], linewidth=2.)
    ax5.set_ylabel('Inverter', fontweight='bold')
    ax5.plot(timestamp, PCB_temperature_filt, label='Inv. PCB temp. (filtered) [deg C]', c=colors[0],
             linestyle=linestyles[0])
    ax5.plot(timestamp, inv_temp_A_filt, label='Inv. temp. A (filtered) [deg C]', c=colors[1], linestyle=linestyles[0])
    ax5.plot(timestamp, inv_temp_B_filt, label='Inv. temp. B (filtered) [deg C]', c=colors[2], linestyle=linestyles[0])
    ax5.plot(timestamp, inv_temp_C_filt, label='Inv. temp. C (filtered) [deg C]', c=colors[3], linestyle=linestyles[0])

    # Motor(s), ax7, ax8
    ax7.set_ylim([20, 150.])
    ax7.plot([timestamp[0], timestamp[-1]], [120, 120], c='r', linestyle=linestyles[3], linewidth=2.)
    ax7.set_ylabel('Motor', fontweight='bold')
    ax7.plot(timestamp, motor_temperature_filt, label='Motor temp. (filtered) [deg C]', c=colors[0],
             linestyle=linestyles[0])

    # ax8.set_ylabel('ac voltage, current')
    ax8.plot(timestamp, ac_voltage_filt, label='AC voltage [V]', c=colors[1], linestyle=linestyles[1])
    ax8.plot(timestamp, ac_current_filt, label='AC current [A]', c=colors[2], linestyle=linestyles[1])

    if it == 1:
        fig.suptitle(latest_file)
    ax1.legend(loc='upper left', fontsize=7., bbox_to_anchor=(0., 1.18))
    ax2.legend(loc='upper right', fontsize=7., bbox_to_anchor=(1., 1.18))
    ax3.legend(loc='upper left', fontsize=7., bbox_to_anchor=(0., 1.18))
    ax4.legend(loc='upper right', fontsize=7., bbox_to_anchor=(1., 1.18))
    ax5.legend(loc='upper left', fontsize=7., bbox_to_anchor=(0., 1.18))
    ax6.legend(loc='upper right', fontsize=7., bbox_to_anchor=(1., 1.18))
    ax7.legend(loc='upper left', fontsize=7., bbox_to_anchor=(0., 1.18))
    ax8.legend(loc='upper right', fontsize=7., bbox_to_anchor=(1., 1.18))

    plt.pause(1.)
