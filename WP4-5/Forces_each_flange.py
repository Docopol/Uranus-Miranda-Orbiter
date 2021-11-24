# assuming 2 flanges

g = 9.80665
m = 36.0
a_y = g*6.0
a_x = a_z = g*2.0

# Of ASRG:
l_rtg = 780
h_rtg = 460
w_rtg = 390

wx = a_x * m
wy = a_y * m
wz = a_z * m


# PER FLANGE
f_tot_x = 1/4 * wx
f_tot_y = 1/2 * wy
f_tot_z = 1/4 * wz + 1/2 * wy * l_rtg/h_rtg

M_tot_x = wz * h_rtg/2
M_tot_y = wx * l_rtg/2
M_tot_z = wx * h_rtg/2

print(f_tot_x)
print(f_tot_y)
print(f_tot_z)