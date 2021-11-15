
from Classes import *
from Iterations_Lug import *

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002

F = Loads (353.0394,2118.2364,4069.2436105263155,0,141.21576000000002,0)

n = 4 #number of bolts

w = 200.0
h = 150.0

D = Min_Fastener_Diameter_Tension(F,steel, n, w, h, 0.02)

print("Bolt D    ", D)