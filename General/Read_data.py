import pickle
import matplotlib.pyplot as plt

# Normal pressure NO PCC
data = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/datadump_2016-03-28 19_19discharge.pickle", "rb"))

# Vacuum pressure NO PCC
data1 = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/datadump_2016-03-28 16_18discharge.pickle", "rb"))

# Normal pressure WITH PCC
voltdata2 = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/Amb_PCC_Voltage2016-09-16 15_03.pickle", "rb"))
tempdata2 = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/Amb_PCC_Temperature2016-09-16 15_03.pickle", "rb"))

# Vacuum pressure WITH PCC
voltdata3 = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/Vac_PCC_Voltage2016-09-16 15_04.pickle", "rb"))
tempdata3 = pickle.load(open("/Users/olivierwitteman/delfthyperloop.bitbucket.org/battery tests/data/Vac_PCC_Temperature2016-09-16 15_04.pickle", "rb"))

# avgvolt = sum(data['voltage'])/len(data['voltage'])

vlst = data['voltage']
templst = data['temp']
caplst = data['capacity']
curlst = data['current']


vlst1 = data1['voltage']
templst1 = data1['temp']
caplst1 = data1['capacity']
curlst1 = data1['current']


vlst2 = voltdata2['voltage']
vcaplst2 = (voltdata2['capacity'])
curlst2 = []

for i in range(len(vcaplst2)):
    curlst2.append(curlst[int(i*(float(len(curlst))/float(len(vcaplst2))))])
for j in range(len(vlst2)):
    if not 2.4 < vlst2[j] < 4.3:
        vlst2[j] = vlst2[j-1]

templst2 = tempdata2['temp']
caplst2 = tempdata2['capacity']
for i in range(len(templst2)):
    try:
        if templst2[i+1] < templst2[i]:
            templst2[i+1] = templst2[i]
    except:
        pass

vlst3 = voltdata3['voltage']
vcaplst3 = voltdata3['capacity']
curlst3 = []


for i in range(len(vcaplst3)):
    curlst3.append(curlst[int(i*(float(len(curlst))/float(len(vcaplst3))))])
for j in range(len(vlst3)):
    if not 2.4 < vlst3[j] < 4.3:
        vlst3[j] = vlst3[j-1]

templst3 = tempdata3['temp']
caplst3 = tempdata3['capacity']

for i in range(len(templst3)):
    try:
        if templst3[i + 1] < templst3[i]:
            templst3[i + 1] = templst3[i]
    except:
        pass

# vlst.append(data1['voltage'])
# templst.append(data1['temp'])
#
# for i in range(len(data1['voltage'])):
#     caplst.append(data1['capacity'][i] + data['capacity'][-1])

resistance = 0.10424242 # 2.74 ipv 3.6

for i in range(len(vlst)):
    vlst[i] = vlst[i] + curlst[i] * resistance
for i in range(len(vlst1)):
    vlst1[i] = vlst1[i] + curlst1[i] * resistance
for i in range(len(vlst2)):
    vlst2[i] = vlst2[i] + curlst2[i] * resistance
for i in range(len(vlst3)):
    vlst3[i] = vlst3[i] + curlst3[i] * resistance

vlst2[:35] = vlst[:35]
vlst3[:35] = vlst[:35]
print data['capacity'][-1]

fig = plt.figure()
vplot = fig.add_subplot(111)
vplot1 = fig.add_subplot(111)
vplot2 = fig.add_subplot(111)
vplot3 = fig.add_subplot(111)

# fig, vplot = plt.subplots()
vplot.plot(caplst[1:], vlst, color="blue", label="3C - Normal pressure - No PCC", linewidth="2")
tempplot = vplot.twinx()
tempplot.plot(caplst[1:], templst, color="blue", label="Temperature", linewidth="2")

vplot1.plot(caplst1[1:], vlst1, color="red", label="3C - Vacuum pressure - No PCC", linewidth="2")
tempplot.plot(caplst1[1:], templst1, color="red", label="Temperature", linewidth="2")

vplot2.plot(vcaplst2, vlst2, color="green", label="3C - Normal pressure - PCC", linewidth="2")
tempplot.plot(caplst2, templst2, color="green", label="Temperature", linewidth="2")

vplot2.plot(vcaplst3, vlst3, color="black", label="3C - Vacuum pressure - PCC", linewidth="2")
tempplot.plot(caplst3, templst3, color="black", label="Temperature", linewidth="2")

plt.title("I = "+ str(round(-data['current'][500], 1)) + "A")
vplot.set_xlabel("Capacity (Ah)")
vplot.set_ylabel("Voltage (V)")
tempplot.set_ylabel("Temperature (C)")
vplot.legend(loc="lower right")

NormNoPCC = {}
NormNoPCC['voltage'] = vlst
NormNoPCC['current'] = curlst
NormNoPCC['capacity'] = caplst
NormNoPCC['temp'] = templst

NormPCC = {}
NormPCC['voltage'] = vlst2
NormPCC['current'] = curlst2
NormPCC['vcapacity'] = vcaplst2
NormPCC['capacity'] = caplst2
NormPCC['temp'] = templst2

VacNoPCC = {}
VacNoPCC['voltage'] = vlst1
VacNoPCC['capacity'] = caplst1
VacNoPCC['temp'] = templst1

VacPCC = {}
VacPCC['voltage'] = vlst3
VacPCC['current'] = curlst3
VacPCC['vcapacity'] = vcaplst3
VacPCC['capacity'] = caplst3
VacPCC['temp'] = templst3

pickle.dump(NormNoPCC, open('./data/3C_PNormal_NoPCC.pickle', 'wb'))
pickle.dump(NormPCC, open('./data/3C_PNormal_PCC.pickle', 'wb'))
pickle.dump(VacNoPCC, open('./data/3C_PVacuum_NoPCC.pickle', 'wb'))
pickle.dump(VacPCC, open('./data/3C_PVacuum_PCC.pickle', 'wb'))

# tempplot.legend(loc="lower left")
vplot.set_xlim(0, 3)
vplot.set_ylim(2, 4.5)
tempplot.set_ylim(20, 70)
plt.ioff()
plt.show()
