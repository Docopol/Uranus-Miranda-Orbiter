
from Classes import *
#from Iterations_Lug import *

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002
gap = 0.02
thick = 0.01

aluminium = Material(
    name='aluminium',
    Youngs_Modulus=75*10**9,
    yield_stress=265*10**6,
    shear_modulus=24*10**9,
    maximum_shear=207*10**6,
    max_bearing_stress=1.6*265*10**6,
    density=2700
)
iron = Material(
    name='iron',
    Youngs_Modulus=175*10**9,
    yield_stress=465*10**6,
    shear_modulus=41*10**9,
    maximum_shear=0.6*465*10**6,
    max_bearing_stress=1.5*465*10**6,
    density=7200
)
steel = Material(
    name='steel',
    Youngs_Modulus=210*10**9,
    yield_stress=800*10**6,
    shear_modulus=77*10**9,
    maximum_shear=600*10**6,
    max_bearing_stress=185*10**6,
    density=7850
)


F = Loads(353.0394,2118.2364,4069.2436105263155,0,141.21576000000002,0)

n = 4 #number of bolts

w = 200.0
h = 150.0

D_1st = 1.5 * Min_Fastener_Diameter_Tension(F,steel, n, w, h, gap)

plate = Plate(n,D_1st, thick, w+D_1st*1.5, h+D_1st*1.5)

plate.get_mass(aluminium)

cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

plate_cg = plate.get_cg(cord)

plate_force_cg = plate.force_cg(F.F_x,F.F_y,n)

plate_moment_cg = plate.moment_cg(plate_cg, [0,0], F.F_x, F.F_y)

plate_ftdm = plate.force_due_to_moment(cord, plate_cg, 0)

plate_fm = plate.force_moment(plate_ftdm,F.F_x, F.F_y)

shearStress = plate.fastener_shear_stress(D_1st, thick, plate_fm)

print("Shear stress in fasteners   ", shearStress/(10**6), "MPa")

shearYieldStrength = 0.58 * steel.y

SF_Shear_Failure = shearYieldStrength / shearStress

print("Shear stress Safety Factor  ", SF_Shear_Failure)

print("Bolt D    ", D_1st)