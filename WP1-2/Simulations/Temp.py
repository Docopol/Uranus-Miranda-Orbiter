import math
import matplotlib.pyplot as plt
import scipy as sc


def temperature(d):  # only if 278K < T < 288
    I = I_sun / d ** 2
    f0 = (a * A1 * I + Q_g) / (A2 * stph)
    f = sc.poly1d([0.0108, -2.9408, 0, 0, 0, -f0])
    T = sc.roots(f)
    t = float(str(T[0]).split('+')[0][1:])  # gets the first solution
    return t


def T_close(d, af):
    I = I_sun / d ** 2
    ab = 0.1*af + 0.09*(1-af)
    em = 0.66*af + 0.17*(1-af)
    f0 = (ab * A1 * I + Q_g) / (em * A2 * stph)
    T = f0**0.25
    return T


I_sun = 30459109.914585304
d_U = 2872.463
AU = 1.5 * 10**11
d = 108

a = 0.09
A1 = 32.9
A2 = 119.1
Q_g = 400 + 3700 * 1.15
stph = 5.67 * 10 ** (-8)
I = I_sun / d ** 2

t_list = list()
d_list = list()

while d * 10**9 / AU < 1:
    d += 1

    Q_g = 350 + 3700 * 1.15
    T = T_close(d, 0.085)
    if T>300:
        Q_g = 3000
        T = T_close(d, 0.085)

    t_list.append(T)
    d_list.append(d * 10**9 / AU)
print(T)

Q_g = 3700
while d < d_U:
    if 278 < T < 288:
        T = temperature(d)
    else:
        if 278 > T:
            e = 0.062
        else:
            e = 0.17

        I = I_sun / d ** 2
        T = ((a * A1 * I + Q_g) / (stph * A2 * e))**0.25

    t_list.append(T)
    d_list.append(d * 10**9 / AU)
    d += 1
print(T)

plt.plot(d_list, t_list)
plt.xlabel('Distance [AU]')
plt.ylabel('Temperature [K]')
plt.grid()
plt.show()
