import math
import matplotlib.pyplot as plt
import scipy as sc


def temperature(d):  # only if 278K < T < 288
    I = I_sun / d ** 2
    Q_in_sun = I * Ac * ap

    f0 = (asc * (Q_in_sun + a2)*Q_g/(1-a2*asc) + Q_g) / (escc)
    f = sc.poly1d([0.0108, -2.9408, 0, 0, 0, -f0])
    T = sc.roots(f)
    t = float(str(T[0]).split('+')[0][1:])  # gets the first solution
    return t


Ap = 119.1
Asc = Ap
Ac = 32.9

a1 = 0.05
a2 = a1
asc = 0.09

I_sun = 30459109.914585304
AU = 1.5 * 10**11
d = 108

Q_g = 3250
stph = 5.67 * 10 ** (-8)
I = I_sun / d ** 2





