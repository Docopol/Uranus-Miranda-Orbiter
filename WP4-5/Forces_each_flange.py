# assuming 2 flanges

g = 9.80665
m = 36.0
a_y = g*6.0
a_x = a_z = g*2.0

l_gap = 0.02 #ASSUMED distance between ASRG and S/C 20 mm

# Of ASRG:
l_rtg = 0.760
r_tot = l_rtg/2 + l_gap
h_rtg = 0.456
w_rtg = 0.390

wx = a_x * m
wy = a_y * m
wz = a_z * m


# PER FLANGE
f_tot_x = (1/2 * wx)
f_tot_y = 1/2 * (wy)
f_tot_z = 1/2 * (1/2 * wz + wy * r_tot/h_rtg)

M_tot_y = (1/2 * wx * r_tot)

print(f'Forces on 1 out of 2 Flanges: Fx={f_tot_x}, Fy={f_tot_y}, Fz={f_tot_z}, My={M_tot_y}')

