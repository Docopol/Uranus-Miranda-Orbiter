import math
import numpy as np


def cross_section(t, l):
    A = l**2 - (l-2*t)**2
    I = (1/12) * (l**4 - (l-2*t)**4)
    return A, I


def stress(t, l):
    A, I = cross_section(t, l)

    F_net = math.sqrt(2)*m*g
    F_t = F_net / 2 * 3*I / (3*I + A*L*(L+R))
    F_l = F_net/2 - F_t
    F_y = 0.75*m*g

    M_x = F_y*L
    M_y = F_t*L

    sigma_1 = (M_x + M_y) * (l/2) / I
    sigma_2 = M_x * (l/2) / I + F_l/A
    shear = F_y/I * 3*l**2/8
    return [sigma_1 / 10**6, sigma_2 / 10**6], shear / 10**6


safety_factor = 1.5
sigma_max = 480 / safety_factor
tau_max = 331 / safety_factor

trange = np.linspace(0.0005, 0.02, 15)
lrange = np.linspace(0.005, 0.2, 15)

A = 10000
R = 1.4478
L = 1.8-R
m = 18639.82476
g = 9.80665
for length in lrange:
    for thick in trange:
        if thick > 0.1*length:
            continue
        elif max(stress(thick, length)[0]) < sigma_max and stress(thick, length)[1] < tau_max:
            if length**2 - (length-2*thick)**2 < A:
                A = 4*thick*length
                opt_config = (thick, length)

print(f'thickness, length = {opt_config} m, maximum stress = {stress(opt_config[0], opt_config[1])[0]} MPa, '
      f'mass = {cross_section(opt_config[0], opt_config[1])[0] * 2810 * 0.386} kg')
print(f'Max shear stress = {stress(opt_config[0], opt_config[1])[1]} MPa')
