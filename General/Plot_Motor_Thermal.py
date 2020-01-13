import matplotlib.pyplot as plt

path = './'
name = 'tempdata'

with open('{!s}{!s}.csv'.format(path, name), 'r') as data:
    samples = data.readlines()
    t, T_housing, T_stator, T_rotor, T_magnet, T_windings = [], [], [], [], [], []


for i in range(8, len(samples), 1):


    try:

        t.append(float(samples[i].split(',')[2][:]))
        T_housing.append(float(samples[i].split(',')[59][:]))
        T_stator.append(float(samples[i].split(',')[21][:]))
        T_rotor.append(float(samples[i].split(',')[23][:]))
        T_magnet.append(float(samples[i].split(',')[25][:]))
        T_windings.append(float(samples[i].split(',')[237][:]))


    except:
        # print 'error'
        pass

# print(T_windings)

width = 7.5
fig, ax1 = plt.subplots(figsize=(width, width/1.5))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']


textsize = 17

ax1.plot(t, T_housing, label='Bearings', c=colors[0], ls='-')
ax1.plot(t, T_stator, label='Stator', c=colors[1], ls='-.')
ax1.plot(t, T_rotor, label='Rotor', c=colors[2], ls='--')
ax1.plot(t, T_magnet, label='Magnets', c=colors[3], ls=':')
ax1.plot(t, T_windings, label='Windings', c=colors[4], ls='-')
ax1.plot(t, len(t)*[max(T_windings)], c='k', lw=1., ls=':')

ax1.set_yticks([50, 100, 150, 200, 250, int(round(max(T_windings)))])

ax1.tick_params(labelsize=14.)

plt.xlabel('Time [$s$]', fontsize=textsize)
plt.ylabel('Temperature [$deg C$]', fontsize=textsize)

plt.legend(loc='upper center', fontsize=textsize, ncol=3, bbox_to_anchor=(0.5, 1.15))
plt.grid()

ax1.set_ylim(30, 300)
ax1.set_xlim(0, 1800)

plt.savefig('./{!s}'.format('Motor_Temp.png'), dpi=255, format='png')
plt.tight_layout()

plt.show()
