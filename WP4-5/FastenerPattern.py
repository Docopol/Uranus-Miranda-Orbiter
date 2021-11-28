from Classes import *
from calc import f_x_bot, f_y_bot, f_z_bot, M_y_bot
#from Iterations_Lug import *
from Constants import *
import math
import numpy as np
import time
#from Brute_Force_Iteration import *
start_time = time.time()
h_rtg = 0.456
l_rtg = 0.4
#print("--- %s seconds ---" % (time.time() - start_time))

# F_y = 2118.2364
# F_z = 4069.2436105263155
# F_x = 353.0394
# M_y = 141.21576000000002
gap = 0.02
thickness = 0.01

F = Loads(f_x_bot, f_y_bot, f_z_bot, 0, M_y_bot, 0)
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

    cord_for_pullthrough = [[-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2,w/2],[-h/2-h_rtg/2,h/2-h_rtg/2,-h/2-h_rtg/2,h/2-h_rtg/2,-h/2+h_rtg/2,h/2+h_rtg/2,-h/2+h_rtg/2,h/2+h_rtg/2]]

    bearing_Stress = plate.pull_through_fail(n*2,D_1st,D_1st*1.5,cord_for_pullthrough,thickness,thickness,36.0,l_rtg,h_rtg/2)

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

def massBackPlate (material,W,t, D):
    A = W**2 - math.pi * D**2
    return material.d*A*t

def massBolt (material,D_in,D_out,h,L):
    V = math.pi * D_in**2 / 4 * (L-2*h) + D_out**2 * math.pi / 4 * hex_circ_Ratio * 2 * h 
    return V * material.d / (1000**3)
SFs = GetSFs(D, thickness, w, h, n, Al2014T6, StA992)

print("Safety Factors Backplate/Fasteners: Shear, Pull-through, Tension")
print(SFs)
mass_min = massBackPlate(Al2014T6,W,thickness,D) + n * massBolt(StA992,D, D*1.5,D/1.5,2*thickness+2*D/1.5)

while (min(SFs) > 1.5):  # constant dimensions
#while (min(SFs)>1.5):
    thickness = thickness - 0.00025
    w = w_over_t * thickness
    h = w
    D = D_over_t * thickness
    SFs = GetSFs(D, thickness, w, h, n, Al2014T6, StA992)
    
thickness = thickness + 0.00025
w = w_over_t * thickness
h = w
W = W_over_w * w
D = D_over_t * thickness
SFs = GetSFs(D, thickness, w, h, n, Al2014T6, StA992)

mass_back_plate = W**2 * thickness * Al2014T6.get_density()
print("")
print("")
# print("Revised Safety Factors: Shear, Pull-through, Tension")
# print(SFs)
# print("Thickness (mm)   ", thickness*1000)
# print("Width = Height (mm)  ",W*1000)
# print("Distance between fasteners (mm)  ",w*1000)
# print("Fastener diameter (mm)  ",D*1000)
# print("Mass of Back plate (kg) ", mass_back_plate)


#aluminiums = (Al2014T6,Al2014T6,Al2024T4,Al7075T6)
#steels = (StA992,St8630)
#magnesium = MgAZ91CT6

materials_all = (Al2014T6,Al6061T6,StA992,MgAM60,Ti6Al4V)
#print(materials_all)
#materials_all.append(MgAZ91CT6)
#print(materials_all)

#optimal_Values = (0,0,0,0)
#print("test")

#case1 = [Al2014T6, 0.0379]
#case2 = (Ti6Al4V, 0.0379)
#case3 = (Al6061T6, 0.0379)
#case4 = (MgAM60, 0.0379)
#case5 = (StA992, 0.0379)
#case3 = ()
#cases = (case1)#,case2,case3,case4,case5)
#for case in cases:
mass_min = 100
mass_best_bolt = 100
mass_best_plate = 100
w_lug = 0.0471
for t in np.linspace(0.01,0.0005,1001):
    for bolt in bolt_D_standarts:
        D=bolt[0]/1000
        for bolt_mat in materials_all:
            plate_mat = Al2014T6
            w = w_lug + D
            if min(GetSFs(D, t, w,w,n, plate_mat, bolt_mat))>1.5:
                
                #h=w
                W = w + 4*D
                mass_plate = massBackPlate(plate_mat, W, t,D)
                mass_bolt = massBolt(bolt_mat, D, bolt[1], bolt[2], t*2000+bolt[2]*2 + 2*bolt[3])
                #mass = massBackPlate(plate_mat, W, t) + n * massBolt(bolt_mat, D, bolt[1], bolt[2], t*2000+bolt[2]*2 + 2*bolt[3])
                mass = mass_plate + n*mass_bolt

                if mass<mass_min:
                    optimal_Values=(D,t,w,W)
                    mass_min = mass
                    mass_best_bolt = mass_bolt
                    mass_best_plate = mass_plate
                    best_bolt = bolt
print("Plate material: {}, Bolt material: {}".format(plate_mat.n, bolt_mat.n))
print("Optimal fastener diameter, thickness, distance between fasteners, width")
print(optimal_Values)
#print("")
print("Total mass: {}, Plate mass: {}, single Bolt mass: {}, total Bolt mass: {}".format(mass_min,mass_best_plate,mass_best_bolt, mass_best_bolt*n))
#print("")


print("Bolt diameter: {}, Bolt length: {}, Nut/head width: {}, Nut/head thickness: {}".format(best_bolt[0], optimal_Values[1]*2000+best_bolt[2]*2 + 2*best_bolt[3],best_bolt[1], best_bolt[2]))
print("")
print("")
print("")
d = optimal_Values[2]/2
print(d)
cord_for_pullthrough_wall = [[-d,-d,d,d,-d,-d,d,d],[-d-h_rtg/2,d-h_rtg/2,-d-h_rtg/2,d-h_rtg/2,-d+h_rtg/2,d+h_rtg/2,-d+h_rtg/2,d+h_rtg/2]]

wall_stress = pull_through_fail_standalone(4,best_bolt[0]/1000,best_bolt[1]/1000,cord_for_pullthrough_wall,optimal_Values[1],optimal_Values[1],36,l_rtg,h_rtg/2)

print(Al2024T3.y/max(wall_stress))
print(max(wall_stress))

print("--- runtime: %s seconds ---" % (time.time() - start_time))