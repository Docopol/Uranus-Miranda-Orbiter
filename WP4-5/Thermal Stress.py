# all temperatures will be in kelvin
from Constants import *
import numpy as np

T_ref = 288
T_max = 298.5  # IS NOT ACTUAL TMAX probably higher
T_min = 279

D_fo = ...  # i think these can be found in classes.py... standby,
D_fi = ...
t = ...

fas_mat = StA992  # fastener material
plt_mat = Al7075T6  # material of clamped parts

delta_a = (4*t)/(plt_mat.get_E()*np.pi*(D_fo**2 - D_fi**2))  # need to define t, D_fo and D_fi
delta_b = (1/fas_mat.get_E())  # not finished
Phi = delta_a/(delta_a + delta_b)  # force ratio

A_sm = np.pi*(D_fi/2)**2

DT_max = T_max - T_ref
DT_min = T_min - T_ref

alpha_b = fas_mat.get_TEC()
alpha_c = plt_mat.get_TEC()


def maxT_stress(DT, E, A_sm, alpha_b, alpha_c, Phi):
    return (alpha_c - alpha_b) * DT * E * A_sm * (1 - Phi)


print("thermal stress at maximum temp:", maxT_stress(DT_max, fas_mat.get_E(), A_sm, alpha_b, alpha_c, Phi))
print("thermal stress at minimum temp:", maxT_stress(DT_min, fas_mat.get_E(), A_sm, alpha_b, alpha_c, Phi))
