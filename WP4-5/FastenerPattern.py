from Classes import *
#from Iterations_Lug import *
from Constants import *
import math
import numpy as np

F_y = 2118.2364
F_z = 4069.2436105263155
F_x = 353.0394
M_y = 141.21576000000002
gap = 0.02
thickness = 0.01

F = Loads(353.0394, 2118.2364, 4069.2436105263155, 0, 141.21576000000002, 0)

n = 4 #number of bolts

#w = 0.200
#h = w

def inch_to_m(l):
    return l*2.54/100

def GetSFs (D_1st,thickness,w,h,n):
    F = Loads(353.0394, 2118.2364, 4069.2436105263155, 0, 141.21576000000002, 0)
    D_not_fail = Min_Fastener_Diameter_Tension(F,St8630, n, w, h, gap)

    SF_Tension_Failure = D_1st/D_not_fail

    plate = Plate(n,D_1st, thickness, w+D_1st*1.5, h+D_1st*1.5)

    plate.get_mass(Al2014T6)

    cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

    plate_cg = plate.get_cg(cord)

    plate_force_cg = plate.force_cg(F.F_x,F.F_y,n)

    plate_moment_cg = plate.moment_cg(plate_cg, [0,0], F.F_x, F.F_y)

    plate_ftdm = plate.force_due_to_moment(cord, plate_cg, 0)

    plate_fm = plate.force_moment(plate_ftdm,F.F_x, F.F_y)

    shearStress = plate.fastener_shear_stress(D_1st, thickness, plate_fm)

    shearYieldStrength = 0.58 * St8630.y

    SF_Shear_Failure = shearYieldStrength / shearStress

    bearing_Stress = plate.pull_through_fail(n,D_1st,D_1st*3,np.transpose(cord),thickness,thickness,36.0,gap)

    bearing_Stress_Max = max(bearing_Stress)

    SF_bearing_failure = Al2014T6.y/bearing_Stress_Max

    return SF_Shear_Failure, SF_bearing_failure, SF_Tension_Failure

flange = Flange(inch_to_m(1+3/4),inch_to_m(1),inch_to_m(1+3/8),Al2014T6,inch_to_m(3))
lug = Lug(flange,inch_to_m(2.038),2)

def getSF_lug(lug):
    F = Loads(353.0394, 2118.2364, 4069.2436105263155, 0, 141.21576000000002, 0)
    SF_thickness = lug.f.t/lug.minimum_t((F.F_x,F.F_y,F.F_z))
    SF_diameter_min = lug.f.d/lug.minimum_d((F.F_x,F.F_y,F.F_z))
    SF_width = lug.f.w/lug.minimum_w((F.F_x,F.F_y,F.F_z))
    SF_diameter_max = 1/(lug.f.d/lug.maximum_d((F.F_x,F.F_y,F.F_z)))
    #print(lug.minimum_w((F.F_x,F.F_y,F.F_z)))
    return SF_diameter_min, SF_diameter_max, SF_thickness, SF_width

print("")
print("")
print("Safety Factors Lugs:  diameter min, diameter max, thickness, width")
print(getSF_lug(lug))

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

def massBackPlate (material,W,t):
    return material.d*W**2*t

SFs = GetSFs(D, thickness, w, h, n)

print("Safety Factors: Shear, Pull-through, Tension")
print(SFs)
mass_min = massBackPlate(Al2024T3,W,thickness)


while (min(SFs)>1.5):
    thickness = thickness - 0.00025
    w = w_over_t * thickness
    h = w
    D = D_over_t * thickness
    SFs = GetSFs(D, thickness, w, h, n)
    
thickness = thickness + 0.00025
w = w_over_t * thickness
h = w
W = W_over_w * w
D = D_over_t * thickness
SFs = GetSFs(D, thickness, w, h, n)

mass_back_plate = W**2 * thickness * Al2014T6.get_density()
print("")
print("")
print("Revised Safety Factors: Shear, Pull-through, Tension")
print(SFs)
print("Thickness (mm)   ", thickness*1000)
print("Width = Height (mm)  ",W*1000)
print("Distance between fasteners (mm)  ",w*1000)
print("Fastener diameter (mm)  ",D*1000)
print("Mass of Back plate (kg) ", mass_back_plate)

print("")
print("")


#print("test")
for t in np.linspace(0.01,0.0005,100):
    for w in np.linspace(0.4,0.01,100):
        for D in np.linspace(0.01,0.003,100):
            if min(GetSFs (D, t, w,h,n))>1.5:
                h=w
                W = W_over_w * w
                mass = massBackPlate(Al2024T3, W, t)
            
                if mass<mass_min:
                    mass_min = mass


#print("test end")               
print(mass_min)

