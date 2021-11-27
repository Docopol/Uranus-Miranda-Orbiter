# all temperatures will be in kelvin
from Constants import *
import numpy as np

T_ref = 288
T_max = 298.5  # IS NOT ACTUAL TMAX probably higher
T_min = 279

D_fo = ...  # outer diameter of the bolt
D_fi = ...  # inner diameter of the bolt
t = ...  # thickness of the clamped material

fas_mat = StA992  # fastener material
plt_mat = Al7075T6  # material of clamped parts

delta_a = (4*t)/(plt_mat.get_E()*np.pi*(D_fo**2 - D_fi**2))
delta_b = ...  # (1/fas_mat.get_E())*sum(L_i/A_i)+(L_nsub)/(E_n*A_nom)  # not finished
Phi = delta_a/(delta_a + delta_b)  # force ratio

A_sm = np.pi*(D_fi/2)**2  # Stiffness Area

DT_max = T_max - T_ref
DT_min = T_min - T_ref

alpha_b = fas_mat.get_TEC()
alpha_c = plt_mat.get_TEC()


def maxT_stress(DT, E, A_sm, alpha_b, alpha_c, Phi):
    return (alpha_c - alpha_b) * DT * E * A_sm * (1 - Phi)


print("thermal stress at maximum temp:", maxT_stress(DT_max, fas_mat.get_E(), A_sm, alpha_b, alpha_c, Phi))
print("thermal stress at minimum temp:", maxT_stress(DT_min, fas_mat.get_E(), A_sm, alpha_b, alpha_c, Phi))
