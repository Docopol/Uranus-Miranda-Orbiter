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
thickness = 0.5
mission_time = 20
K = 0.7
v = 20


R=np.array([0.1015961057287725,0.4047537964306023,0.7112808385838605,1.001734835407617,1.519184634934273,2.028630972796837,3.0583691965274244,4.058015639708228,5.274106052409366,5.989825196382176])
F_r=np.array([3.3371149266726937e-10,1.4256083893648263e-10,1.225871302123046e-10,1.320847113555509e-10,1.810215647316382e-10,3.7207477446029754e-10,1.5142608630917805e-9,4.948367979701734e-9,7.521019073810325e-9,5.014810662418809e-9])
# 0.1015961057287725, 3.3371149266726937e-10
# 0.4047537964306023, 1.4256083893648263e-10
# 0.7112808385838605, 1.225871302123046e-10
# 1.001734835407617, 1.320847113555509e-10  EARTH
# 1.519184634934273, 1.810215647316382e-10
# 2.028630972796837, 3.7207477446029754e-10
# 3.0583691965274244, 1.5142608630917805e-9
# 4.058015639708228, 4.948367979701734e-9
# 5.274106052409366, 7.521019073810325e-9
# 5.989825196382176, 5.014810662418809e-9
#dist_corr = np.mean(F_r,R)/F_r[3]
dist_corr = np.trapz(F_r,R)/(R[len(R)-1]-R[0])/F_r[3]
max_F = max(F_r)/F_r[3]

def F1(m):
    return k * np.power(k1 * np.power(m, p1) + k2, p2)


def F2(m):
    return k * k3 * np.power(m + k4 * np.power(m, p3) + k5 * np.power(m, p4), p5)


def F3(m):
    return k * k6 * np.power(m + k7 * np.power(m, p3), p6)
def Flux(m):
    return F1(m) + F2(m) + F3(m)

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
    return (dist_corr*N * A * mission_time)

def NofPen_corr(thickness):
    idx = np.searchsorted(t, thickness)
    print(m[idx])
    m_lim = m[idx]
    N = Flux(m_lim)
    return (dist_corr*N * A * mission_time)



#print("test ", NofPen(np.array([0.5])))

thickness_range = np.linspace(0.05, 100, 1000).astype(float)
NP = NofPen(thickness_range)

# N_tot = np.trapz(N_fail)
print("# of particles that will penetrate fuel tank during mission: ", NofPen_corr(np.array([thickness])))

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
#print(NofPen([0.5]))
# plt.axhline(y=thickness, color='r', linestyle='-')

# show the plot
plt.show()



