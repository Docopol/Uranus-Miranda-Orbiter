g = 9.80665
m = 36.0
P_y = 6.0
P_x = P_z = 2.0
l_ASRG_half = 0.380
l_gap = 0.02 #ASSUMED distance between ASRG and S/C 20 mm
#Assumed that lateral forces are in +z and +x directions (fasteners more likely to fail in tension)
h = 0.456

l=l_ASRG_half+l_gap

F_y = m*g*P_y
M_x = F_y*l

F_z = m*g*P_z

F_x = m*g*P_x

M_y = F_x*l

Force_upper_x = F_x / 2.0
Force_lower_x = Force_upper_x

Moment_upper_y = Moment_lower_y = M_y/2

Force_upper_z = F_z/2 + M_x / h * 2

Force_upper_y = Force_lower_y = F_y

print("Force in Y (both)   ",Force_upper_y)
print("Force in Z max      ", Force_upper_z)
print("Force in X          ", Force_upper_x)
print("Moment around y     ", Moment_upper_y)
