
from Classes import *
from Iterations_Lug import *

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002

thick = 0.01

F = Loads (353.0394,2118.2364,4069.2436105263155,0,141.21576000000002,0)

n = 4 #number of bolts

w = 200.0
h = 150.0

D_1st = Min_Fastener_Diameter_Tension(F,steel, n, w, h, 0.02)

plate = Plate(n,D_1st, thick, w+D_1st*1.5, h+D_1st*1.5)



cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

plate_cg = plate.get_cg(cord)

plate_force_cg = plate.force_cg(F.F_x,F.F_y,n)

plate_moment_cg = plate.moment_cg(plate_cg, [0,0], F.F_x, F.F_y, 0)

plate_ftdm = plate.force_due_to_moment(cord, plate_cg, 0)

plate_fm = plate.force_moment(plate_ftdm,F.F_x, F.F_y)

shearStress = plate.fastener_shear_stress(D_1st, thick, plate_fm)

print("Shear stress in fasteners   ", shearStress)


print("Bolt D    ", D_1st)