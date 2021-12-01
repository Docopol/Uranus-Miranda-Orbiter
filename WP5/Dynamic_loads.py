import numpy as np
from Constants import *

sc_mat = Al7075T6

def frequency_SC(E, M, A, I, L):
    k_y = E * A / L  # Longitudinal direction

    f_nat = np.sqrt(k_y / M) / (2 * np.pi)
    f_launcher = 30

    return f_nat, f_nat > f_launcher

r = 1.8
d = r*2
t = 2.01 * 1e-3
L = 8.235
A = 2 * np.pi * 1.8 * 0.0005

rho = sc_mat.get_density()
E = sc_mat.get_E()
m_SC = 2*np.pi*(np.power(d , 2)/4 + d / 2 * L) * t * rho

print(frequency_SC(73.1e9, 18119.35, 2 * np.pi * 1.8 * 0.0005, np.pi * np.power(1.8, 3) * 0.0005, 8.235))
