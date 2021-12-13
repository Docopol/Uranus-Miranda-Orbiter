g = 9.80665
m = 18119.35
a_y = g*6.0
a_x = a_z = g*2.0

# On top of Tank:

Px = a_x * m
Py = a_y * m
Pz = a_z * m


def reaction_forces(h):
    Rx = Px
    Ry = Py
    Rz = Pz
    Mx = Pz * h
    My = 0
    Mz = Px * h
    return Rx, Ry, Rz, Mx, My, Mz

