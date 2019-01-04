import numpy as np


# Adjustable inputs
T = 288.15              # ambient temperature [K]
V_inf = 40.             # aircraft airspeed [m/s]
tip_mach = 0.8          # propeller tip mach number
ac_aoa = 10.            # aircraft angle of attack [deg]
Thrust = 1600.          # propeller thrust [N]
D_prop = 1.2            # propeller diameter [m]
x_b = 0.75              # propeller spanwise location of resultant force


# Calculated inputs
a = np.sqrt(1.4*287.15*T)   # speed of sound [m/s]
tip_speed = tip_mach * a    # propeller tip speed [m/s]


V_75b = 0.75 * tip_speed


V_rel_ref = np.sqrt(V_inf**2 + V_75b**2)