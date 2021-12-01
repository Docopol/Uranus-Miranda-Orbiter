import numpy as np
from materials import material_dict
import time

t1 = time.time()
fx, fy, fz, my = 353.0394, 1059.1182, 1105.570752631579, 0


def K_t(matn, w, d):
    x = w/d
    c1 = 0.0006 * x ** 6 - 0.0099 * x ** 5 + 0.0636 * x ** 4 - 0.1779 * x ** 3 + 0.1932 * x ** 2 - 0.0412 * x + 0.9727
    c2 = -0.0045 * x ** 5 + 0.0414 * x ** 4 - 0.129 * x ** 3 + 0.1296 * x ** 2 + 0.0066 * x + 0.9568
    c3 = -0.002 * x ** 4 + 0.0217 * x ** 3 - 0.0805 * x ** 2 + 0.0519 * x + 1.02
    c4 = -0.0036 * x ** 4 + 0.044 * x ** 3 - 0.1763 * x ** 2 + 0.1694 * x + 0.981
    c5 = 0.001 * x ** 5 - 0.0134 * x ** 4 + 0.0653 * x ** 3 - 0.1165 * x ** 2 - 0.1143 * x + 1.197
    c6 = -0.083 * x + 0.7549
    c7 = 0.0059 * x ** 5 - 0.0862 * x ** 4 + 0.4716 * x ** 3 - 1.172 * x ** 2 + 1.0229 * x + 0.7781
    if matn == 'Al2014-T6':
        k = (c1 + c2 + c4 + c5) / 4
    elif matn == 'Al7075-T6' or matn == 'Al6061-T6':
        k = (c1 + c2 + c4) / 3
    elif matn == 'Al2024-T4':
        k = (c3 + c4) / 2
    elif matn == 'Al2024-T3':
        k = c4
    elif matn == 'St4130' or matn == 'St8630' or matn == 'St-A992':
        k = c1
    elif matn == 'MgAZ91C-T6' or matn == 'Mg-Am60':
        k = c7
    else:
        k = (c1 + c2 + c3 + c4 + c5 + c6 + c7) / 7

    ms = 0.15  # Margin of safety
    k += ms
    return k


def K_ty(t, w, d):
    A1 = t * (w - d * np.sqrt(1 / 2)) / 2
    A2 = t * (w - d) / 2
    A_av = 6 / (4 / A1 + 2 / A2)
    A_br = t * d
    x = A_av / A_br
    c3 = 0.0718 * x ** 3 - 0.5166 * x ** 2 + 1.5215 * x - 0.0359

    k = c3
    ms = 0.15
    k += ms
    return k


def K_bry(t, w, d):
    r = t / d

    if r <= 0.06:
        r = 0.06
    elif 0.06 < r < 0.135:
        r = round(r / 2 * 100) * 2 / 100
    elif 0.135 <= r < 0.25:
        r = round(r / 5 * 100) * 5 / 100
    elif 0.25 <= r < 0.5:
        r = round(r * 10) / 10
    else:
        r = 0.6

    x = w / (2 * d)

    if r == 0.06:
        k = -0.00235 * x ** 6 + 0.3448 * x ** 5 - 2.0373 * x ** 4 + 6.2116 * x ** 3 - 10.396 * x ** 2 + 9.3121 * x - 2.7106
    elif r == 0.08:
        k = -0.0196 * x ** 6 + 0.2937 * x ** 5 - 1.7831 * x ** 4 + 5.6263 * x ** 3 - 9.845 * x ** 2 + 9.3348 * x - 2.8232
    elif r == 0.1:
        k = -0.0081 * x ** 6 + 0.1355 * x ** 5 - 0.9318 * x ** 4 + 3.3725 * x ** 3 - 6.8401 * x ** 2 + 7.5535 * x - 2.4513
    elif r == 0.12:
        k = -0.005 * x ** 6 + 0.0901 * x ** 5 - 0.6644 * x ** 4 + 2.5808 * x ** 3 - 5.6329 * x ** 2 + 6.7237 * x - 2.2501
    elif r == 0.15:
        k = 0.0032 * x ** 6 - 0.0281 * x ** 5 + 0.0106 * x ** 4 + 0.6622 * x ** 3 - 2.8503 * x ** 2 + 4.8915 * x - 1.8208
    elif r == 0.2:
        k = 0.0068 * x ** 6 - 0.087 * x ** 5 + 0.3885 * x ** 4 - 0.5524 * x ** 3 - 0.8532 * x ** 2 + 3.4179 * x - 1.441
    elif r == 0.3:
        k = 0.004 * x ** 6 - 0.0555 * x ** 5 + 0.2734 * x ** 4 - 0.4473 * x ** 3 - 0.6323 * x ** 2 + 3.0505 * x - 1.3112
    elif r == 0.4:
        k = -0.0015 * x ** 6 + 0.0165 * x ** 5 - 0.088 * x ** 4 + 0.4184 * x ** 3 - 1.6331 * x ** 2 + 3.579 * x - 1.4127
    else:
        k = -0.0048 * x ** 6 + 0.0626 * x ** 5 - 0.343 * x ** 4 + 1.1103 * x ** 3 - 2.5736 * x ** 2 + 4.1826 * x - 1.5554

    if k < 0:
        k = 0.01

    return k


