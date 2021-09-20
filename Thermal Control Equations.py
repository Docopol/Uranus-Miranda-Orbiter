import math


def Q_out(T, A, e):
    stph = 5.67 * 10**(-8)
    return e * stph * A * T**4


def q_drag(V, d, r):
    return 1.83 * 10**(-4) * V**3 * math.sqrt(d/r)


def Q_in(I, A_sc, A_pl, a, albedo, h):
    return a * I * (A_sc + A_pl * albedo / h**2)



