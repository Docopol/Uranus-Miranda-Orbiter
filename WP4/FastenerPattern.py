from Classes import *
from calc import f_x_bot, f_y_bot, f_z_bot, M_y_bot
from Constants import *
import math
import numpy as np
import time


start_time = time.time()
h_rtg = 0.456
l_rtg = 0.4

# Adaptations made during WP5 (lines 16-32)
m = 18119.35
g = 9.81

l = 0.197
t = 0.005
A = l**2 - (l-2*t)**2
I = (1/12) * (l**4 - (l-2*t)**4)

R = 1.414
L = 0.386

F_net = math.sqrt(2) * m * g
F_xz = F_net/2 * 3*I / (3*I + A*L*(L+R))
F_y = 133270

F = Loads(0, 133270, 123160, 51460, 0, 0)
#print(F.F_z)
n = 4  # number of bolts

gap = l/2
thickness = 0.01

def inch_to_m(l):
    return l*2.54/100


def GetSFs (D_1st,thickness,w,h,n,material_plate, material_bolt):
    D_not_fail = Min_Fastener_Diameter_Tension(F,material_bolt, n, w, h, gap)

    SF_Tension_Failure = D_1st/D_not_fail

    plate = Plate(n,D_1st, thickness, w+D_1st*1.5, h+D_1st*1.5)

    plate.get_mass(material_plate)

    cord = [[-w/2,-h/2],[-w/2,h/2],[w/2,h/2],[w/2,-h/2]]

    plate_cg = plate.get_cg(cord)

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

def massBackPlate (material,W,t, n,D):
    A = W**2 - n*math.pi * D**2
    return material.d*A*t

def massBolt (material,D_in,D_out,h,L):
    V = math.pi * D_in**2 / 4 * (L-2*h) + D_out**2 * math.pi / 4 * hex_circ_Ratio * 2 * h 
    return V * material.d / (1000**3)
SFs = GetSFs(D, thickness, w, h, n, Al2014T6, StA992)

print("Safety Factors Backplate/Fasteners: Shear, Pull-through, Tension")
print(SFs)
mass_min = massBackPlate(Al2014T6,W,thickness,n,D) + n * massBolt(StA992,D, D*1.5,D/1.5,2*thickness+2*D/1.5)

while (min(SFs) > 1.5):  # constant dimensions
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
d = w/2
cord_for_pullthrough_wall = [[-d,-d,d,d,-d,-d,d,d],[-d-h_rtg/2,d-h_rtg/2,-d-h_rtg/2,d-h_rtg/2,-d+h_rtg/2,d+h_rtg/2,-d+h_rtg/2,d+h_rtg/2]]
wall_stress = pull_through_fail_standalone(4,D,D*1.6,cord_for_pullthrough_wall,thickness,thickness,36,l_rtg,h_rtg/2)
print(max(wall_stress))

mass_back_plate = W**2 * thickness * Al2014T6.get_density()
print("")
print("")

materials_all = (Al2014T6,Al6061T6,StA992,MgAM60,Ti6Al4V)
w_lug = 0.175
mass_min = 100000
mass_best_bolt = 100
mass_best_plate = 100

for t in np.linspace(10,0.005,1001):
    #print("test1")
    for bolt in bolt_D_standarts:
        #print("test2")
        D=bolt[0]/1000
        for bolt_mat in materials_all:
            plate_mat = Al7075T6
            w = w_lug + D
            if min(GetSFs(D, t, w,w,n, plate_mat, bolt_mat))>1.5:
                print("test4")
                W = w + 4*D
                mass_plate = massBackPlate(plate_mat, W, t,n,D)
                mass_bolt = massBolt(bolt_mat, D, bolt[1], bolt[2], t*2000+bolt[2]*2 + 2*bolt[3])
                mass = mass_plate + n*mass_bolt

                if mass<mass_min:
                    
                    optimal_Values=(D,t,w,W)
                    print("test5")
                    mass_min = mass
                    mass_best_bolt = mass_bolt
                    mass_best_plate = mass_plate
                    best_bolt = bolt
print("Plate material: {}, Bolt material: {}".format(plate_mat.n, bolt_mat.n))
print("Optimal fastener diameter, thickness, distance between fasteners, width")
print(optimal_Values)
print("Total mass: {}, Plate mass: {}, single Bolt mass: {}, total Bolt mass: {}".format(mass_min,mass_best_plate,mass_best_bolt, mass_best_bolt*n))


print("Bolt diameter: {}, Bolt length: {}, Nut/head width: {}, Nut/head thickness: {}".format(best_bolt[0], optimal_Values[1]*2000+best_bolt[2]*2 + 2*best_bolt[3],best_bolt[1], best_bolt[2]))
print("")
print("")
print("")
d = optimal_Values[2]/2
cord_for_pullthrough_wall = [[-d,-d,d,d,-d,-d,d,d],[-d-h_rtg/2,d-h_rtg/2,-d-h_rtg/2,d-h_rtg/2,-d+h_rtg/2,d+h_rtg/2,-d+h_rtg/2,d+h_rtg/2]]

wall_stress = pull_through_fail_standalone(4,best_bolt[0]/1000,best_bolt[1]/1000,cord_for_pullthrough_wall,optimal_Values[1],optimal_Values[1],36,l_rtg,h_rtg/2)

print(Al2024T3.y)
print(max(wall_stress))

print("--- runtime: %s seconds ---" % (time.time() - start_time))