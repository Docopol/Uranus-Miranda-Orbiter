import math
import numpy as np


def cross_section(t, l):
    A = l**2 - (l-2*t)**2
    I = (1/12) * (l**4 - (l-2*t)**4)
    return A, I


def stress(t, l):
    A, I = cross_section(t, l)
    return (math.sqrt(2)*l*L/(2*I)) * (3*I / (2*(3*I + A*L*(L+R))) + 0.75) * m*g


safety_factor = 1.5
sigma_max = 480*10**6 / safety_factor

trange = np.linspace(0.005, 0.05, 50)
lrange = np.linspace(0.04, 0.2, 50)

A = 10000
L = 0.386
R = 1.414
m = 18119.35
g = 9.81

for length in lrange:
    for thick in trange:
        if thick > 0.1*length:
            continue
        elif stress(thick, length) < sigma_max:
            if 4*thick*length < A:
                A = 4*thick*length
                opt_config = (thick, length)

print(f'thickness, length = {opt_config}, maximum stress = {stress(opt_config[0], opt_config[1])}, '
      f'mass = {cross_section(opt_config[0], opt_config[1])[0] * 2810 * 0.386} ')

# Bolts
bolt_D_standarts = [(1.6, 3.02), (2, 3.82), (2.5, 4.82), (3, 5.32), (3.5, 5.82), (4, 6.78), (5, 7.78), (6, 9.78),
                    (8, 12.73), (10, 15.73), (12, 17.73), (14, 20.67), (16, 23.67), (20, 29.16), (24, 35), (30, 45)]

A, I = cross_section(opt_config[0], opt_config[1])

bolt_list = list()
for bolt in bolt_D_standarts:
    d_in = bolt[0]
    d_out = bolt[1]

    P = sigma_max * math.pi / 4 * ((d_out/1000)**2 - (d_in/1000)**2)
    F_t = (m*g / math.sqrt(2)) * 3 * I / (3*I + A*L*(L+R))
    F_y = 0.75 * m * g

    n = P / math.sqrt(F_t**2 + F_y**2)
    t = P / (n * 0.6 * sigma_max * d_in)
    bolt_list.append((n, t))

print(bolt_list)
