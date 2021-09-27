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


I_sun = 30459109.914585304
d_U = 2872.463
AU = 1.5 * 10**11
d = 108

a = 0.09
A1 = 32.9
A2 = 119.1
Q_g = 3250
stph = 5.67 * 10 ** (-8)
I = I_sun / d ** 2

first = True
T = temperature(d)
t_list = list()
d_list = list()
while d < d_U:
    d += 1

    if 278 < T < 288:
        T = temperature(d)
    else:
        if 278 > T:
            e = 0.062
        else:
            e = 0.17

        I = I_sun / d ** 2
        T = ((a * A1 * I + Q_g) / (A2 * stph * e)) ** 0.25

    if first:
        print(T)
        first = False
    t_list.append(T)
    d_list.append(d * 10**9 / AU)

print(T)
plt.plot(d_list, t_list)
plt.xlabel('Distance [AU]')
plt.ylabel('Temperature [K]')
plt.grid()
plt.show()
