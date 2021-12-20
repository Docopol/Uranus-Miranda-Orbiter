g = 9.80665
m = 18119.35
a_y = g*6.0
a_x = a_z = g*2.0

# On top of Tank:

Px = a_x * m
Py = a_y * m
Pz = a_z * m


def reaction_moments(y):
    Rx = Px
    Ry = Py
    Rz = Pz
    Mx = Pz * y
    My = 0
    Mz = Px * y
    return Rx, Ry, Rz, Mx, My, Mz

print(reaction_moments(0))
#
#
# V = 13.98544
#
#
# import numpy as np
# coeff1 = [-2/3*np.pi, np.pi*8.235, 0, - V]
# print(np.roots(coeff1))
# coeff2 = [np.pi*1.8**2, -2/3*np.pi*1.8**3 - V]
# print(np.roots(coeff2))
