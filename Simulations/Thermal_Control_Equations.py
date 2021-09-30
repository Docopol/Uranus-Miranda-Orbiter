import math


def Q_out(T, A, e):
    stph = 5.67 * 10**(-8)
    return e * stph * A * T**4


def q_drag(d, r, h):
    GM = 5.794 * 10**6
    V = math.sqrt(GM / (h/1000))
    return 1.83 * 10**(-4) * V**3 * math.sqrt(d/r)


def radiating_area(h):
    R = 25362000
    return math.pi * (R**2 - (R**2/(R+h))**2)


def Q_in_eclipse(h, a):
    stph = 5.67 * 10**(-8)
    A_p = radiating_area(h)
    A_b = 32.9
    T = 58.1
    return a * A_b * A_p * stph * T**4 / h**2


def Q_sun(I, a, A):
    return I * A * a


def Q_in_sunlight(h, a):
    IR = Q_in_eclipse(h, a)
    alb = 0.3
    I = 3.69
    A_p = radiating_area(h)
    A_b = 32.9
    return IR + (a * A_b / h**2) * (I + I * A_p * alb)

