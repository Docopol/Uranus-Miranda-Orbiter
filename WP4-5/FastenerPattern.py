import math 

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002

n = 4 #number of bolts

E = 200 * 10**9 #Youngs modulus for steel

M_x_plate = F_y * 0.02

w = 200
h = 150 

F_z_max = F_z + M_y/w*2 + M_x_plate/h*2


sigma_yield = 250 * 10**6 #Yield strength steel

A_tot = F_z / sigma_yield

A = A_tot / n

D = math.sqrt(4*A/math.pi)




print("Bolt Area ", A)
print("Bolt D    ", D)