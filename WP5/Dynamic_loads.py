import numpy as np
from Constants import *

sc_mat = Al7075T6

def frequency_SC(E, M, A, I, L):
    k_y = E * A / L  # Longitudinal direction

    f_nat = np.sqrt(k_y / M) / (2 * np.pi)
    f_launcher = 30

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