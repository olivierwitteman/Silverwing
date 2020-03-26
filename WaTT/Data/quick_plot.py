import matplotlib.pyplot as plt
import numpy as np


path = '.'
day = 8


def readinput(ns):
    with open('./{!s}jan-Table 1.csv'.format(day), 'r') as d:
        inputs = d.readlines()

        linenumber, id, r_pwr, deflection = [], [], [], []
        for i in range(len(inputs)):
            try:
                linenumber.append(int(inputs[i].replace(';', ',').split(',')[0][:]))
                r_pwr.append(int(inputs[i].replace(';', ',').split(',')[4][:].strip()))
            except:
                linenumber = linenumber[:i-1]
                r_pwr = r_pwr[:i-1]
    p = []
    for j in ns:
        p.append(r_pwr[j])
        p.append(r_pwr[j])
    print p
    return p


def readd():
    f0s = []
    rpm0s = []
    p0s = []
    ns = []
    with open('./WaTT_{!s}jan.log'.format(day), 'r') as logfile:
        dfs = logfile.readlines()
    for i in range(len(dfs)):
        f0s.append(float(dfs[i].split(',')[8]))
        f0s.append(float(dfs[i].split(',')[9]))
        rpm0s.append(float(dfs[i].split(',')[3]))
        rpm0s.append(float(dfs[i].split(',')[4]))
        p0s.append(float(dfs[i].split(',')[5])/2)
        p0s.append(float(dfs[i].split(',')[5]) / 2)
        ns.append(int(dfs[i].split(',')[0]))

    colors = np.array(p0s)
    return rpm0s, f0s, colors, ns


rpm0s, f0s, colors, ns = readd()
ps = readinput(ns=ns)
ps.append(20)
ps.append(40)
rpm0s.append(3000)
rpm0s.append(3600)
f0s.append(25)
f0s.append(30)

cs = np.array(ps)
plt.scatter(ps, rpm0s, c=f0s)

plt.ylabel('W0 [rpm]')
plt.xlabel('power setting [%pwm]')
plt.title('Colors show F0 [N]')
plt.colorbar()
plt.show()