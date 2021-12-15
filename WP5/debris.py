import matplotlib.pyplot as plt
import math
import numpy as np

# All this based on grun IFM
m = np.logspace(-18, 1, 10000).astype(float)
# coefficients
k = 3.15576 * 10 ** 7
k1 = 2.2 * 10 ** 3
k2 = 15
k3 = 1.3 * 10 ** -9
k4 = 10 ** 11
k5 = 10 ** 27
k6 = 1.3 * 10 ** -16
k7 = 10 ** 6

# powers
p1 = 0.306
p2 = -4.38
p3 = 2
p4 = 4
p5 = -0.36
p6 = -0.85

# other stuff
A = 119.1
thickness = 2
mission_time = 20
K = 0.7
v = 20


# t_double =

def F1(m):
    return k * np.power(k1 * np.power(m, p1) + k2, p2)


def F2(m):
    return k * k3 * np.power(m + k4 * np.power(m, p3) + k5 * np.power(m, p4), p5)


def F3(m):
    return k * k6 * np.power(m + k7 * np.power(m, p3), p6)


x = np.log10(m)

F = F1(m) + F2(m) + F3(m)
F = F.astype(float)
y = np.log10(F)

rho = np.piecewise(m, [m < 10 ** -12, np.logical_and(10 ** -12 <= m, m < 10 ** -6), m >= 10 ** -6], [2, 1, 0.5])
t = K * np.power(m, 0.352) * np.power(v, 0.875) * np.power(rho, 0.167)

t_fail = np.piecewise(t, [t < thickness, t > thickness], [0, 1])

F_fail = F * t_fail
N_fail = F_fail * A * mission_time


def NofPen(thickness):
    idx = np.searchsorted(t, thickness)
    F_f = []
    for i in idx:
        F_f.append(F[i:])
    F_f = np.asarray(F_f, dtype=object)
    m_lim = []
    for i in idx:
        m_lim.append(m[i:])
    m_lim = np.asarray(m_lim, dtype=object)

    N = []
    for j in range(len(F_f)):
        N.append(np.trapz(F_f[j], m_lim[j]))
    N = np.asarray(N)
    return (N * A * mission_time)

print("test ", NofPen(np.array([0.5])))

thickness_range = np.linspace(0.05, 100, 1000).astype(float)
NP = NofPen(thickness_range)

# N_tot = np.trapz(N_fail)
print("# of particles that will penetrate fuel tank during mission: ", NofPen(np.array([thickness])))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.tick_params(axis="x", direction="inout")
ax.tick_params(axis="y", direction="inout")
ax.tick_params(bottom=True, top=True, left=True, right=True)
# ax.spines['right'].set_position('zero')
# #ax.spines['bottom'].set_position(('bottom'))
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
plt.xlabel("t, mm")
plt.ylabel("# of penetrations")
# plot the function
plt.plot(thickness_range, NP, 'k')
print(NofPen(np.array([10])))
# plt.axhline(y=thickness, color='r', linestyle='-')

# show the plot
plt.show()
