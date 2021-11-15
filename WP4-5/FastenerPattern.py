import math 

F_y = 2118.2364
F_z = 546.22255968
F_x = 353.0394
M_y = 141.21576000000002

n = 4 #number of bolts

E = 200 * 10**9 #Youngs modulus for steel

sigma_yield = 250 * 10**6 #Yield strength steel

A_tot = F_y / sigma_yield

A = A_tot / n

D = math.sqrt(4*A/math.pi)

print("Bolt area ", A)
print("Bolt D    ", D)