import numpy as np

a = 0.000244
b = 1.073
c = 1.744
offset = 268


Pset = float(input('Power setpoint (full vehicle) [kW]: '))


def P_loss(VDC, IoutRMS):
    p_dis = a*VDC**b * IoutRMS**c + offset
    p_t = VDC * IoutRMS
    n = 100*p_dis/p_t
    return p_dis, n


print('\nCombined losses for 2 inverters')
print('At P_vehicle = {!s} kW\n'.format(Pset))


for i in np.linspace(450, 670, 5):
    V = int(i)
    P_dis, eta_inv = P_loss(V, Pset*1e3/(2*V))
    print('At VDC = {!s} V; {!s} kW; {!s} %'.format(V, round(2*P_dis/1000, 2), round(eta_inv, 2)))
