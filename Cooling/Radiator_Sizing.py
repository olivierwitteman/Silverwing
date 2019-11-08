import numpy as np
from scipy import constants as c


def pressure_drop(mu, l, vdot, rho=0, d=0, lam=True):
    if lam:
        dp = 128.*mu*l*vdot/np.pi

    else:
        dp = 0.241*l*rho**(3/4.)*mu**(1/4.)*d**(-4.75)*vdot**1.75
    return dp


def q_convection(A, T, Tamb, h):
    q_conv = h*A*(T-Tamb)
    return q_conv


def q_radiation(A, T, Tamb, sigma=c.Boltzmann):
    q_rad = sigma*A*(T**4 - Tamb**4)
    return q_rad


def q_conductivity():
    pass

def q_ext(A, T, Tamb, h):
    q = q_convection(A, T, Tamb, h) + q_radiation(A, T, Tamb)
    return q


def sanity_check(A_ref, m_ref_dot):
    q = 1.
    dT = 1.
    q_r = 1.
    dT_r = 1.
    alpha = np.sqrt((q/dT)/(q_r/dT_r))

    mdot = alpha * m_ref_dot
    A = alpha * A_ref


print(pressure_drop(0, 0, 0))
