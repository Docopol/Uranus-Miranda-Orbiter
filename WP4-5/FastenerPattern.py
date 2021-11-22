
from Classes import *
#from Iterations_Lug import *
import math
import numpy as np

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002
gap = 0.02
thickness = 0.01

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
    Youngs_Modulus=210*(10**9),
    yield_stress=800*(10**6),
    shear_modulus=77*10**9,
    maximum_shear=600*10**6,
    max_bearing_stress=185*10**6,
    density=7850
)


F = Loads(353.0394,2118.2364,4069.2436105263155,0,141.21576000000002,0)

n = 4 #number of bolts

#w = 0.200
#h = w

def inch_to_m(l):
    return l*2.54/100

def GetSFs (F,D_1st,thickness,w,h,n):

    D_not_fail = Min_Fastener_Diameter_Tension(F,steel, n, w, h, gap)

    SF_Tension_Failure = D_1st/D_not_fail

    plate = Plate(n,D_1st, thickness, w+D_1st*1.5, h+D_1st*1.5)

    plate.get_mass(aluminium)

    cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

    plate_cg = plate.get_cg(cord)

    plate_force_cg = plate.force_cg(F.F_x,F.F_y,n)

    plate_moment_cg = plate.moment_cg(plate_cg, [0,0], F.F_x, F.F_y)

    plate_ftdm = plate.force_due_to_moment(cord, plate_cg, 0)

    plate_fm = plate.force_moment(plate_ftdm,F.F_x, F.F_y)

    shearStress = plate.fastener_shear_stress(D_1st, thickness, plate_fm)

    shearYieldStrength = 0.58 * steel.y

    SF_Shear_Failure = shearYieldStrength / shearStress

    bearing_Stress = plate.pull_through_fail(n,D_1st,D_1st*3,np.transpose(cord),thickness,thickness,36.0,gap)

    bearing_Stress_Max = max(bearing_Stress)

    SF_bearing_failure = aluminium.y/bearing_Stress_Max

    return SF_Shear_Failure, SF_bearing_failure, SF_Tension_Failure

thickness = inch_to_m(7/8)
D = inch_to_m(5/8)
w = inch_to_m(3+13/16)
W = inch_to_m(5)
h=w

#ratios
w_over_t = w/thickness
D_over_t = D/thickness
h = w
W_over_w = W/w

SFs = GetSFs(F,D, thickness, w, h, n)

while (min(SFs)>1.5):
    thickness = thickness - 0.00025
    w = w_over_t * thickness
    h = w
    D = D_over_t * thickness
    SFs = GetSFs(F,D, thickness, w, h, n)
    

thickness = thickness + 0.00025
w = w_over_t * thickness
h = w
W = W_over_w * w
D = D_over_t * thickness
SFs = GetSFs(F,D, thickness, w, h, n)

print("Safety Factors: Shear, Pull-through, Tension")
print(SFs)
print("Thickness (mm)   ", thickness*1000)
print("Width = Height (mm)  ",W*1000)
print("Distance between fasteners (mm)  ",w*1000)
print("Fastener diameter (mm)  ",D*1000)

