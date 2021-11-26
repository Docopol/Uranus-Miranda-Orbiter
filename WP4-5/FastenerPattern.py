from Classes import *
from calc import Force_upper_x, Force_upper_y, Force_upper_z, Moment_upper_y
#from Iterations_Lug import *
from Constants import *
import math
import numpy as np
import time
#from Brute_Force_Iteration import *
start_time = time.time()

#print("--- %s seconds ---" % (time.time() - start_time))

# F_y = 2118.2364
# F_z = 4069.2436105263155
# F_x = 353.0394
# M_y = 141.21576000000002
gap = 0.02
thickness = 0.01

F = Loads(Force_upper_x, Force_upper_y, Force_upper_z, 0, Moment_upper_y, 0)
print(F.F_z)
n = 4 #number of bolts

#w = 0.200
#h = w

def inch_to_m(l):
    return l*2.54/100

def GetSFs (D_1st,thickness,w,h,n,material_plate, material_bolt):
    #F = Loads(353.0394, 2118.2364, 4069.2436105263155, 0, 141.21576000000002, 0)
    D_not_fail = Min_Fastener_Diameter_Tension(F,material_bolt, n, w, h, gap)

    SF_Tension_Failure = D_1st/D_not_fail

    plate = Plate(n,D_1st, thickness, w+D_1st*1.5, h+D_1st*1.5)

    plate.get_mass(material_plate)

    cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

    plate_cg = plate.get_cg(cord)

    plate_force_cg = plate.force_cg(F.F_x,F.F_y,n)

    plate_moment_cg = plate.moment_cg(plate_cg, [0,0], F.F_x, F.F_y)

    plate_ftdm = plate.force_due_to_moment(cord, plate_cg, 0)

    plate_fm = plate.force_moment(plate_ftdm,F.F_x, F.F_y)

    shearStress = plate.fastener_shear_stress(D_1st, thickness, plate_fm)

    shearYieldStrength = 0.58 * material_bolt.y

    SF_Shear_Failure = shearYieldStrength / shearStress

    bearing_Stress = plate.pull_through_fail(n,D_1st,D_1st*1.5,np.transpose(cord),thickness,thickness,36.0,gap)

    bearing_Stress_Max = max(bearing_Stress)

    SF_bearing_failure = material_plate.y/bearing_Stress_Max

    return SF_Shear_Failure, SF_bearing_failure, SF_Tension_Failure

flange = Flange(inch_to_m(1+3/4),inch_to_m(1),inch_to_m(1+3/8),Al2014T6,inch_to_m(3))
lug = Lug(flange,inch_to_m(2.038),2)

def getSF_lug(lug):
    #F = Loads(353.0394, 2118.2364, 4069.2436105263155, 0, 141.21576000000002, 0)
    SF_thickness = lug.f.t/lug.minimum_t((F.F_x,F.F_y,F.F_z))
    SF_diameter_min = lug.f.d/lug.minimum_d((F.F_x,F.F_y,F.F_z))
    SF_width = lug.f.w/lug.minimum_w((F.F_x,F.F_y,F.F_z))
    SF_diameter_max = 1/(lug.f.d/lug.maximum_d((F.F_x,F.F_y,F.F_z)))
    #print(lug.minimum_w((F.F_x,F.F_y,F.F_z)))
    return SF_diameter_min, SF_diameter_max, SF_thickness, SF_width

print("")
print("")
print("Safety Factors Flanges:  diameter min, diameter max, thickness, width")
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

def massBolt (material,D_in,D_out,h,L):
    V = math.pi * D_in**2 / 4 * (L-2*h) + D_out**2 * math.pi / 4 * magic_Ratio * 2 * h 
    return V * material.d
SFs = GetSFs(D, thickness, w, h, n, Al2024T3, St4130)

print("Safety Factors Backplate/Fasteners: Shear, Pull-through, Tension")
print(SFs)
mass_min = massBackPlate(Al2024T3,W,thickness) + n * massBolt(St4130,D, D*1.5,D/1.5,2*thickness+2*D/1.5)

while (min(SFs) > 1.5):  # constant dimensions
#while (min(SFs)>1.5):
    thickness = thickness - 0.00025
    w = w_over_t * thickness
    h = w
    D = D_over_t * thickness
    SFs = GetSFs(D, thickness, w, h, n, Al2024T3, St4130)
    
thickness = thickness + 0.00025
w = w_over_t * thickness
h = w
W = W_over_w * w
D = D_over_t * thickness
SFs = GetSFs(D, thickness, w, h, n, Al2024T3, St4130)

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

aluminiums = (Al2014T6,Al2024T3,Al2024T4,Al7075T6)
steels = (St4130,St8630)
#magnesium = MgAZ91CT6

materials_all = (Al2014T6,Al2024T3,Al2024T4,Al7075T6,St4130,St8630,MgAZ91CT6)
#print(materials_all)
#materials_all.append(MgAZ91CT6)
#print(materials_all)

optimal_Values = (0,0,0,0)
#print("test")
for plate_mat in materials_all:
    for t in np.linspace(0.1,0.00005,101):
        for bolt in bolt_D_standarts:
            D=bolt[0]/1000
            for bolt_mat in materials_all:
                w = 3*D
                if min(GetSFs(D, t, w,h,n, plate_mat, bolt_mat))>1.5:
                    h=w
                    W = w + 4*D
                    mass = massBackPlate(plate_mat, W, t) + n * massBolt(bolt_mat, D, bolt[1]/1000, bolt[2]/1000, t*2+bolt[2]/1000*2 + 2*D)
            
                    if mass<mass_min:
                        optimal_Values=(D,t,w,W)
                        mass_min = mass


          
print(mass_min)

print("Optimal fastener diameter, thickness, distance between fasteners, width")
print(optimal_Values)

print("")
print("--- runtime: %s seconds ---" % (time.time() - start_time))