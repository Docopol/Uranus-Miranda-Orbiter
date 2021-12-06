import numpy as np
from Constants import *
import cmath

SC_mat = Al7075T6
Tank_mat = Al7075T6
r = 1.8
d = r * 2
t = 2.01 * 1e-3
L_SC = 8.235
L_Tank = 2
A_SC = 2 * np.pi * 1.8 * 0.0005
A_Tank = 0.002

rho_SC = SC_mat.get_density()
rho_Tank = Tank_mat.get_density()
E_SC = SC_mat.get_E()
E_Tank = Tank_mat.get_E()
m_SC = 2 * np.pi * (np.power(d, 2) / 4 + d / 2 * L_SC) * t * rho_SC
m_Tank = 100


def frequency(E, M, A, L):
    k_y = E * A / L  # Longitudinal direction

    f_nat = np.sqrt(k_y / M) / (2 * np.pi)
    f_launcher = 25

    return f_nat, f_nat > f_launcher, k_y


print(f'Natural Frequency of S/C is {frequency(E_SC, m_SC, A_SC, L_SC)}')
print(f'Natural Frequency of Tank is {frequency(E_Tank, m_Tank, A_Tank, L_Tank)}')

k1 = frequency(E_SC, m_SC, A_SC, L_SC)[2]
k2 = frequency(E_Tank, m_Tank, A_Tank, L_Tank)[2]

"""
M = np.matrix([[m_SC, 0], [0, m_Tank]])
K = np.matrix([[k_1 + k_2, -k_2], [-k_2, k_2]])
"""
m1 = m_SC
m2 = m_Tank

a = m1 * m2
b = m1 * k2 + m2 * k1 + m2 * k2
c = k1 * k2

d = b ** 2 - 4 * a * c

omega_sq1 = (-b + cmath.sqrt(d))/(2*a)
omega_sq2 = (-b - cmath.sqrt(d))/(2*a)

omega1 = cmath.sqrt(-omega_sq1)/(2*np.pi)
omega2 = cmath.sqrt(-omega_sq2)/(2*np.pi)

print(omega1, omega2)