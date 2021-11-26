# all temperatures will be in kelvin
from Constants import *

T_ref = 288
T_max = 298.5
T_min = 279

DT_max = T_max - T_ref
DT_min = T_min - T_ref

fas_mat = material_dict['Al2014T6'] # fastener material
plt_mat = material_dict['Al2014T6'] # material of clamped parts

alpha_b = fas_mat.get_TEC()
alpha_c = plt_mat.get_TEC()

def maxT_stress(DT, E, A_sm, alpha_b, alpha_c, Phi):
    return (alpha_c-alpha_b)*DT*E*A_sm*(1-Phi)