def lmax(sigma, w, t, sep):
    l1 = w*t**2 / (6*fx) * (sigma - 6*my*(sep/2 + t)/(w*t**3 + 3*w*t*(sep+t)))
    l2 = sigma * t * w**2 / (6*fy)
    return min([l1, l2])


def dmin(t, sigma, kty, kbry):
    d1 = fy / (t * sigma * kty)
    d2 = fz / (t * sigma * kbry)
    return max([d1, d2])


n = 50  # Steps in the iteration
trange = np.linspace(10/1000, 0.5/1000, n)
wrange = np.linspace(100/1000, 8/1000, n)
drange = np.linspace(80/1000, 5/1000, n)
lrange = np.linspace(100/1000, 20/1000, n)
# srange = np.linspace(50, 10, n)

# nrange = np.array([40, 32, 24, 16, 8])
mat = material_dict['Al2014T6']
separation = 500

# Volume can be calculated as t(wl + (pi/8)(w^2-d^2))
w1, l1 = np.meshgrid(wrange, lrange)
d1 = np.meshgrid(wrange, drange)[1]

wl = w1*l1
wd = (np.pi/8)*(w1**2 - d1**2)
t_arr = np.tile(trange, (len(trange), 1))

# Decompose the arrays into arrays of the same size made out of its columns
t_array = np.tile(t_arr[:, 0], (len(trange), 1))
wld = np.tile(wl[:, 0], (n, 1))
wld += wd
for i in range(len(wl)-1):
    z = i + 1
    x = np.tile(wl[:, z], (len(wld), 1))
    wld = np.hstack((wld, x.transpose() + wd))
    x = np.tile(t_arr[:, z], (len(trange), 1))
    t_array = np.hstack((t_array, x))


t_array = np.tile(t_array, (n, 1)).transpose()
wld = np.tile(wld, (n, 1))
volumes = t_array * wld

# Physical constraints
volumes = np.where(volumes <= 0, 0, volumes)
m = 0
for i in range(len(volumes)):
    if m == n:
        m = 0
    w_value = wrange[m]
    greater_d = np.where(drange>w_value)
    smaller_l = np.where(lrange<w_value/2) * np.array([n])
    for j in range(n):
        sl = smaller_l + j
        volumes[i, sl] = 0
        volumes[i, greater_d] = 0
        greater_d += np.array([n])
    m += 1

# Check for failure
m = 0
for i in range(len(volumes)):
    if m == n:
        m = 0

    w_value = wrange[m]
    t_value = trange[int(str(i/n).split('.')[0])]
    l_max = lmax(mat['t_yield_stress'], w_value, t_value, separation)
    greater_l = np.where(lrange > l_max) * np.array([n])
    for j in range(n):
        gl = greater_l + j
        volumes[i, greater_l] = 0

        k_t = K_t(mat['name'], w_value, drange[j])
        d_max = w_value - fz / (t_value * mat['t_yield_stress'] * k_t)

        k_ty = K_ty(t_value, w_value, drange[j])
        k_bry = K_bry(t_value, w_value, drange[j])
        d_min = dmin(t_value, mat['t_yield_stress'], k_ty, k_bry)

        if drange[j] < d_min or drange[j] > d_max:
            volumes[i, j] = 0

    m += 1

mass = mat['density'] * volumes
for i in range(len(mass)):
    mass[i, np.where(mass[i] == 0)] = 100000

min_mass = np.min(mass)
row, column = np.where(mass == min_mass)

w_opt = wrange[row - n*int(str(row/n).split('.')[0])]
t_opt = trange[int(str(row/n).split('.')[0])]

d_opt = drange[column - n*int(str(column/n).split('.')[0])]
l_opt = lrange[int(str(column/n).split('.')[0])]

print(min_mass, w_opt, t_opt, d_opt, l_opt, time.time()-t1)
