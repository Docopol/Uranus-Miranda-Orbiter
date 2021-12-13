import numpy as np
from Constants import *
import cmath
import matplotlib.pyplot as plt

SC_mat = Al7075T6
Tank_mat = Al7075T6
r = 1.8
d = r * 2
t = 2.01 * 1e-3
L_SC = 8.235
L_Tank = 2
A_SC = 2 * np.pi * 1.8 * 0.0005
A_Tank = 0.002
rho_SC = SC_mat.get_density()
rho_Tank = Tank_mat.get_density()
E_SC = SC_mat.get_E()
E_Tank = Tank_mat.get_E()
m_SC = 2 * np.pi * (np.power(d, 2) / 4 + d / 2 * L_SC) * t * rho_SC
m_Tank = 100


def frequency(E, M, A, L):
    k_y = E * A / L
    f_nat = np.sqrt(k_y / M) / (2 * np.pi)
    f_launcher = 25
    return f_nat, f_nat > f_launcher, k_y


def calc_omega(m_SC, m_Tank, k1, k2):
    m1 = m_SC
    m2 = m_Tank

    a = m1 * m2
    b = m1 * k2 + m2 * k1 + m2 * k2
    c = k1 * k2

    d = b ** 2 - 4 * a * c

    omega_sq1 = (-b + cmath.sqrt(d)) / (2 * a)
    omega_sq2 = (-b - cmath.sqrt(d)) / (2 * a)

    omega1 = cmath.sqrt(-omega_sq1) / (2 * np.pi)
    omega2 = cmath.sqrt(-omega_sq2) / (2 * np.pi)

    return [omega1.real, omega2.real]


print(f'Natural Frequency of S/C is {frequency(E_SC, m_SC, A_SC, L_SC)[0]}')
print(f'Natural Frequency of Tank is {frequency(E_Tank, m_Tank, A_Tank, L_Tank)[0]}')

print(f'Natural Frequency of total system {calc_omega(m_SC, m_Tank, k1, k2)[0]}')

fn = calc_omega(m_SC, m_Tank, k1, k2)[0]


def displacement(fn, ff):
    x_0 = 0
    v_0 = 0
    a_0 = 0.9 * 9.81

    om_n = fn * 2 * np.pi
    om_f = ff * 2 * np.pi

    t = np.arange(-1, np.pi, 0.00001)

    def function(t):
        d_h = (-om_f / om_n) * (a_0 / ((om_n ** 2) - (om_f ** 2))) * np.sin(om_n * t)
        d_p = (a_0 / (om_n ** 2 - om_f ** 2)) * np.sin(om_f * t)
        d = d_h + d_p
        return 10000 * d

    plt.title("Displacement vs Time")
    plt.plot(t, function(t))
    plt.xlabel("Time")
    plt.ylabel("Displacement x $\mathregular{10^4}$")
    plt.xlim(0, 0.2)
    plt.tight_layout()
    plt.savefig('plot.svg', format='svg')
    plt.show()


def particular_vs_freq(fn):
    a_0 = 0.9 * 9.81

    om_n = fn * 2 * np.pi
    f_f = np.arange(0, 100, 0.1)
    om_f = f_f * 2 * np.pi

    d_p = 2 * (a_0 / abs((om_n ** 2 - om_f ** 2))) * 1000

    plt.title("Amplitude of Particular Solution vs Forcing Frequency")
    plt.plot(f_f, d_p)
    plt.ylim(0, 2)
    plt.xlabel("Forcing Frequency")
    plt.ylabel("Amplitude of Particular Solution x $\mathregular{10^3}$")
    plt.tight_layout()
    plt.savefig('plot2.svg', format='svg')
    plt.show()


def test():
    a_0 = 0.9 * 9.81
    om_n = fn * 2 * np.pi
    om_f = 100 * 2 * np.pi
    t = 0
    d_h = (-om_f) * (a_0 / ((om_n ** 2) - (om_f ** 2))) * np.cos(om_n * t)
    d_p = om_f * (a_0 / (om_n ** 2 - om_f ** 2)) * np.cos(om_f * t)
    print(d_h, d_p)
    print(d_h + d_p)


k1 = frequency(E_SC, m_SC, A_SC, L_SC)[2]
k2 = frequency(E_Tank, m_Tank, A_Tank, L_Tank)[2]


print(f'Natural Frequency of S/C is {frequency(E_SC, m_SC, A_SC, L_SC)[0]}')
print(f'Natural Frequency of Tank is {frequency(E_Tank, m_Tank, A_Tank, L_Tank)[0]}')
print(f'Natural Frequency of total system {calc_omega(m_SC, m_Tank, k1, k2)}')

fn = calc_omega(m_SC, m_Tank, k1, k2)[0]


displacement(fn, 100)
#particular_vs_freq(fn)
# test()
