import input_parameters as i
import math


def dimensions(d, V, th):   # inner diameter, maximal volume
    r = d / 2                       # [m] inner radius
    a = math.pi * (r ** 2)          # [m^2] inner area
    h = V / a                       # [m] height
    R = r + th                       # [m] outer radius
    A = math.pi * (R ** 2)          # [m^2] outer area
    ca = A - a                      # [m^2] cross sectional area
    I_a = math.pi * th * (R ** 3)    # [m^4] second moment of area
    return {
        "Height": h,
        "Outer Radius": R,
        "Cross Sectional Area": ca,
        "Outer Area": A,
        "Second Moment of Area": I_a
    }


def stresses(M, g_a, g_l, dims, p, th):    # s/c mass, axial load, lateral load, dimensions
    A = dims["Cross Sectional Area"]
    h = dims["Height"]
    r = dims["Outer Radius"]
    I_a = dims["Second Moment of Area"]
    P_a = M * g_a                               # [N] axial load
    V = M * g_l                                 # [N] lateral load
    sigma_a = (P_a / A) * 1e-6                  # [MPa] axial stress
    sigma_l = (V * (h / 2) * r / I_a) * 1e-6    # [MPa] bending stress
    tau_av = (V / A) * 1e-6                     # [MPa] average shear stress
    # sigma_hoop = p * r / th                   # [MPa] hoop stress
    sigma_long = (p * r / (2 * th)) * 1e-6      # [MPa] longitudinal stress
    sigma_n = sigma_a + sigma_l + sigma_long    # [MPa] maximal normal stress !!!!CHECKKKK
    tau_max = tau_av                            # [MPa] maximal shear stress
    return {
        "Max Normal Stress": round(sigma_n, 1),
        "Max Shear Stress": round(tau_max, 1)
    }


def strains(strss, E, G):       # stresses, elastic modulus, shear modulus
    sigma_n = strss["Max Normal Stress"]
    tau_av = strss["Max Shear Stress"]
    epsilon = sigma_n / E       # [mm] normal strain
    gamma = tau_av / G          # [mm] shear strain
    return {
        "Normal Strain": round(epsilon, 3),
        "Shear Strain": round(gamma, 3)
    }


def mass(dims, rho, th):
    h = dims["Height"]
    R = dims["Outer Radius"]
    V = (math.pi * (R ** 2) + math.pi * 2 * R * h) * th      # [m^3] total volume of structural elements
    m = V * rho     # [kg] total structure mass
    return round(m, 1)


t = 0.0001      # [m] wall thickness
dt = 0.0001     # [m] change in thickness per iteration

while True:
    Dimensions = dimensions(i.d, i.V, t)    # compute dimensions

    Stresses = stresses(i.M, i.g_axial, i.g_lateral, Dimensions, i.p, t)    # compute stresses
    if (Stresses["Max Normal Stress"] or Stresses["Max Shear Stress"]) > i.sigma_y:
        t += dt     # if stresses too high increase thickness and iterate again
        continue

    Strains = strains(Stresses, i.E, i.G)       # compute strains
    # if (Strains["Normal Strain"] or Strains["Shear Strain"]) > 10:
    #    t += dt  # if strains too high increase thickness and iterate again
    #    continue
    Structure_Mass = mass(Dimensions, i.rho, t)     # compute structure mass
    break

print(Stresses)
print(Strains)
print(Structure_Mass, round(t, 4))
