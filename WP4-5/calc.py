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


# PER LUG
# TOP:
f_x_top = 1/2 * wx
f_y_top = wy
f_z_top = 1/2 * wz - wy * r_tot/h_rtg

M_y_top = 1/2 * wx * r_tot

# BOTTOM:
f_x_bot = 1/2 * wx
f_y_bot = wy
f_z_bot = 1/2 * wz + wy * r_tot/h_rtg

M_y_bot = 1/2 * wx * r_tot

print(f'Top: Fx={f_x_top}, Fy={f_y_top}, Fz={f_z_top}, My={M_y_top}')
print(f'Bot: Fx={f_x_bot}, Fy={f_y_bot}, Fz={f_z_bot}, My={M_y_bot}')
