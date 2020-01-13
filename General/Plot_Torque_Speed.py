import matplotlib.pyplot as plt


width = 7.5
fig, ax1 = plt.subplots(figsize=(width, width/1.7))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'r', 'g', 'c']


textsize = 15

rpm = [2000, 4000, 4500, 5000]


I105 = [165.014521314218, 164.560921492279, 155.47523083874, 143.025217238522]
I62 = [105.575449857752, 105.334346950993, 100.446342784174, 86.8021156589373]
I20 = [34.4619264311306, 34.2818164269501, 29.752582509365, 0.]

ax1.plot(rpm, I105, label='I = 105$A_{rms}$', c=colors[0], ls='-')
ax1.plot(rpm, I62, label='I = 62$A_{rms}$', c=colors[1], ls='-.')
ax1.plot(rpm, I20, label='I = 20$A_{rms}$', c=colors[2], ls='--')

plt.xlabel('Speed [$rpm$]', fontsize=textsize)
plt.ylabel('Torque [$Nm$]', fontsize=textsize)

plt.legend(loc='upper center', fontsize=textsize, ncol=3, bbox_to_anchor=(0.5, 1.15))
plt.grid()


plt.savefig('./{!s}'.format('Motor_T_omega.eps'), dpi=255, format='eps')
plt.tight_layout()

plt.show()