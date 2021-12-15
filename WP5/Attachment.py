# from materials import material_dict
from K_func import *
import Forces_FBD as f
# from Constants import bolt_D_standarts
# import math
import numpy as np

h = float(input("Height: "))
R = float(input("Radius: "))
fx, fy, fz, mx, my, mz = f.reaction_forces(h)
print(fx, fy, fz)


def force_per_bolt(n_bolts):
    cos_sum = 0
    sin_sum = 0
    thetarange = np.linspace(-np.pi/2, np.pi/2, n_bolts)
    for theta in thetarange:
        cos_sum += m.cos(theta)
        sin_sum += m.sin(theta)
    distr_sum = cos_sum + sin_sum

    fxb = fx/(2*distr_sum)
    fzb = fz/(2*distr_sum)
    fxb_max = m.sqrt(2)*fxb
    fzb_max = m.sqrt(2)*fzb
    fyb = fyb_max = fy/n_bolts + (mx/sin_sum + mz/cos_sum)/(2 * R)
    return fxb_max, fyb_max, fzb_max

print(force_per_bolt(100))
def mass_structural_plate(material, R, W, t, n_bolts, D_bolts):
    A = 2*np.pi*R*W - n_bolts*np.pi * D_bolts**2
    return material.d*A*t


def bearing(F, D_bolt, t_plate):
    sigma = F/(D_bolt*t_plate)
    return sigma


def pull_through(F, t_plate):
    sigma = ...
    tau = ...
    Y = m.sqrt(sigma**2 + 3*tau**2)
    return Y

# def lmax(sigma, w, t, sep):
#     safety_factor = 1.5
#     l1 = w*t**2 / (6*fx) * (sigma/safety_factor - 6*my*(sep/2 + t)/(w*t**3 + 3*w*t*(sep+t)))
#     l2 = sigma/safety_factor * t * w**2 / (6*fy)
#     return min([l1, l2])
#
#
# def dmin(t, sigma, kty, kbry):
#     safety_factor = 1.5
#     d1 = fy / (t * sigma/safety_factor * kty)
#     d2 = fz / (t * sigma/safety_factor * kbry)
#     return max([d1, d2])
#
#
# n = 41  # Steps in the iteration
# trange = np.linspace(10/1000, 0.5/1000, n)
# wrange = np.linspace(100/1000, 8/1000, n)
# drange = np.linspace(80/1000, 5/1000, n)
# lrange = np.linspace(100/1000, 20/1000, n)
# # srange = np.linspace(50, 10, n)
#
# # nrange = np.array([40, 32, 24, 16, 8])
# mat = material_dict['Al2014T6']
# separation = 20/1000
#
# # Volume can be calculated as t(wl + (pi/8)(w^2-d^2))
# w1, l1 = np.meshgrid(wrange, lrange)
# d1 = np.meshgrid(wrange, drange)[1]
#
# w1 = w1.transpose()
# l1 = l1.transpose()
# d1 = d1.transpose()
#
# wl = w1*l1
# wd = (np.pi/8)*(w1**2 - d1**2)
# t_arr = np.tile(trange, (len(trange), 1))
#
# # Decompose the arrays into arrays of the same size made out of its columns
# t_array = np.tile(t_arr[:, 0], (len(trange), 1))
# wld = np.tile(wl[:, 0], (n, 1))
# wld += wd
# for i in range(len(wl)-1):
#     z = i + 1
#     x = np.tile(wl[:, z], (len(wld), 1))
#     wld = np.hstack((wld, x.transpose() + wd))
#     x = np.tile(t_arr[:, z], (len(trange), 1))
#     t_array = np.hstack((t_array, x))
#
#
# t_array = np.tile(t_array, (n, 1)).transpose()
# wld = np.tile(wld, (n, 1))
# volumes = t_array * wld
#
# # Physical constraints
# volumes = np.where(volumes <= 0, 0, volumes)
# m = 0
# for i in range(len(volumes)):
#     if m == n:
#         m = 0
#     w_value = wrange[m]
#     greater_d = np.where(drange>w_value)
#     smaller_l = np.where(lrange<w_value/2) * np.array([n])
#     for j in range(n):
#         sl = smaller_l + j
#         volumes[i, sl] = 0
#         volumes[i, greater_d] = 0
#         greater_d += np.array([n])
#     m += 1
#
# # Check for failure
# m = 0
# for i in range(len(volumes)):
#     if m == n:
#         m = 0
#
#     w_value = wrange[m]
#     t_value = trange[int(str(i/n).split('.')[0])]
#     l_max = lmax(mat['t_yield_stress'], w_value, t_value, separation)
#     greater_l = np.where(lrange > l_max) * np.array([n])
#     for j in range(n):
#         gl = greater_l + j
#         volumes[i, greater_l] = 0
#
#         k_t = K_t(mat['name'], w_value, drange[j])
#         d_max = w_value - fz / (t_value * mat['t_yield_stress'] * k_t)
#
#         k_ty = K_ty(t_value, w_value, drange[j])
#         k_bry = K_bry(t_value, w_value, drange[j])
#         d_min = dmin(t_value, mat['t_yield_stress'], k_ty, k_bry)
#
#         if drange[j] < d_min or drange[j] > d_max:
#             volumes[i, j] = 0
#
#     m += 1
#
# mass = mat['density'] * volumes
# for i in range(len(mass)):
#     mass[i, np.where(mass[i] == 0)] = 100000
#
# min_mass = np.min(mass)
# row, column = np.where(mass == min_mass)
#
# w_opt = wrange[n - (row - n*int(str(row/n).split('.')[0][1:]))]
# t_opt = trange[int(str(row/n).split('.')[0][1:])]
#
# d_opt = drange[n - (column - n*int(str(column/n).split('.')[0][1:]))]
# l_opt = lrange[int(str(column/n).split('.')[0][1:])]
#
# print('mass: {} g,'.format(1000*min_mass), '(w, t, d, l):{}'.format((w_opt, t_opt, d_opt, l_opt)))
