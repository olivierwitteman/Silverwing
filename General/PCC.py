cp_batt = 0.83E3
cp_pcc = 1.9E3


m_cell = 46.6
m_pack = 84

m_pcc = 0

E = 1565.1E3

dT = E/(m_cell**cp_batt + m_pcc*cp_pcc)

print(dT)

