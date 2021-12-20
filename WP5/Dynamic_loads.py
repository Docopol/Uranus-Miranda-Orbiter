import numpy as np
from Constants import *
import cmath
import matplotlib.pyplot as plt

SC_mat = Al7075T6
Tank_mat = Ti6Al4V
r_SC = 1.8
r_tank = 1.448
t_SC = 2.01 * 1e-3
t_tank = 0.0247
L_SC = 8.235
L_Tank = 0.193 + 2 * r_tank
A_SC = 2 * np.pi * 1.8 * t_SC
A_Tank = 2 * np.pi * r_tank * t_tank
rho_SC = SC_mat.get_density()
rho_Tank = Tank_mat.get_density()
E_SC = SC_mat.get_E()
E_Tank = Tank_mat.get_E()
m_SC = 1217.9
m_Tank = 741.48


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


def displacement(fn, ff):
    F_0 = 0.9 * 9.81
    a_0 = F_0

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
    plt.xlabel("Time [s]")
    plt.ylabel("Displacement x 10 [mm]")
    plt.xlim(0, 0.2)
    plt.tight_layout()
    plt.savefig('plot.svg', format='svg')
    plt.show()


def particular_vs_freq(fn):
    F_0 = 0.9 * 9.81
    a_0 = F_0

    om_n = fn * 2 * np.pi
    f_f = np.arange(0, 100, 0.1)
    om_f = f_f * 2 * np.pi

    d_p = 2 * (a_0 / abs((om_n ** 2 - om_f ** 2))) * 1000

    redlinex=[25,25]
    redliney=[0,10]

    fig,ax = plt.subplots()

    plt.title("Amplitude of Particular Solution vs Forcing Frequency")
    plt.plot(f_f, d_p, label="amplitude of solution")
    plt.plot(redlinex,redliney, color="red", label="25Hz")
    plt.ylim(0, 1)
    plt.xlabel("Forcing Frequency [Hz]")
    plt.ylabel("Amplitude of Particular Solution [mm]")
    ax.legend()
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
print(f'Natural Frequency of total system {calc_omega(m_SC, m_Tank, k1, k2)[0]}')


fn = calc_omega(m_SC, m_Tank, k1, k2)[0]


#displacement(fn, 100)
particular_vs_freq(fn)
