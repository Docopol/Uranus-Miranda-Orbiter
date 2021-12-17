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

#radius correction
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

#closest value of an array
def closest_value_idx(array, value):
    idx = []
    for val in value:
        abs_diff = np.abs(array - value)
        idx.append(abs_diff.argmin())
    return idx


#Flux
def F1(m):
    return k * np.power(k1 * np.power(m, p1) + k2, p2)
def F2(m):
    return k * k3 * np.power(m + k4 * np.power(m, p3) + k5 * np.power(m, p4), p5)
def F3(m):
    return k * k6 * np.power(m + k7 * np.power(m, p3), p6)
def Flux(m):
    return F1(m) + F2(m) + F3(m)

F = F1(m) + F2(m) + F3(m)
F = F.astype(float)


#Density and thickness
rho = np.piecewise(m, [m < 10 ** -12, np.logical_and(10 ** -12 <= m, m < 10 ** -6), m >= 10 ** -6], [2, 1, 0.5])
t = K * np.power(m, 0.352) * np.power(v, 0.875) * np.power(rho, 0.167)


#Number of penetrations single plate
def NofPen(thickness):
    idx = np.searchsorted(t, thickness)
    m_lim = m[idx]
    m_lim = np.asarray(m_lim, dtype=object)
    N = Flux(m_lim)
    return (dist_corr*N * A * mission_time)


#Douple penetration stuff
d = np.cbrt(6*m/rho/np.pi)
rho_al = 2.8
coef = 1.44
def NofPen_DP(thickness, gap):
    #correction due to inability to use SI for some people
    thickness = thickness * 10
    gap = gap * 10
    #actual stuff
    M = rho_al*thickness
    L = 0.401
    m_crit = coef * L * M * gap**2 / v
    idx = closest_value_idx(m, m_crit)#idx = np.searchsorted(m, m_crit)
    if M/rho[idx]/(d[idx]*10) < 1:
        m_crit = np.power( (coef * np.power(np.pi/6,1/3) * L * M * M * np.power(gap,2)) / (np.power(rho[idx],2/3) * v) , 3/4)
    N = Flux(m_crit)
    return (dist_corr*N * A * mission_time)
    

# def t_DP(gap):
#     gap = gap/10
#     return np.power( (d * np.power(rho,1/3) * np.power(rho_al,1/9) * np.power(v, 2/3)) / (coef * np.power(gap,1/3)) , 3/2)*10

# def NofPen_DP(thickness, gap):
#     idx = np.searchsorted(t_DP(gap), thickness)
#     m_lim = m[idx]
#     m_lim = np.asarray(m_lim, dtype=object)
#     N = Flux(m_lim)
#     return (dist_corr*N * A * mission_time)


#Here starts plotting
thickness_range = np.linspace(0.5, 5, 1000).astype(float)
NP = NofPen(thickness_range)

# N_tot = np.trapz(N_fail)
print("# of particles that will penetrate the wall during mission: ", NofPen_DP(0.25,2))

x = np.log10(m)
y = np.log10(F)

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
plt.grid(True)
# plot the function
plt.plot(thickness_range, NofPen(thickness_range), 'k')
plt.plot(thickness_range, NofPen_DP(thickness_range/2,20), 'r')
plt.plot(thickness_range, NofPen_DP(thickness_range/2,40), 'b')
#print(NofPen([0.5]))
# plt.axhline(y=thickness, color='r', linestyle='-')

# show the plot
plt.show()



